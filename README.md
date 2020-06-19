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
For the time being, I've been busy getting a better understanding of:
*  how to navigate html response using css attributes (when the response is in html).
*  how to "translate" unicode text with '\r\n\t' and leading and trailing whitespaces
** 
understand dynamic requests
