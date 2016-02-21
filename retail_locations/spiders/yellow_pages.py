import scrapy

from retail_locations.items import RetailLocationsItem

class YellowPagesSpider(scrapy.Spider):
    name = "yellow_pages"
    allowed_domains = ["www.yellowpages.com",]
    start_urls = ["http://www.yellowpages.com/search?search_terms=Urban+Outfitters&geo_location_terms=CA",]

    def parse(self, response):

        items = response.css('.info')
        for item in items:
            business_name = item.xpath('.//a/text()').extract()[0]
            full_address = item.css('.info-section')
            try:
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
            except:
                print("bad row: {0}".format(business_name))


        next_page = response.css('.next').xpath('@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            # quit after 3 pages
            if int(url[-1]) <= 3:
                yield scrapy.Request(url, self.parse)
