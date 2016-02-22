import scrapy

from retail_locations.items import RetailLocationsItem

class YellowPagesSpider(scrapy.Spider):
    
    name = "yellow_pages"
    allowed_domains = ["www.yellowpages.com",]
    
    cos = ["Urban Outfitters",]
    cos = [c.replace(" ", "+") for c in cos]
    
    us_states = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','GU','HI',
                 'ID','IL','IN','IA','KS','KY','LA','ME','MD','MH','MA','MI','FM','MN',
                 'MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','MP','OH','OK',
                 'OR','PW','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA',
                 'WV','WI','WY',]
    
    base_url = "http://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}"
    start_urls = []
    for co in cos:
        for state in us_states:
            start_urls.append(base_url.format(co, state))
    

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
