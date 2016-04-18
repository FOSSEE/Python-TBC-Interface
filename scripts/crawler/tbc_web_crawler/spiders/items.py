import scrapy


class TbcErrorItems(scrapy.Item):


	chapter_name = scrapy.Field()
	chapter_urls = scrapy.Field()
	completed_book_urls = scrapy.Field()
	number_of_errors = scrapy.Field()
	error_messages = scrapy.Field()
	
	

class TbcBrokenItems(scrapy.Item):
	
	broken_url = scrapy.Field()
	broken_status = scrapy.Field()
