import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from scrapy.utils.response import open_in_browser
class Udemyc(scrapy.Spider):
    name = 'udemy_coupons'
    headers = {
        #"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    	#"accept-encoding": "gzip, deflate, br",
        #"accept-language": "en-US,en;q=0.9",
       # "cache-control": "max-age=0",
       # "cookie": "__cfduid=d70e6f4389469eb641dfca5aa9e16ae771596457912; PHPSESSID=cgsi3eal56kcf73lj7j3s6p05l",
        #"sec-fetch-dest": "document",
       # "sec-fetch-mode": "navigate",
        #"sec-fetch-site": "same-origin",
       # "upgrade-insecure-requests": "1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = 'https://www.discudemy.com/search'

    def __init__(self):
    	with open('results.csv', 'w') as csv_file:
    		csv_file.write('course_name,coupon_link,coupon_date,coupon_description\n')

    def start_requests(self):
    	for page in range(0, 10):
    		yield scrapy.Request(url=self.url + '/' + str(page) + '/python.jsf', headers=self.headers, callback=self.parse)

    def parse(self, response):
        course_name = response.xpath("//a[@class='card-header']/text()").extract()
        coupon_link = response.xpath("//a[@class='card-header']/@href").extract()
        coupon_date = response.xpath("//span[@class='category']/div/text()").extract()
        coupon_description = response.xpath("//div[@class='description']/text()").extract()
        cd = [x for x in coupon_description if x != ' \n\t\t\t\t\n            ']
        i=0
        for x in course_name:
            items = {
                    'course_name': course_name[i],
                    'coupon_link': coupon_link[i],
                    'coupon_date': coupon_date[i],
                    'coupon_description': cd[i] 
                }

            with open('results.csv','a',encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=items.keys())
                writer.writerow(items)
            i=i+1

#run scraper
process = CrawlerProcess()
process.crawl(Udemyc)
process.start()