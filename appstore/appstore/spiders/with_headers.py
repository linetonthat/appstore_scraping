import scrapy
import json
from urllib.parse import urlencode

class WithHeadersSpider(scrapy.Spider):
    name = 'with_headers'
    token = '' # define your token here

    # found after decoding the URL of the request
    params = {
                "platform" : "web",
                "additionalPlatforms":"appletv,ipad,iphone,mac",
                "extend":"description,developerInfo,editorialVideo,eula,fileSizeByDevice,messagesScreenshots,privacyPolicyUrl,privacyPolicyText,promotionalText,screenshotsByType,supportURLForLanguage,versionHistory,videoPreviewsByType,websiteUrl",
                "include":"genres,developer,reviews,merchandised-in-apps,customers-also-bought-apps,developer-other-apps,app-bundles,top-in-apps,eula",
                "l":"fr-fr"
            }

    root_url = 'https://amp-api.apps.apple.com/v1/catalog/FR/apps/'

    # ids found on the url of identified apps related to air quality on the appstore for France
    app_ids = {
                'sensio' : '1252417620',
                'breezometer' : '989623380'
                }
    # NameError: name 'root_url' is not defined
    #start_urls = [root_url+v+'?'+ urlencode(params) for v in app_ids.values()]

    # define the list of urls to crawl, based on the app ids
    start_urls = []
    for v in app_ids.values():
        start_urls.append(root_url+v+'?'+ urlencode(params))

    # define request headers similar to headers used in the web browser
    #and REFRESH pages if needed before launching the spider
    headers = {
                'Accept': 'application/json',
                'Referer': 'https://apps.apple.com/fr/app/sensio-air-allergy-tracker/id1252417620',
                'Authorization': 'Bearer '+token,
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    # define crawler's entry points
    def start_requests(self):
        for url in self.start_urls:
            # make HTTP GET request to url
            yield scrapy.Request(
                url=url,
                headers = self.headers
                )

    # parse responses
    def parse(self, response):
        json_response = json.loads(response.text)
        features = json_response['data']
        yield {
                'app2_id': features[0]['id'],
                'href': features[0]['href'],
                'organization' : features[0]['attributes']['artistName'],
                'user_rating_value' : features[0]['attributes']['userRating']['value'],
                'user_rating_count' : features[0]['attributes']['userRating']['ratingCount'],
                'user_rating_count_list' : features[0]['attributes']['userRating']['ratingCountList'],
                # also check 'contentRatingsBySystem'
                'no_versions_in_history': len(features[0]['attributes']['platformAttributes']['ios']['versionHistory']), # check what's relevant regarding version history
                'genre' : features[0]['relationships']['genres']['data'][0]['attributes']['name'],
                'description' : features[0]['attributes']['platformAttributes']['ios']['description']
                }
