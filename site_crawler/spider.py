import scrapy

# pip install scrapy
# scrapy runspider -o items.csv -a site="www.randyleagowinds.com" spider.py
# scrapy runspider -o items.csv -a site="www.blueskoolrecords.com" spider.py

#this script generates a list of 404's on a given site


class BrokenLinksSpider(scrapy.Spider):
    http_user = ''
    http_pass = ''
    name = 'broken-link-checker'
    handle_httpstatus_list = [403, 404, 500]
    COOKIES_ENABLED = False
    download_timeout = 20

    #mf_blacklist = ['/documentation', '/ondemand'];
    #black_list = []
    #for url in mf_blacklist:
    #    url = 'http://www.randyleagowinds.com/'+ url
    #    black_list.append(url)
    

    #def __init__(self, site, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.start_urls = [site]
    #    self.DOMAIN = site.split('//')[1]

    def start_requests(self):
        urls = [
            #'http://www.blueskoolrecords.com',
            #'http://www.randyleagowinds.com',
            #'https://www.microfocus.com',
            'https://bellalash.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status in (403, 404, 500):
            item = dict()
            item['url'] = response.url
            item['prev_page'] = '';
            item['prev_href'] = '';
            item['prev_link_url'] = '';
            item['prev_link_text'] = '';
            item['prev_origin'] = '';
            item['status'] = '';

            if('prev_url') in response.meta:
                item['prev_page'] = response.meta['prev_url']
            if('prev_href') in response.meta:
                item['prev_link_url'] = response.meta['prev_href']
            if('prev_link_text') in response.meta:
                item['prev_link_text'] = response.meta['prev_link_text']
            item['status'] = response.status
            if('prev_origin') in response.meta:
                item['prev_origin'] = response.meta['prev_origin']

            yield item

        #elif response.url.startswith('http://www.blueskoolrecords.com'):
        #elif response.url.startswith('http://www.randyleagowinds.com'):
        #elif response.url.startswith('https://www.microfocus.com'):
        elif response.url.startswith('https://bellalash.com'):    
            for link in response.css('a, link[rel="alternate"]'):
                # use blacklist for page origin
                #if any(item in response.url for item in self.black_list):
                #    self.logger.debug('Skipping black listed url {} from {}'.format(response.url))
                #    continue

                href = link.xpath('@href').extract()
                text = link.xpath('text()').extract()
                if href:  # maybe should show an error if no href

                    if 'x-page-origin' in response.headers:
                        origin = response.headers['x-page-origin']
                    else:
                        origin = 'n/a'
                    yield response.follow(link, self.parse, meta={
                        #'prev_link_text': text,
                        'prev_link_text': '',
                        'link_on_site': href,
                        'url_with_bad_link': response.url,
                        'prev_origin': origin
                    })
