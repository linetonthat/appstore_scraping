import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    start_urls = [
        'https://www.amazon.fr/Hatteker-Tondeuse-%C3%A9lectrique-pr%C3%A9cision-waterproof/product-reviews/B07W1HM28N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    ]

    def parse(self, response):
        # we define a dictionary to be passed to .translate() to remove '\r\n\t' in unicode text
        trans_table = {ord(c): None for c in u'\r\n\t'}
        for review in response.css("div.a-section.review.aok-relative"):
            yield {
                'rating' : review.css("span.a-icon-alt::text").get().split(" sur")[0].replace(",","."),
                'date' :  review.css("span.a-size-base.a-color-secondary.review-date::text").get().split("le ")[1],
                'day' : review.css("span.a-size-base.a-color-secondary.review-date::text").get().split("le ")[1].split(' ')[0],
                'month' : review.css("span.a-size-base.a-color-secondary.review-date::text").get().split("le ")[1].split(' ')[1],
                'year' : review.css("span.a-size-base.a-color-secondary.review-date::text").get().split("le ")[1].split(' ')[2],
                'review_title' : review.css("a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold span::text").get(),
                'review_text': review.css('span.a-size-base.review-text.review-text-content span::text').get().strip().translate(trans_table),
                'username' : review.css("span.a-profile-name::text").get(),
                'verified': review.css('span.a-size-mini.a-color-state.a-text-bold::text').get()
            }
        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
