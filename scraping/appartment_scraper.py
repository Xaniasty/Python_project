
from otodom_scraper import OtodomScraper
import json
from datetime import datetime
import unicodedata
from bs4 import BeautifulSoup

class ApartmentScraper(OtodomScraper):
    SEARCH_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska"

    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def if_error_set_nan(offer, *sentence):
        try:
            if len(sentence) <= 1:
                return offer.get(sentence[0])
            else:
                return offer.get(sentence[0]).get(sentence[1])
        except KeyError:
            return None
        except ValueError:
            return None
        
    def return_null():
        return None
        

    def _parse_apartment_offer_soup(self, soup):
        
        try:
            offer = json.loads(soup.find("script", id="__NEXT_DATA__").text)["props"]["pageProps"]["ad"]
        except AttributeError:
            print(f"\033[31m{offer}\033[0m")
            
            print("\033[31mBłądAtrybytu\033[0m")
            offer = json.loads(soup.find("script", id="__NEXT_DATA__"))["props"]["pageProps"]["ad"]
            
        offer_dict = {}
        
        offer_dict["id"] = offer.get("id")
        offer_dict["market"] = offer.get("market")
        offer_dict["publicId"] = offer.get("publicId")
        offer_dict["advertType"] = offer.get("advertType")
        offer_dict["createdAt"] = offer.get("createdAt")
        offer_dict["description"] = unicodedata.normalize("NFKC", BeautifulSoup(offer["description"], 'html.parser').text)
        offer_dict["exclusiveOffer"] = offer.get("exclusiveOffer")
        offer_dict["features"] = "|".join(offer.get("features"))
        offer_dict["area"] = offer.get("target", None).get("Area", None)
        offer_dict["Build_year"] = offer.get("target", None).get("Build_year", None) #self.if_error_set_nan(offer,"target","Build_Year") 
        offer_dict["Building_floors_num"] = offer.get("target", None).get("Building_floors_num", None)
        offer_dict["Floor_no"] = offer.get("target", None).get("Floor_no", None)[0]
        # offer_dict["Building_ownership"] = "|".join(offer["target"]["Building_ownership"])
        # offer_dict["Building_type"] = "|".join(offer["target"]["Building_type"])
        # offer_dict["Country"] = offer["target"]["Country"]
        # offer_dict["Extras_types"] = "|".join(offer["target"]["Extras_types"])
        # offer_dict["OfferType"] = offer["target"]["OfferType"]
        # offer_dict["Price"] = offer["target"]["Price"]
        # offer_dict["Price_per_m"] = offer["target"]["Price_per_m"]
        # offer_dict["ProperType"] = offer["target"]["ProperType"]
        # offer_dict["Province"] = offer["target"]["Province"]
        # offer_dict["Rent"] = offer["target"]["Rent"]
        # offer_dict["Rooms_num"] = "|".join(offer["target"]["Rooms_num"])
        # offer_dict["City"] = offer["location"]["address"]["city"]["name"]
        # offer_dict["Currency"] = offer.get("currency")
        # offer_dict["latitude"] = offer["location"]["coordinates"]["latitude"]
        # offer_dict["longitude"] = offer["location"]["coordinates"]["longitude"]
        offer_dict["scraping_date"] = str(datetime.now())
        print(offer_dict)
        return offer_dict



scraper = ApartmentScraper("Moja_nazwa")
all_urls = scraper.list_offers_urls_from_search_params()
offers = scraper.scrap_offers_from_urls(all_urls)
with open("offers.json", "w") as f:
    json.dump(offers, f, indent=4)


# url = "https://www.otodom.pl/pl/oferta/penthouse-luksusowe-2p-ak-poznan-lacina-54-m2-ID4mEjW"
# response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})
# soup = BeautifulSoup(response.text, 'html.parser')
# response

