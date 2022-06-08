from lxml import etree
import requests
from io import StringIO
import lxml.html

content = requests.get("https://www.lululemon.fr/fr-fr/c/hommes/collections/on-en-a-trop-pour-hommes?sz=10").text



root = lxml.html.fromstring(content)
items = root.xpath("//div[@class='col-6 col-md-4']")

for item in items:
    itemURL = item.xpath("//div[@class='image-container']/a[@data-lulu-attributes]/@href")[0]
    print(itemURL)

    itemContent = requests.get(itemURL).text
    itemRoot = lxml.html.fromstring(itemContent)
    sizes = itemRoot.xpath("//div[@data-attr='size']//div[@class='custom-select-btn '][span/input[not(@disabled)]]//label/text()") # <div class="custom-select-btn ">
    print(sizes[0])
