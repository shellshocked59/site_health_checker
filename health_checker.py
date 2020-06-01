import urllib 
from lxml import html
from urllib import urlopen
from bs4 import BeautifulSoup

class HealthChecker(object):
	def __init__(self):
		self.site = 'http://bellalash.com'
		webpage = urlopen(self.site)
		self.soup = BeautifulSoup(webpage, "lxml")
		#self.page = html.fromstring(urllib.urlopen(self.site).read())

		self.test_data = dict()
		self.test_data['success'] = 1;
		self.test_data['messages'] = [];

	def runAll(self):
		self.meta_tags()
		self.fav_icon()
		self.sitemap()
		self.analytics()
		self.test_https()


		self.report_errors()

	def report_errors(self):
		if(self.test_data['success'] == 1):
			print 'No errors found on site '+self.site
		else:
			print 'Errors were found on the site'
			print str(len(self.test_data['messages']))+' errors are listed below:'
			for error in self.test_data['messages']:
				print '-- '+error;

	def add_error(self, message):
		self.test_data['success'] = 0
		self.test_data['messages'].append(message)

	def url_exists(self, url, message = ''):
		if not message:
			message = url+' does not exist'

		webpage = urlopen(url)
		if webpage.getcode() == 200:
			return 1
		else:
			self.add_error(message)
			return 0

	def meta_tags(self):
		#get and format all meta tags
		all_meta = dict()
		for meta in self.soup.find_all("meta") :
			single_meta = dict()
			single_meta['name'] = meta.get('name')
			#use property as name if not available
			if(single_meta['name'] == None):
				single_meta['name'] = meta.get('property')

			single_meta['content'] = meta.get('content')
			all_meta[single_meta['name']] = single_meta['content']

		#test all meta tags
		#robots enabled
		if 'robots' in all_meta:
			if 'index' not in all_meta['robots']:
				self.add_error('Robots meta tag makes page not indexable')
		else:
			self.add_error('Robots meta tag is missing')
		#description
		if 'description' not in all_meta:
			self.add_error('Description meta tag is missing')
		#viewport
		if 'viewport' not in all_meta:
			self.add_error('Viewport meta tag is missing')

		#title
		title = self.soup.select("title")
		if title == []:
			self.add_error('Title tag does not exist')
		elif self.soup.find('title').get_text == '':
			self.add_error('Title tag exists, but is empty')

		#charset
		charset_found = 0;
		for meta in self.soup.find_all("meta") :
			if meta.get('charset') != None:
				charset_found += 1;
		if charset_found == 0:
			self.add_error('Charset meta tag not found')
		elif charset_found > 1:
			self.add_error('Multiple charset meta tags were found on page')
			
	#test to see if favicon exists
	def fav_icon(self):
		self.url_exists(self.site+'/favicon.ico')

	#test to see if sitemap exists
	#TODO test if sitemap is valid XML
	#TODO test if sitemap links ALL exist
	def sitemap(self):
		self.url_exists(self.site+'/sitemap.xml')
		#TODO do all links inside the sitemap actually exist??

	#test to see if gtm.js exists
	def analytics(self):
		full_html = self.soup.get_text()
		if 'gtm.js' not in full_html:
			self.add_error('GTM.js not found on page')

	#test to see if site is available via https
	#TODO should add certificate validation
	def test_https(self):
		https = self.site.replace('http://', 'https://')
		webpage = urlopen(https)
		if webpage.getcode() != 200:
			self.add_error('site not available at https')

    #favicons
    #sitemap.xml
    #page title
    #google analytics
    #console errors
    #404's
    #improper image sizes
    #useage of retina images
    #google tags
    #http/https


#runs class
hc = HealthChecker()
hc.runAll()