from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

#kdyby neslapalo tak python -m pip install -r requirements.txt
#stahni si chromedriver.exe a dej ho do slozky C:\Program Files (x86)\chromedriver.exe :D
s = Service("C:\Program Files (x86)\chromedriver.exe")

chromeOptions = Options()
chromeOptions.headless = False
driver = webdriver.Chrome(service = s, options= chromeOptions)


def pagescrape(links):
    listings = driver.find_elements(By.CLASS_NAME, value="property.ng-scope") 
    for listing in listings :
        aTag = listing.find_element(By.TAG_NAME, value="a")
        link = aTag.get_attribute("href")
        links.append(link)
    return links
    

def getpage(page):
    url = f'http://www.sreality.cz/hledani/prodej/byty?no_shares=1&strana={page}&bez-aukce=1'
    driver.get(url)
    # wait for the page to be loaded
    time.sleep(5)


def getNumPages(numOfPropsOnPage):
    allProperties = driver.find_element(By.CLASS_NAME, value="info.ng-binding").text.split(' ')
    pages = (allProperties[5]+ allProperties[6])
    pages = (int(pages)/numOfPropsOnPage)
    return int(pages)

def getCity():
    loc = driver.find_element(By.CLASS_NAME, value="location-text.ng-binding").text.split(',')
    ulice = loc[0]
    city = loc[1].split('-')
    mesto = city[0].replace(" ","")
    if len(city) < 3:
        cast_mesta = None
    else:
        cast_mesta = city[1][1:]
    return [ulice,mesto,cast_mesta]

def getName():
    heading = driver.find_element(By.CLASS_NAME, value="name.ng-binding").text.split(' ')
    return heading

def getPrice(type):
    element = driver.find_element(By.CLASS_NAME, value="norm-price.ng-binding").text
    ss = element.replace(" ","")

    if type == "Prodej":
        price = ss[:-2]
        unit =  element[-2:] 

    elif type == "Pronájem":
        s =ss.replace("zaměsíc","")
        price = s[:-2]
        unit = s[-2:]

    return [price,unit]

def getText():
    clas = driver.find_element(By.CLASS_NAME, value="description.ng-binding")
    test = clas.find_elements(By.TAG_NAME, value="p")

    text = []
    for head in test:
        if head.text != "":
            text.append(head.text)
    plainText = ' '.join(text)
    return plainText

def getNarocnost():
    try:
        energie = driver.find_element(By.CLASS_NAME, value="energy-efficiency-rating__type.ng-binding").text
    except:
        return None
    else:
        return energie

def find_el(type):
                try:
                    if type == "false":
                        val = 'icof.icon-cross.ng-scope'
                    else:
                        val = 'icof.icon-ok.ng-scope'
                    test.find_element(By.CLASS_NAME, value=val)
                except:
                    pass
                else:
                    pass
                    rnd = str[0].lower()[:-1]
                    if type == 'false':
                        obj[f'{rnd}'] = None
                    else:
                        obj[f'{rnd}'] = True

#load 1st page without scraping to get num of pages
getpage(1)

# testing links
# links = ['https://www.sreality.cz/detail/prodej/byt/1+kk/plzen-doubravka-na-kovarne/3546888012',
#          'https://www.sreality.cz/detail/prodej/byt/1+1/rokycany-nove-mesto-prazska/3572290636',
#          'https://www.sreality.cz/detail/pronajem/byt/1+kk/praha-liben-u-svobodarny/3434726476'
#          ]


links = []
#scrape all pages return urls to list Links
# for num in range(1,getNumPages(20)): loop through all pages

for num in range(1,2):
    getpage(num)
    pagescrape(links)
print(len(links))

list = []
for link in links:
    driver.get(link)
    time.sleep(5)
    start = time.time()
    # print(getName())
    # print(getCity())
    # print(getPrice(getName()[0]))
    # print(getText())
    name = getName()
    city = getCity()
    cena = getPrice(getName()[0])
    obj = {
        'transakce': name[0],
        'typ_nemovitosti': name[1],
        'vel_kk': name[2],
        'velikost': name[3],
        'jednotka_vel' : name[4],
        'ulice': city[0],
        'mesto': city[1],
        'cast_mesta':city[2],
        'cena': cena[0],
        'jednotka_cena':cena[1],
        'text': getText(),
        'narocnost': getNarocnost(),
        'aktualizace': None,
        'id' : None,
        'stav': None,
        'stavba': None,
        'vlastnictvi': None,
        'umisteni': None,
        'patro': None,
        'celk_pater': None,
        'uzitna_plocha': None,
        'balkon': None,
        'sklep': None,
        'parkovani': None,
        'datum_post': None,
        'topeni': None,
        'odpad': None,
        'voda': None,
        'elektrina': None,
        'doprava': None,
        'vybaveni': None
    }
    upper = driver.find_element(By.CLASS_NAME, value="params.clear")
    for el in upper.find_elements(By.TAG_NAME, value="ul"):
        for test in el.find_elements(By.TAG_NAME, value="li"):
            #toogles like vytah atd.... TRUE FALSE
            
            el = test.text
            str = el.split(" ")
            
            find_el('false')
            find_el('true')
            #str conditions
            if str[0] == "Aktualizace:":
                obj['aktualizace'] = str[1]

            elif str[0] == "ID:":
                obj['id'] = str[1]
            
            elif str[0] == "ID":
                obj['id'] = str[2]

            elif str[0] == "Stav":
                obj['stav'] = str[2]

            elif str[0] == "Stavba:":
                obj['stavba'] = str[1]

            elif str[0] == "Vlastnictví:":
                obj['vlastnictvi'] = str[1]

            elif str[0] == "Umístění":
                str.pop(0)
                obj['umisteni'] = str

            elif str[0] == "Podlaží:":
                obj['patro'] = str[1]
                if len(str) > 5:
                    obj['celk_pater'] = str[5]
                else:
                    pass

            elif str[0] == "Užitná":
                obj['uzitna_plocha'] = str[2]

            elif str[0] == "Balkón:":
                if len(str) > 1:
                    obj['balkon'] = str[1]
                else:
                    pass

            elif str[0] == "Parkování:":
                if len(str) > 1:
                    obj['parkovani'] = str[1]
                else:
                    pass

            elif str[0] == "Datum":
                if obj['transakce'] == 'prodej':
                    obj['datum_post'] = str[3]
                else:
                    obj['datum_post'] = str[2]

            elif str[0] == "Topení:":
                str.pop(0)
                obj['topeni'] = str

            elif str[0] == "Odpad:":
                str.pop(0)
                obj['odpad'] = str

            elif str[0] == "Elektřina:":
                str.pop(0)
                obj['elektrina'] = str

            elif str[0] == "Voda:":
                str.pop(0)
                obj['voda'] = str
            
            elif str[0] == "Doprava:":
                str.pop(0)
                obj['doprava'] = str
            
            elif str[0] == "Vybavení:":
                if len(str) > 1:
                    obj['vybaveni'] = str[1]
            

    list.append(obj)
    print(f'{time.time()- start} s')
    print(link)
print(list)
    
driver.quit()

