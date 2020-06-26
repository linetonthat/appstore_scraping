# landing pages on the appstore (also served as referer url in the request headers)
url = 'https://apps.apple.com/us/app/airvisual-air-quality-forecast/id1048912974' #AirVisual Air Quality Forecast
url = 'https://apps.apple.com/fr/app/sensio-air-allergy-tracker/id1252417620' # sensio
url = 'https://apps.apple.com/fr/app/plume-air-report-pollution/id950289243' # Plume air report
url = 'https://apps.apple.com/fr/app/air-to-go-qualit%C3%A9-de-lair/id1155558364' #AirToGo Auvergne Rhône-Alpes
url = 'https://apps.apple.com/us/app/airly/id1283400152' # Airly
url = 'https://apps.apple.com/fr/app/pollen/id515301928' #pollen
url = 'https://apps.apple.com/fr/app/breezometer-air-quality-index/id989623380' # breezometer


# also check appstores from different countries
'https://apps.apple.com/us/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #us
'https://apps.apple.com/gb/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #gb
'https://apps.apple.com/ae/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #uae
'https://apps.apple.com/de/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #de
'https://apps.apple.com/in/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #india
'https://apps.apple.com/cn/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #china
'https://apps.apple.com/kr/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #korea
'https://apps.apple.com/jp/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #japan
'https://apps.apple.com/ua/app/airvisual-qualit%C3%A9-de-lair/id1048912974#see-all/reviews' #ukraine


# pages and parameters to access see-all review pages
'/v1/catalog/fr/apps/1048912974/reviews?l=fr-FR&offset=30'
root_url = 'https://amp-api.apps.apple.com/v1/catalog/US/apps/'
app_id = '1048912974' #AirVisual
def parameters(offset):
    return {
                "l":"fr-FR",
                "offset": offset,
                "platform":"web",
                "additionalPlatforms":"appletv,ipad,iphone,mac"
            }
from urllib.parse import urlencode
url = root_url+app_id+'/reviews?'+ urlencode(parameters(offset))

# page loaded with reviews from the landing page
root_url = 'https://amp-api.apps.apple.com/v1/catalog/FR/apps/'
app_id = '1048912974' #AirVisual
params = {
            "platform" : "web",
            "additionalPlatforms":"appletv,ipad,iphone,mac",
            "extend":"description,developerInfo,editorialVideo,eula,fileSizeByDevice,messagesScreenshots,privacyPolicyUrl,privacyPolicyText,promotionalText,screenshotsByType,supportURLForLanguage,versionHistory,videoPreviewsByType,websiteUrl",
            "include":"genres,developer,reviews,merchandised-in-apps,customers-also-bought-apps,developer-other-apps,app-bundles,top-in-apps,eula",
            "l":"fr-fr"
        }
from urllib.parse import urlencode
root_url+app_id+'?'+ urlencode(params)

#################################################################################
# ids found on the url of selected apps related to air quality on the appstore 
app_ids = {
            'AirVisual': ['1048912974', 'airvisual-air-quality-forecast'],
            'Sensio' : ['1252417620','sensio-air-allergy-tracker'],
            'Plume': ['950289243','plume-air-report-pollution'],
            'AirToGo' ['1155558364','air-to-go-qualit%C3%A9-de-lair'],
            'Airly':['1283400152','airly'],
            'Pollen':['515301928','pollen'],
            'Breezometer' : ['989623380','breezometer-air-quality-index']
            }
