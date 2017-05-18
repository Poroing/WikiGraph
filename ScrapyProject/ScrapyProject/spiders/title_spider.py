import scrapy
import re
import functools

class TitleSpider(scrapy.Spider):
    name = 'title'

    urls = ['http://awoiaf.westeros.org/index.php/Main_Page']

    other_aticle_xpath = '''//a[
        starts-with(@href, \'/index.php/\')
        and not(contains(@href, \':\'))]/@href'''

    def start_requests(self):
        callback = functools.partial(self.parse, 'Main_Page')
        yield scrapy.Request(
            url='http://awoiaf.westeros.org/index.php/Main_Page',
            callback=callback)

    def parse(self, title, response):
        links = set()

        for other_aticle in response.xpath(TitleSpider.other_aticle_xpath).extract():
            other_aticle_title = self.getTitleOfLinkIfArticle(other_aticle)

            links.add(other_aticle_title)

            callback = functools.partial(self.parse, other_aticle_title)
            yield scrapy.Request(response.urljoin(other_aticle), callback=callback)

        links.discard(title)

        yield { title: list(links) }

    def getTitleOfResponseIfAny(self, response):
        titles = response.xpath('//title/text()').re(r'(.*) - A Wiki of Ice and Fire')
        if titles == []:
            return
        return titles[0]

    def urlIsArticle(self, url):
        return re.match(r'.*/index.php/[^:]+', url) is not None

    def getTitleOfLinkIfArticle(self, url):
        if not self.urlIsArticle(url):
            return None
        match = re.match(r'.*/index.php/([^:#]+).*', url) 
        return match.group(1)
