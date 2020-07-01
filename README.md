# Appstore scraping

Working on a project for better awareness of air quality, I'm interested in knowing what the main apps related to this field
are like and what are the feedback from their users. In order to have access to numerous reviews from the app store, web scraping is the way to go!
After some research, it seems that Scrapy (https://doc.scrapy.org/en/latest/index.html) should help me scrape the data needed for my analysis. Scrapy allows for gently scraping the web by creating spiders and sending them out to crawl the app stores.

---
## Take-aways from this project

### Learned how to use Scrapy:
 *  How to navigate html responses using css attributes - [cf. reviews_to_dict.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/reviews_to_dict.py)
     - How to deal with multiple classes in css tags to access the right level of data
 *  How to "translate" unicode text with '\r\n\t' and leading and trailing whitespaces - [cf. reviews_to_dict.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/reviews_to_dict.py)
     - Used the .translate() function with the following dictionary: trans_table = {ord(c): None for c in u'\r\n\t'}
     - Used the .strip() function to get rid of leading and trailing whitespaces
 * Understand dynamic requests: when the URL has a '#', the server does not care about what's after this symbol. The client (web browser) deals with it. Then, I went to the Developer's tools to find out where I could identify the "real" url I would need for scraping. Learned about cURL!
     - How to transform the cURL of into a request that can be handled by Scrapy (done manually at first, and discovered it can also be done using https://michael-shub.github.io/curl2scrapy/: thank you!!)
 * How to build a spider where the requests have headers and deal with responses in JSON format - [cf. with_headers.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/with_headers.py)
     - How to easily visualize the tree structure of a JSON format (thanks to: https://jsonformatter.org/json-viewer)
     - How to decode parameters from a URL in order to tidy up the code (thanks to: https://meyerweb.com/eric/tools/dencoder/)
 * How to configure the settings of my spiders to ensure gentle scraping - [cf. settings.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/settings.py)
     - Followed the guidance from Scrapy blog (https://blog.scrapinghub.com/2016/08/25/how-to-crawl-the-web-politely-with-scrapy) and updated my settings.
     - Disabled #HTTPCACHE_ENABLED = True, as some pages were not reached using a spider, while they could be fetched using the same request via scrapy shell.

---
### Built a spider to scrape specific features of apps on the appstore related to air quality - using SelectorList in CSS
* Identify relevant apps 
   - (so far, couldn't find an app search menu outside the appstore app...)
   - Not sure, it could be automated, after reading robots.txt from Google store and App store, since I've read "Disallow: /store/search*" and "Disallow: /work/search". Need to check on that!
   - Read about factors that most affect app ranking in the appstore (https://www.mobiloud.com/blog/factors-really-impact-app-store-ranking/): app's title, targeted keywords, number of downloads, and user ratings. I'm surprised that usage is not part of these factors. 
* Build a spider to collect app features and description across a range of apps - [cf. app_features.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/app_features.py)
   - Using a list of landing pages
   - Dealing with Exceptions as some features are not present for all apps.

---
### Built a spider to scrape all the app reviews on the appstore from a given country - using dynamic requests with headers and token (JSON response)
* Built a spider to collect reviews for a specific app (app id and app name are required) - [cf. app_reviews.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/app_reviews.py)
    - Understood how reviews are loaded, and how to reproduce this loading using a spider. Reviews are loaded 10 by 10 when scrolling down in the web browser. Found a third url to use. This url is specific to reviews, and it's the best url to use for review scraping! 
    - Looped on the review pages to define the scraping requests.
    - Checked what's the best way to collect data from fields that do not exist for all items (e.g. response from the developer): Used handling exceptions (KeyError).
    - Review app_review spider to build a loop that stops automatically when there is no more page to scrape (request launched within the parse function and callback of the parse function).
    
---
### Built a simple spider to scrape all the reviews on Amazon French website -  using SelectorList in CSS
 * Build a "side" spider to scrape reviews for a given product on Amazon French website - [cf. amazon_reviews.py](https://github.com/linetonthat/appstore_scraping/blob/master/appstore/appstore/spiders/amazon_reviews.py)
   - Recursively follow the link to the next page.

---
## Future Work
* Scrape version history to better understand priorization of feature releases
* Scrape similarly from Google Play store. NB: App ranking are assessed on a different way apparently (https://thementalclub.com/rank-app-play-store-ranking-algorithm-26708).
   
