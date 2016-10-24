import scrapy
from .items import TbcErrorItems, TbcBrokenItems
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request

import os, json

if os.path.isfile('items.json'):
	os.remove('items.json')
else:
	pass
	
class TbcSpider(scrapy.Spider):

	name = "tbc_spider"  # Name of the crawler. Use this name when crawling from the terminal, for eg - scrapy crawl tbc_spider
	
	start_urls = ["http://tbc-python.fossee.aero.iitb.ac.in/completed-books/"]
	handle_httpstatus_list = [404, 500, 502] # A list containing HTTP error codes.
	
	def parse(self,response):
		""" This function looks for book links and returns the url"""
		
		for book_link in response.xpath('//a[contains(@href,"book-details")]/@href').extract():
			""" Searches for links with "book-details" in it """
		
			first_base_url = get_base_url(response)
			first_relative_url = urljoin_rfc(first_base_url,book_link)
			"""creates a url to be returned to the next function."""
		
			yield scrapy.Request(first_relative_url,callback=self.parse_book_contents)
		
			
			
	def parse_book_contents(self, response):
		
		""" This function looks for chapter links through each book link and returns the url"""
	
		for chapter_link in response.xpath ('//a[contains(@href,"convert-notebook")]/@href').extract():
			""" Searches for chapters in each book list"""
			second_base_url = get_base_url(response).split('/book-details')[0]
			second_relative_url = urljoin_rfc(second_base_url,chapter_link)
			"""creates a url to be returned to the next function."""
			
			yield scrapy.Request(second_relative_url,callback=self.parse_chapter_details)
			
			

	def parse_chapter_details(self, response):
		 
		if not response.xpath('//h1/text()').extract():
			chapter_details = [response.url]
		else:
			chapter_details = response.xpath('//h1/text()').extract()

		
		error_tag = response.xpath('//div[@class="output_subarea output_text output_error"]') 
		error_list = [error_notifications for error_notifications \
		              in response.xpath \
		              ('//div[@class="output_subarea output_text output_error"]/span/text()').extract()]

		if response.status in self.handle_httpstatus_list:
			broken_items = TbcBrokenItems()
			broken_items['broken_url'] = response.url
			broken_items['broken_status'] = response.status
			yield broken_items
		else:
			if len(error_tag) != 0:
				items = TbcErrorItems()
				items ['chapter_name'] = chapter_details[0]
				items ['chapter_urls'] = response.url
				items ['number_of_errors'] = len (error_tag)
				#items ['completed_book_urls'] = response.request.headers.get('Referer', None)
				#items ['error_messages'] = error_list
				yield items
				
