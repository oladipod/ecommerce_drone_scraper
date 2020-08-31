import requests
import bs4 as bs
import time
import csv
class Scraper:
    def __init__(self,mainUrl:str):
        self.mainUrl = mainUrl
        self.csvInitialized = False
        self.filename = 'scraped.csv'
        self.products = []
        self.page = 1

    def openFile(self):
        with open(self.filename, 'w', newline='') as f:
            file = f
            writer = csv.writer(file)
            writer.writerow(['Product Name','Product Manufacturer','Product price','Product Url','Product Images'])
            file.close()
        self.csvInitialized = True
        

    def writeProducts(self,product_inf: list):
        if self.csvInitialized == False: self.openFile()
        with open(self.filename, 'a', newline='') as f:
            file = f
            writer = csv.writer(file)
            for pro in product_inf:
                writer.writerow(pro)
            file.close()
            

    def scrape(self):
        page = requests.get(self.mainUrl)
        mainSource = bs.BeautifulSoup(page.content,'html.parser')
        navObject: bs.BeautifulSoup
        for navObject in self.getNavObjectElements(mainSource):
            try:
                self.scrapeSection(navObject)
            except Exception as e:
                print(e)
        try:
            self.writeProducts(self.products)
        except Exception as e:
            print(e)
        

    def getNavObjectElements(self,bsSource: bs.BeautifulSoup) -> list:
        nav: bs.BeautifulSoup =  bsSource.find('div',{'id':'block_top_menu'})
        nav_ul: bs.BeautifulSoup = nav.findChild('ul')
        return nav_ul.children

    def scrapeSection(self, section: bs.BeautifulSoup):
        url: bs.BeautifulSoup = section.findChild('a')
        sectionPage = requests.get(url.attrs['href'])
        sectionSoup = bs.BeautifulSoup(sectionPage.content, 'html.parser')
        main: bs.BeautifulSoup = sectionSoup.findChild('main',{'class':'col-xs-12 col-sm-9'})
        categoryTableFinder: bs.BeautifulSoup = main.findChild('table')
        if (type(categoryTableFinder) == type(None)):
            self.scrapePage(main, url.attrs['href']),
        else:
            tr: bs.BeautifulSoup
            for tr in categoryTableFinder.findChild('tbody').children:
                tds = tr.children
                tds: bs.BeautifulSoup
                for td in tds:
                    try:
                        td_url: bs.BeautifulSoup = td.findChild('a')
                        req = requests.get(td_url.attrs['href'])
                        pageSoup: bs.BeautifulSoup = bs.BeautifulSoup(req.content,'html.parser')
                        self.scrapePage(pageSoup,td_url.attrs['href'])
                    except Exception as e:
                        print(e)


    def scrapePage(self, pageSoup:bs.BeautifulSoup,url:str = None):
        print(':::::::::::{}'.format(url))
        self.page += 1
        if (type(url) == type(None)):
            pass
        else:
            pageSoup = bs.BeautifulSoup(requests.get(url).content,'html.parser')
        categoryProduct: bs.BeautifulSoup = pageSoup.find('section',{'id':'category-products'})
        ul: bs.BeautifulSoup = categoryProduct.find('ul')
        child: bs.BeautifulSoup
        no_child = 0
        for child in ul.children:
            # no_child += 1
            # if(no_child ==3):
            #     break
            a: bs.BeautifulSoup = child.findChild('a')

            product_url = a.attrs['href']
            productPage = requests.get(product_url)
            productPageSoup: bs.BeautifulSoup = bs.BeautifulSoup(productPage.content,'html.parser')
            primaryBlockRow: bs.BeautifulSoup = productPageSoup.find('div',{'class':'primary_block row'})
            primaryBlockRowList = [*primaryBlockRow.children]
            imageSection: bs.BeautifulSoup = primaryBlockRowList[0]
            informationSection: bs.BeautifulSoup = primaryBlockRowList[1]
            product_name = informationSection.find('h1',{'itemprop':'name'}).getText()
            product_manufacturer = ''
            try:
                product_manufacturer = informationSection.find('p',{'id':'product_brand'}).findChild('span',{'itemprop':'name'}).getText()
            except Exception as e:
                print(e)
                product_manufacturer = ''
            product_price = ''
            try:
                product_price = informationSection.find('span',{'id':'our_price_display'}).getText()
            except Exception as e:
                print(e)
            image_link_list: list = []
            image_link_list.append(imageSection.find('img',{'id':'bigpic'}).attrs['src'])
            thumb_ul: bs.BeautifulSoup = imageSection.find('ul',{'id':'thumbs_list_frame'})
            for thumb_img in thumb_ul.children:
                image_link_list.append(thumb_img.find('a').attrs['href'])

            product_all_inf = [product_name, product_manufacturer, product_price, product_url,'|'.join(image_link_list)]
            if product_all_inf in self.products:
                print('product already exist:::::::probably in a last page')
                self.page == 1
            else:
                print(product_all_inf)
                self.products.append(product_all_inf)
            if len(self.products) >= 10:
                self.writeProducts(self.products)
                self.products = []
            time.sleep(5) #to avoid overloading the server
        if no_child == 0 or self.page>=5:
            print(':::::::::::::::::::::::::::::::::::::::::\n:::::::::::::::::::::::::::::\n::::::::::{}'.format(url))
            self.page = 1
            return
        else:
            self.scrapePage(None,'{}#/page-{}'.format(url.split('#')[0],str(self.page)))





s = Scraper('https://www.drone-fpv-racer.com/')
s.scrape()
