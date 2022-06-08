from bs4 import BeautifulSoup
import requests, os, json
from os.path import exists
from TwitterClient import TwitterClient
import lxml.html


new_line = '\n'
tweet_limit = 250
endpoints = {
    "fr": {
        "male": "https://www.lululemon.fr/fr-fr/c/hommes/collections/on-en-a-trop-pour-hommes?sz=400",
        "female": "https://www.lululemon.fr/fr-fr/c/femmes/collections/on-en-a-trop?sz=400"
    }
}


class WMTM:
    def __init__(self, country):
        self.country = country
        self.endpoint = endpoints[country]

    # compute new products that were recently added to WMTM for a specific gender
    # return: ([{}], [{}])
    def getItems(self, gender):
        fileName = f'items_{self.country}_{gender}.json'
        html_content = requests.get(self.endpoint[gender]).text
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('div', class_="col-6 col-md-4")
        print(f"{len(items)} products currently in WMTM")
        current_items = []
        for item in items:
            itemName = ' '.join(item.find("img")["alt"].replace('"', 'inch').split()) # remove non breaking space
            sizes = self.getSizes(str(item))
            current_items.append(f"{itemName} ({sizes})")
        current_items = set(current_items)

        if (not exists(fileName)):
            os.system('echo {} > ' + fileName)
        f = open(fileName, 'r',  encoding='utf-8')
        dic = json.loads(f.read())
        f.close()

        old_items = set(dic.keys())
        new_items = current_items.difference(old_items)
        return new_items, current_items

    # get messages for new products
    # return: [string]
    def formatMessages(self, new_items, gender):
        header = f"Nouveau produits {'hommes' if gender=='male' else 'femmes'}:{new_line}"
        splitted_message = []
        message = ""
        j = 0
        for i, item in enumerate(new_items):
            if (len(message + f'{new_line}{item}'))>tweet_limit:
                splitted_message.append(f"{message}{new_line}{j}")
                message = ""
            message += f'{new_line}{item}'
            j+=1
        splitted_message.append(f"{message}{new_line}")
        splitted_message[0] = header + splitted_message[0]
        return splitted_message

    def tweetNewProducts(self, gender):
        new_items, current_items = self.getItems(gender)
        if (len(new_items) > 0):
            # save current items
            current_state = {}
            for i in current_items:
                current_state[i] = "value"
            with open(f'items_{self.country}_{gender}.json', 'w', encoding='utf-8') as f:
                json.dump(current_state, f, ensure_ascii=False, indent=4)

            # send tweets
            messages = self.formatMessages(new_items, gender)
            tc = TwitterClient("credentials.json")
            for message in messages:
                print(f'{self.country}_{gender}')
                print(message)
                tc.tweet(message)
        else:
            print("no new items")

    # itemHTML: string (from product's html page)
    # return: string (product's available sizes)
    def getSizes(self, itemHTML):
        itemRoot = lxml.html.fromstring(itemHTML)
        itemURL = itemRoot.xpath("//div[@class='image-container']/a[@data-lulu-attributes]/@href")[0]
        itemContent = requests.get(itemURL).text
        itemRoot = lxml.html.fromstring(itemContent)
        sizes = itemRoot.xpath("//@data-availablesizes")[0]
        if (sizes == "ONE SIZE"):
            return ""
        else:
            return sizes

    # return old price and reduced price from product's html
    def getPrices(self, itemHTML):
        itemRoot = lxml.html.fromstring(itemHTML)
        newPrice = itemRoot.xpath("//span[@class='cta-price-value'][span[@class='list-price'] and span[@class='markdown-prices']]/span[@class='markdown-prices']/text()")
        oldPrice = itemRoot.xpath("//span[@class='cta-price-value'][span[@class='list-price'] and span[@class='markdown-prices']]/span[@class='list-price']/text()")
        return oldPrice, newPrice

if __name__=="__main__":
    wmtm = WMTM("fr")
    wmtm.tweetNewProducts("male")
    wmtm.tweetNewProducts("female")