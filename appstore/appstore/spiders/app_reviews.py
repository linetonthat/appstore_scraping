import scrapy
import json
from urllib.parse import urlencode

class AppReviewsSpider(scrapy.Spider):
    name = 'app_reviews_v6'
    # define token used in web browser on the appstore
    token = ''
    # define app parameters (name and id)
    app_name = 'airvisual-air-quality-forecast'
    app_id = '1048912974' #AirVisual
    # define appstore country
    country = 'fr'
    # define starting parameters for page crawling
    url = ''
    offset = 32 # 1 offset corresponds to 10 reviews
    # define a function to generate request headers similar to headers used in the web browser
    def gen_headers(self):
        ref_root_url = lambda c : "https://apps.apple.com/"+c+"/app/"
        return  {
            "Accept": "application/json",
            "Referer": ref_root_url(self.country)+self.app_name+"/id"+ self.app_id,
            "Authorization": "Bearer "+self.token,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
    # define a function to generate a url based on offset
    def gen_url(self):
        parameters = {
                    "l":"fr-FR",
                    "offset": str(self.offset)+'0',
                    "platform":"web",
                    "additionalPlatforms":"appletv,ipad,iphone,mac"
                }
        root_url = lambda c : "https://amp-api.apps.apple.com/v1/catalog/"+c+"/apps/"
        return root_url(self.country)+self.app_id+'/reviews?'+ urlencode(parameters)
    # define the starting url using headers in the request
    def start_requests(self):
        self.url = self.gen_url()
        yield scrapy.Request(url=self.url,headers = self.gen_headers())
    # parse responses and add new request (following 10 reviews)
    def parse(self, response):
        # test if there is a response from the request made, else exit the function
        if response is not None:
            # load response text as json
            json_response = json.loads(response.text)
            set_of_features = json_response['data']
            for features in set_of_features:
                d = dict()
                # if there is no developer response, this will cause a Key Error exception
                try:
                    d['url'] = self.url
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
            # define new page to be scraped
            self.offset +=  1
            self.url = self.gen_url()
            #next_page = self.url
            next_page = response.urljoin(self.url)
            yield scrapy.Request(next_page, headers = self.gen_headers(), callback=self.parse)
