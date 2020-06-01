import scrapy
import os
import sys

#this script generates a CSV of valid links on a given site

# pip install scrapy
# scrapy runspider -o map.csv -a site="www.randyleagowinds.com" mapper.py

''' Used to map all the pages on the site (software or microfocus.com) that return 200 '''


class LinksSpider(scrapy.Spider):
    http_user = 'pnx'
    http_pass = 'nolooking'
    name = 'site-mapper'
    COOKIES_ENABLED = False
    download_timeout = 20

    black_list = []
    #result = os.popen("curl https://www.microfocus.com/robots.txt").read()
    #result_data_set = set()                
    #for line in result.split("\n"):                              
        #if line.startswith('Noindex'):    #adding Noindex url in the set            
            #result_data_set.add(line.split(': ')[1].split(' ')[0])

    #def __init__(self, site, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.start_urls = [site]
    #    self.DOMAIN = site.split('//')[1]
    #    print(self.DOMAIN)
    #    print(self.start_urls)   

    def start_requests(self):
        urls = [
            'http://www.blueskoolrecords.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        if response.status is 200:
            ignored_urls = set()
            item = dict()            
            #if any(text in response.url for text in self.result_data_set):
            if 'X-Robots-Tag' in response.headers:
                test = str(response.headers['X-Robots-Tag'])
                if 'noindex' in test:                                
                    ignored_urls.add(response.url)
            else:                
                item['url'] = response.url
                item['status'] = response.status
                if 'x-page-origin' in response.headers:
                    item['origin'] = response.headers['x-page-origin']
                else:
                    item['origin'] = 'n/a'
                updated_at = response.xpath('//meta/@updated_at').extract() #get the updated at from the meta tag               
                if updated_at:
                    mod_date = updated_at[0].replace("/","-")
                    if mod_date:                        
                        item['updated_at'] =  mod_date
                    else:                        
                        item['updated_at'] =  '2019-03-01'
                else:
                    item['updated_at'] =  '2019-03-01'
            yield item            

        if response.url.startswith('http://www.blueskoolrecords.com/'):

            for link in response.css('a, link[rel="alternate"]'):
                href = link.xpath('@href').extract()                                               
                if href:
                    if any(item in href[0] for item in self.black_list):
                        continue                                       
                    yield response.follow(link, self.parse)                                                           


