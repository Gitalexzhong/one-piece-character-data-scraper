import scrapy
import string
from PIL import Image
import requests
from io import BytesIO
import base64

class OnepieceSpider(scrapy.Spider):
    name = 'char_info'
    allowed_domains = ['onepiece.fandom.com']

    def start_requests(self):
        urls = ['https://onepiece.fandom.com/wiki/List_of_Canon_Characters']
        for url in urls:
            yield scrapy.Request(url, self.extract_links)

    def extract_links(self, response):
        characters = response.xpath(
            "//h2[1]//following::table[position()<3]//tbody/tr/td[2]/a/@href").getall()
        
        # for character in characters:
            # yield response.follow(character, callback=self.extract_info)

        yield response.follow(characters[0], callback=self.extract_info)
        yield response.follow(characters[1], callback=self.extract_info)

    def extract_info(self, response):
        character = response.xpath(
            "//aside//*[contains(@class,'pi-item pi-item-spacing pi-title')]/text()").get()
        sections = response.xpath(
            "//aside/*[contains(@class, 'pi-item pi-group')]")
        section_data = {}
        # for section in sections:

        #     section_name = section.xpath("descendant::h2/text()").get()
        #     data_items = section.xpath("descendant::div[contains(@class, 'pi-item pi-data')]")
        #     if len(data_items) > 0: 
        #         data_labels = []
        #         data_values = []
        #         for item in data_items:
        #             data_labels.append(item.xpath("descendant::*[contains(@class, 'pi-data-label')]/text()").get())
        #             data_values.append(item.xpath("descendant::*[contains(@class, 'pi-data-value')]//text()").getall())
        #         section_items = dict(zip([label.translate(str.maketrans('', '', string.punctuation)) for label in data_labels], [''.join(value) for value in data_values]))  
        #         section_data[section_name] = section_items
        
        sectionse = response.xpath(
            "//aside/*[contains(@class, 'pi-image-collection')]/*[contains(@class, 'wds-tab__content')]/*[contains(@class, 'pi-item pi-image')]/*[contains(@class, 'image image-thumbnail')]/*[contains(@class, 'pi-image-thumbnail')]").get("src")

        links = [ x for x in sectionse.split(" ") if "src" in x ]
        url = links[0].replace("src=", "").replace("\"", "")

        section_data["image_base64"] = str(get_as_base64(url))

        yield {character: section_data}





def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)
