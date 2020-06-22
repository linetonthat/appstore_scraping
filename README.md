# Appstore scraping

Working on a project for better awareness of air quality, I was interested in knowing what the main apps related to this field
were like. I'd like to (partially) answer the following questions:
* What apps are there?
* What are their main features?
* How are they rated?
* What are users looking for when using those apps?
* What expectations are not currently met?
* How do these apps work? Is there a classification for such apps?

After some research, it seems that Scrapy (https://doc.scrapy.org/en/latest/index.html) should help me scrape the data needed for my analysis.

Basically, Scrapy allows for gently scraping the web, which is what I'm intended here, by creating spiders and sending them out to crawl the app stores.

---
## So far: Learned about:
*  How to navigate html responses using css attributes.
    - How to deal with multiple classes in css tags to access the right level of data
*  How to "translate" unicode text with '\r\n\t' and leading and trailing whitespaces
    - Used the .translate() function with the following dictionary: trans_table = {ord(c): None for c in u'\r\n\t'}
    - Used the .strip() function to get rid of leading and trailing whitespaces
* Understand dynamic requests: when the URL has a '#', the server does not care about what's after this symbol. The client (web browser) deals with it. Then, I went to the Developer's tools to find out where I could identify the "real" url I would need for scraping. Learned about cURL!
    - How to transform the cURL of into a request that can be handled by Scrapy (done manually at first, and discovered it can also be done using https://michael-shub.github.io/curl2scrapy/: thank you!!)
* How to build a spider where the requests have headers and deal with responses in JSON format
    - How to easily visualize the tree structure of a JSON format (thanks to: https://jsonformatter.org/json-viewer)
    - How to decode parameters from a URL in order to tidy up the code (thanks to: https://meyerweb.com/eric/tools/dencoder/)
---
## On-going activities:

* Review the settings of my spiders to ensure gentle scraping (so far, I've been selecting pages with limited amount of data to scrape on purpose) :
    - Followed the guidance from Scrapy blog (https://blog.scrapinghub.com/2016/08/25/how-to-crawl-the-web-politely-with-scrapy) and updated my settings.
* Identify relevant apps (so far, couldn't find an app search menu outside the appstore app...)
    - Not sure, it could be automated, after reading robots.txt from Google store and App store, since I've read "Disallow: /store/search*" and "Disallow: /work/search". Need to checko on that!
    - Read about factors that most affect app ranking in the appstore (https://www.mobiloud.com/blog/factors-really-impact-app-store-ranking/): app's title, targeted keywords, number of downloads, and user ratings. I'm surprised that usage is not part of these factors. Should maybe check other resources. Need to do the same for the Play store: Should start with: https://thementalclub.com/rank-app-play-store-ranking-algorithm-26708.
* Build two distinct spiders:
    1. One to collect app features and description across a range of apps (using landing page to incude app ranking in its category, html response)
    2. One to collect reviews for a specific app (using json response for full reviews):
        - Check how to collect data from fields that do not exist for all items.

---
## Next steps:

* Investigate "live" apps: Are apps still maintained? Downloaded?
* Have a look at the review texts (strange feeling when reading some of them)
* Investigate how to automate data extraction from text reviews
