import scrapy
import datetime
from items import JumiaItem


class JumiaSpider(scrapy.Spider):
    name = "Jumia"
    start_urls = ["https://www.jumia.co.ke/phones-tablets/?page=1#catalog-listing"]
    allowed_domains = ["jumia.co.ke"]
    count = 1

    def parse(self, response):
        url = f"{self.start_urls[0]}"
        # settings = get_project_settings()
        yield scrapy.Request(url=url, callback=self.parse_items)
    
    def parse_items(self, response):
        items = JumiaItem()
        try:
            articles = response.xpath("//article[@class='prd _box _hvr']")

            newdata = {}
            for i, art in enumerate(articles):
                if i < 250:
                    newdata.update({i: self.parse_result(art)})
            items["inform"] = newdata
            yield items


            if self.count < 51:
                self.count += 1
                next_page = f"https://www.jumia.co.ke/phones-tablets/?page={self.count}#catalog-listing"
                yield response.follow(next_page, callback=self.parse_items)

        except Exception as err:
            print("\nEncountered an exception during execution")
            raise err

    def parse_result(self, art) -> dict:
        data = {}
        core = art.xpath(".//a[@class='core']")
        data["crawled_at"] = datetime.datetime.strftime(
            datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"
        )
        data["name"] = self.__safe_parsing(core.xpath("@data-name").get())
        data["href"] = self.__safe_parsing(core.xpath("@href").get())
        data["data-id"] = self.__safe_parsing(core.xpath("@data-id").get())
        data["brand"] = self.__safe_parsing(core.xpath("@data-brand").get())
        data["name2"] = self.__safe_parsing(core.xpath(".//div[@class='info']/h3/text()").get())
        data["price"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='prc']/text()").get())
        data["old_price"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='s-prc-w']/div/text()").get())
        data["discount"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='s-prc-w']/div[@class='bdg _dsct _sm']/text()").get())
        data["votes"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='rev']/text()").get())
        data["stars"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='rev']/div[@class='stars _s']/text()").get())
        data["image_url"] = self.__safe_parsing(core.xpath(".//div[@class='img-c']/img[@class='img']/@data-src").get())
        data["official_store"] = self.__safe_parsing(core.xpath(".//div[@class='info']/div[@class='bdg _mall _xs']/text()").get())

        return data

    def __safe_parsing(self, parsing) -> str:
        try:
            if isinstance(parsing, str):
                return parsing
            elif isinstance(parsing, scrapy.Selector):
                return parsing.get()
        except Exception:
            return None
