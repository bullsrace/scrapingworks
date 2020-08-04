import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

class Olx(scrapy.Spider):
    name = 'olx_in'
    headers = {
    	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    url = 'https://www.olx.in/api/relevance/search?facet_limit=100&lang=en&location=1000001&location_facet_limit=20&query=houses%20and%20apartments%20for%20sale&showAllCars=true&spellcheck=true'

    def __init__(self):
    	with open('result.csv', 'w') as csv_file:
    		csv_file.write('title,description,location,features,date,price\n')

    def start_requests(self):
    	for page in range(0, 10):
    		yield scrapy.Request(url=self.url + '&page=' + str(page), headers=self.headers, callback=self.parse)

    def parse(self, response):
    	data = response.text
    	data = json.loads(data)
    	
    	for offer in data['data']:
    		items = {
    			'title': offer['title'],
    			'description': offer['description'].replace('\n',' '),
    			'location': offer['locations_resolved']['COUNTRY_name'] +", "+ offer['locations_resolved']['ADMIN_LEVEL_1_name'] +", "+ offer['locations_resolved']['ADMIN_LEVEL_3_name'] +", "+ offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name'],
    			'features': offer['main_info'],
    			'date': offer['display_date'],
    			'Price':"Rs "+str(offer['price']['value']['raw'])
    		}
    		with open('result.csv','a',encoding='utf-8') as csv_file:
    			writer = csv.DictWriter(csv_file, fieldnames=items.keys())
    			writer.writerow(items)

#run scraper
process = CrawlerProcess()
process.crawl(Olx)
process.start()

#debug
#Olx.parse(Olx,'')