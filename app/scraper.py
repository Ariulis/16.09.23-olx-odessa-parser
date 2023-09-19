from time import sleep
from random import uniform


from misc import URL, logger, HEADERS


class OLXParser:
    ad_id_list = []

    def __init__(self, session, proxy: dict) -> None:
        self.session = session
        self.proxy = proxy

    def get_html(self, url):
        try:
            response = self.session.get(
                url,
                headers=HEADERS,
                proxies=self.proxy,
                timeout=5
            )
        except Exception as e:
            logger.exception(e)
        else:
            if response.ok:
                logger.info(f'Connection is success. Url: {url}')
                return response.html
            return response.status_code

    @staticmethod
    def parse_link(link):
        return link.split('.')[0].split('-')[-1]

    # def is_private(self, url):
    #     html = self.get_html(url)
    #     is_private = html.xpath(
    #         '/html/body/div/div[2]/div[3]/div[3]/div[1]/div[2]/ul/li[1]/p/span',
    #         first=True
    #     ).text

    #     return is_private == 'Приватна особа'

    def get_data(self):
        html = self.get_html(URL)

        articles = html.find('[data-cy="l-card"]')

        new_articles_data = []

        for article in articles[:10]:
            link = article.find('a', first=True).attrs['href']
            parse_link = self.parse_link(link)

            # if parse_link not in self.ad_id_list and self.is_private(f'https://www.olx.ua{link}'):

            if parse_link not in self.ad_id_list:
                self.ad_id_list.append(parse_link)

                title = article.find('[data-cy="l-card"] h6', first=True).text
                img = article.find(
                    '[data-cy="l-card"] img', first=True).attrs['src']

                article_dict = {
                    'link': f'https://www.olx.ua{link}',
                    'title': title,
                    'img': img
                }

                new_articles_data.append(article_dict)

                time = uniform(1, 3)
                sleep(time)

        return new_articles_data

    def get_all(self):
        return self.get_data()
