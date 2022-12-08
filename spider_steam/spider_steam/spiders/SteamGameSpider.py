import scrapy
from spider_steam.items import SpiderSteamItem


def strip_string(stri):
    return stri.strip()

def remake_price(price):
    return str(int(price) // 100)

def remake_platform(plat):
    return plat[13:]

class SteamgamespiderSpider(scrapy.Spider):
    name = 'SteamGameSpider'
    allowed_domains = ['store.steampowered.com']

    def start_requests(self):
        for page in range(1, 3):
            url = f'https://store.steampowered.com/search/?term=love&supportedlang=russian&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)
        for page in range(1, 3):
            url = f'https://store.steampowered.com/search/?term=death&supportedlang=russian&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)
        for page in range(1, 3):
            url = f'https://store.steampowered.com/search/?term=robots&supportedlang=russian&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.xpath('//div[contains(@id, "search_resultsRows")]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = SpiderSteamItem()
        name = response.xpath('//div[contains(@id, "appHubAppName_responsive")]/text()').extract()
        category = response.xpath('//div[@class="blockbg"]/a[position() >= 2]/text()').extract()
        review_count = response.xpath('//meta[contains(@itemprop, "reviewCount")]/@content').extract()
        review_mean = response.xpath('//div[@class="glance_ctn_responsive_left"]/div[contains(@id, "userReviews")]/div[contains(@itemprop, "aggregateRating")]/div/span[@class="game_review_summary positive"]/text()').extract()
        release_date = response.xpath('//div[@class="grid_content grid_date"]/text()').extract()
        price = response.xpath('//div[@class="game_purchase_action_bg"]/div/@data-price-final').extract()
        developer = response.xpath('//div[contains(@class, "grid_content") and (position() <= 2)]/a/text()').extract()
        tags = response.xpath('//div[contains(@class, "glance_tags popular_tags")]/a/text()').extract()
        platforms = response.xpath('//div[contains(@class, "game_area_purchase_platform") and (position() <= 2)]/span/@class').extract()
        items["game_name"] = ''.join(name).strip()
        items["category"] = '/'.join(category).strip()
        items["review_count"] = ''.join(review_count).strip()
        items["review_mean"] = ''.join(review_mean).strip()
        items["release_date"] = ''.join(release_date).strip()
        items["developer"] = ', '.join(developer).strip()
        items["price"] = ' '.join(map(remake_price, price)).strip()
        items["platforms"] = ', '.join(list(set(map(remake_platform, platforms)))).strip()
        items["tags"] = ', '.join(map(strip_string, tags)).strip()
        yield items
