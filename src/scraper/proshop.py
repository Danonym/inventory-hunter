from scraper.common import ScrapeResult, Scraper, ScraperFactory


class ProshopScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.head.find('meta', property='og:title')
        if tag:
            alert_content += tag['content'] + '\n' +'\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.find('button', class_='site-btn-addToBasket-lg')
        price_str = self.set_price(tag["data-price"]) 
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('script', type='application/ld+json')
        if tag and 'InStock' in tag.string:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class ProshopScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'proshop'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return ProshopScrapeResult
