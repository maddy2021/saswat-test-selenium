# ID, TAG, CSS, XPATH CONSTANTS
PRODUCT_AND_PRICE_SCRIPT_XPATH = '//*[@id="price_container"]//script[@type="application/ld+json"]'
BREAD_CRUMB_SCRIPT_XPATH = '//*[@id="content_shell_container"]/script[@type="application/ld+json"]'
PRODUCT_TITLE_ID = 'product_title'
BUY_BOX_MESSAGE_ID = 'product_shipping_container'
BREAD_CRUMB_XPATH = '//div[@class="bread_crumb_bar"]//li'
IMAGE_GALLARY_XPATH = '//div[@id="product_thumbnails"]//a'
# Currently extracting first para only
DESCRIPTION_XPATH = '//*[@id="overview_content"]//table//p[1]'
VARIENTS_XPATH = '//div[@class="display-group-attribute"]/ul//li'
BUYER_RATING_XPATH = '//*[@id="product-reviews-snippet"]/div[@class="abt-reviews-rating"]/span[@class="sr-only"]'
REVIEW_SECTION_XPATH = '//*[@id="pr-review-snapshot"]//ul[contains(@class,"pr-ratings-histogram")]/li//p' 
LANG_ATTRIBUTE = "lang"
HREF_ATTRIBUTE = "href"
INNER_HTML_ATTRIBUTE = "innerHTML"

# REGEX
# For rating 
RATING_SATAR_REGEX = r'\d{1} star*'

# DATE TO STRiNG FORMATE
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"