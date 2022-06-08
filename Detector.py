from bs4 import BeautifulSoup
import requests, os, json
from os.path import exists
from TwitterClient import TwitterClient


new_line = '\n'
tweet_limit = 250
endpoints = {
    "fr": {
        "male": "https://www.lululemon.fr/fr-fr/c/hommes/collections/on-en-a-trop-pour-hommes?sz=1",
        "female": "https://www.lululemon.fr/fr-fr/c/femmes/collections/on-en-a-trop?sz=300"
    }
}


class WMTM:
    def __init__(self, country):
        self.country = country
        self.endpoint = endpoints[country]

    def getItems(self, gender):
        fileName = f'items_{self.country}_{gender}.json'
        html_content = requests.get(self.endpoint[gender]).text
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('div', class_="col-6 col-md-4")
        print(f"{len(items)} products currently in WMTM")
        current_items = []
        for item in items:
            itemName = ' '.join(item.find("img")["alt"].replace('"', 'inch').split()) # remove non breaking space
            sizes = self.getSizes(item)
            current_items.append(f"{itemName}{sizes}")
        current_items = set(current_items)

        if (not exists(fileName)):
            os.system('echo {} > ' + fileName)
        f = open(fileName, 'r',  encoding='utf-8')
        dic = json.loads(f.read())
        f.close()

        old_items = set(dic.keys())
        new_items = current_items.difference(old_items)
        return new_items, current_items

    def formatMessages(self, new_items, gender):
        header = f"Nouveau produits {'hommes' if gender=='male' else 'femmes'}:{new_line}"
        splitted_message = []
        message = ""
        for i, item in enumerate(new_items):
            if (len(message + f'{new_line}{item}'))>tweet_limit:
                splitted_message.append(f"{message}{new_line}{i}")
                message = ""
            message += f'{new_line}{item}'
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

    def getSizes(self, item):
        return ""
        # print(item)
        # # get url
        # item_html = requests.get(itemURL).text
        # soup = BeautifulSoup(item_html, 'html.parser')
        # pass
            

if __name__=="__main__":
    os.remove("items_fr_male.json")
    wmtm = WMTM("fr")
    wmtm.tweetNewProducts("male")
    # wmtm.tweetNewProducts("female")