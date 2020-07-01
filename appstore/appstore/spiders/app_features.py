import scrapy
import collections


class AppFeaturesSpider(scrapy.Spider):
    name = "app_features"

    start_urls = [
        'https://apps.apple.com/fr/app/airvisual-air-quality-forecast/id1048912974', #AirVisual Air Quality Forecast
        'https://apps.apple.com/fr/app/sensio-air-allergy-tracker/id1252417620', # sensio
        'https://apps.apple.com/fr/app/plume-air-report-pollution/id950289243', # Plume air report
        'https://apps.apple.com/fr/app/air-to-go-qualit%C3%A9-de-lair/id1155558364', #AirToGo Auvergne Rhône-Alpes
        'https://apps.apple.com/fr/app/airly/id1283400152', # Airly
        'https://apps.apple.com/fr/app/pollen/id515301928', #pollen
        'https://apps.apple.com/fr/app/breezometer-air-quality-index/id989623380' # breezometer
    ]

    def parse(self, response):
        # we define a dictionary to be passed to .translate() to remove '\r\n\t' in unicode text
        trans_table = {ord(c): None for c in u'\r\n\t'}
        # define how the items of the Selector List will be parsed and preprocessed
        css_location = lambda sel_lst, cl_loc : sel_lst.css(cl_loc).get().strip().translate(trans_table)
        # define what are the features of interest in an ordered dictionary
        feat_dict = collections.OrderedDict(
                                [('title' ,"h1.product-header__title.app-header__title::text"),
                                ('subtitle', "h2.product-header__subtitle.app-header__subtitle::text"),
                                ('identity', "h2.product-header__identity.app-header__identity a::text"),
                                ('price' , "li.inline-list__item.inline-list__item--bulleted.app-header__list__item--price::text"),
                                ('ranking', "li.inline-list__item::text"),
                                ('ratings','figcaption.we-rating-count.star-rating__count::text')
                                ]
                            )
        # parse selected items
        if response is not None:
            app_d = dict()
            # parse features
            for set_of_features in response.css("header.product-header.app-header.product-header--padded-start"):
                for k, v in feat_dict.items():
                    if k == 'ranking':
                        try:
                            ranking = css_location(set_of_features, v).split(" en ")
                            app_d['rank'] = ranking[0][3:]
                            app_d['category'] = ranking[1]
                        except (AttributeError, IndexError):
                            pass
                    elif k == 'ratings':
                        try:
                            ratings = css_location(set_of_features, v).split(", ")
                            app_d['overall_rating'] = ratings[0]
                            no_of_ratings = ratings[1].split('\xa0')
                            app_d['no_of_ratings'] = no_of_ratings[0]
                            if len(no_of_ratings) == 3: # in case there are more than 1 000 reviews, symbols are used (k for 1000...)
                                app_d['no_of_ratings_unit'] = no_of_ratings[1]
                        except (AttributeError, IndexError):
                            pass
                    else:
                        try:
                            app_d[k] = css_location(set_of_features, v)
                        except (AttributeError, IndexError):
                            pass
            # parse last version number and release date
            try:
                new = response.css('div.l-row.whats-new__content')
                # date of last release
                v = 'div.l-row time::text'
                app_d['last_release_date'] = new.css('div.l-row time::attr(datetime)').get()
                # version number
                v = 'div.l-row p::text'
                app_d['version_no'] = css_location(new, v).split(' ')[1]
            except AttributeError:
                pass
            # parse description
            try:
                description = response.css("div.section__description")
                app_d['description'] = description.css('p::text').getall()
            except AttributeError:
                pass
            yield app_d
