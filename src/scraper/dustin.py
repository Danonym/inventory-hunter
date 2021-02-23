from scraper.common import ScrapeResult, Scraper, ScraperFactory


class DustinScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('meta', itemprop='name')
        if tag:
            alert_content += tag['content'] + '\n' +'\n'
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
        tag = self.soup.body.find('div', class_='c-icon-text c-icon-text--availability')#, title='Kan sendes omgående'
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class DustinScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'dustin'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return DustinScrapeResult
