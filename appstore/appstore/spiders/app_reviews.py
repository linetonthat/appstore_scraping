import scrapy
import json
from urllib.parse import urlencode

class AppReviewsSpider(scrapy.Spider):
    name = 'app_reviews'
    token = '' #define your token here

    ref_root_url = "https://apps.apple.com/fr/app/"
    app_name = 'airvisual-air-quality-forecast'
    app_id = '1048912974' #AirVisual
    #app_name = 'sensio-air'
    #app_id = '1252417620' #SensioAir

    root_url = 'https://amp-api.apps.apple.com/v1/catalog/FR/apps/'

    # define request headers similar to headers used in the web browser
    headers =  {
        "Accept": "application/json",
        "Referer": ref_root_url+app_name+"/id"+ app_id,
        "Authorization": "Bearer "+token,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

    def start_requests(self):
        def parameters(offset):
            return {
                        "l":"fr-FR",
                        "offset": offset,
                        "platform":"web",
                        "additionalPlatforms":"appletv,ipad,iphone,mac"
                    }
        # define urls to scrape
        for i in range(34): # manual check done to identify the number of pages of reviews
            offset = str(i)+'0'
            url = self.root_url+self.app_id+'/reviews?'+ urlencode(parameters(offset))
            yield scrapy.Request(
                url=url,
                headers = self.headers
                )

    # parse responses
    def parse(self, response):
        if response is not None:
            json_response = json.loads(response.text)
            set_of_features = json_response['data']
            for features in set_of_features:
                d = dict()
                # if there is no developer response, this will cause a Key Error exception
                try:
                    d['review_id']=features['id']
                    d['rating']= features['attributes']['rating']
                    d['title']= features['attributes']['title']
                    d['review_date']= features['attributes']['date']
                    d['user_name']= features['attributes']['userName']
                    d['review']= features['attributes']['review']
                    d['response_id']= features['attributes']['developerResponse']['id']
                    d['dev_response']= features['attributes']['developerResponse']['body']
                    d['response_date']= features['attributes']['developerResponse']['modified']
                except KeyError:
                    pass
                yield d
