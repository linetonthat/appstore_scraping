import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews_to_dict"
    start_urls = [
        'https://apps.apple.com/fr/app/airvisual-qualit%C3%A9-de-lair/id1048912974', # AirVisual | Qualité de l'Air
    ]

    def parse(self, response):
        # we define a dictionary to be passed to .translate() to remove '\r\n\t' in unicode text
        trans_table = {ord(c): None for c in u'\r\n\t'}
        for review in response.css("div.we-customer-review.lockup.ember-view"):
            yield {
                'username' : review.css("span.we-truncate.we-truncate--single-line.ember-view.we-customer-review__user::text").get().strip().translate(trans_table), #OK
                'date' :  review.css("time.we-customer-review__date::text").get(), #OK
                'title' : review.css("h3.we-truncate.we-truncate--single-line.ember-view.we-customer-review__title::text").get(), #OK
                'text' : review.css("blockquote.we-truncate.we-truncate--multi-line.we-truncate--interactive.ember-view.we-customer-review__body p::text").get().strip().translate(trans_table),

            }
