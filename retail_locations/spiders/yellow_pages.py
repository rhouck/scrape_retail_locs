import scrapy

from retail_locations.items import RetailLocationsItem

class YellowPagesSpider(scrapy.Spider):
    name = "yellow_pages"
    allowed_domains = ["http://www.yellowpages.com"]
    start_urls = ["http://www.yellowpages.com/search?search_terms=Urban+Outfitters&geo_location_terms=VT",]

    def parse(self, response):

        items = response.css('.info')
        for item in items:
            business_name = item.xpath('.//a/text()').extract()[0]
            full_address = item.css('.info-section')
            street_address = full_address.xpath('.//span[contains(@itemprop, "streetAddress")]/text()').extract()[0]
            address_locality = full_address.xpath('.//span[contains(@itemprop, "addressLocality")]/text()').extract()[0]
            address_region = full_address.xpath('.//span[contains(@itemprop, "addressRegion")]/text()').extract()[0]
            postal_code = full_address.xpath('.//span[contains(@itemprop, "postalCode")]/text()').extract()[0]
            
            item = RetailLocationsItem()
            item['business_name'] = business_name
            item['street_address'] = street_address
            item['address_locality'] = address_locality
            item['address_region'] = address_region
            item['postal_code'] = postal_code
            yield item
            #       filename = response.url.split("/")[-2]
            # with open('data/' + filename, 'wb') as f:
            # 	f.write(response.body)
