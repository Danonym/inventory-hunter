from scraper.common import ScrapeResult, Scraper, ScraperFactory


class KomplettScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.head.find('span', itemprop='manufacturer')
        if tag:
            alert_content += tag.string + '\n' +'\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.find('meta', itemprop='price')
        price_str = self.set_price(tag["content"]) # tag["content"]
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('span', class_='stockstatus-stock-details')
        if tag and 'stk. på lager' in tag.string:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class KomplettScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'komplett'

    @staticmethod
    def get_driver_type():
        return 'selenium'

    @staticmethod
    def get_result_type():
        return KomplettScrapeResult
