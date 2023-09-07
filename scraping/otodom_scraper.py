import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin


class OtodomScraper:
    OFFER_BASE_URL = "https://www.otodom.pl/pl/oferta/"
    SEARCH_URL = None
    

    def __init__(self, name):
        self.name = name

    @staticmethod
    def _make_request(url, headers, params=None):
        response = requests.get(url, headers=headers, params=params)
        return response

    @staticmethod
    def _make_soup(response):
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    def scrap_offers_from_urls(self, urls):
        print("rozpoczynam pobieranie url dla ofert")
        ofers_list = []
        for i,url in enumerate(urls):
            print(f"     Tworzę ofertę nr: {i}")
            print(f"**wykonuje request oferty**{url}")
            response = self._make_request(url, headers=self._generate_headers())
            soup = self._make_soup(response)
            ofert_dict = self._parse_apartment_offer_soup(soup)
            ofers_list.append(ofert_dict)
        print("Zracam listę linków do scrapingu")
        return ofers_list

    @staticmethod
    def _generate_headers():
        
        with open(r"conf\headers.json", "r") as f:
            user_agent = json.load(f)[0]
        headers = {'User-Agent': user_agent}
        
        return headers
    
    def _get_offer_urls_from_one_page(self, otodom_search_offers_soup):
        print("rozpoczynam odczytywanie wszystkich linków do ofert (typ: slug)")
        offers_json = json.loads(
            otodom_search_offers_soup.find_all("script", {"type": "application/json"})[0].text)
        offers_list = offers_json["props"]["pageProps"]["data"]["searchAds"]["items"]
        url_offers_list = [urljoin(self.OFFER_BASE_URL, offer['slug']) for offer in offers_list]
        print("Zwracam listę linków slug do ofert")
        return url_offers_list

    def list_offers_urls_from_search_params(self):
        all_urls_list = []
        print("Zaczynam tworzenie linków do poszczególnych ofert")
        with open(r"conf\apartment_filters.json", "r") as f:
            data = json.load(f)
            search_params = data['filters']
            n_pages = data['pages_number']

        for page_number in range(1, n_pages + 1):
            print(f"Pobieram url ze strony nr {page_number}")
            search_params['page'] = page_number
            print("**wykonuje request strony**")
            offers_page_response = self._make_request(self.SEARCH_URL,
                                                      self._generate_headers(), search_params)
            print("Wykonuje soup strony")
            offers_page_soup = self._make_soup(offers_page_response)
            print("Pobieram linki z soup strony")
            offers_page_urls = self._get_offer_urls_from_one_page(offers_page_soup)
            all_urls_list.extend(offers_page_urls)
        
        with open('LINKS', 'w') as f:
                for link in all_urls_list:
                    f.write(f"{link}\n")

        print("Kończę tworzenie listy")

        return all_urls_list


    
        #requestujemy jedną stronę
        #parsujemy zupę z jednej strony
        #dodajemy urle z jednej strony do listy wszystkich urli

