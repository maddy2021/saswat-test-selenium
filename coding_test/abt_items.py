from datetime import datetime

class AbtItems():
    def __init__(self, url,status=None, 
                    lang="en-us", brand="", title="", asin="", buybox_message="", categories=[], image_url="", 
                    image_urls=[], model="", reseller_id="", sku="", upc="", site_product_id="", 
                    short_description="", buyer_ratings="", variants=[], price_ammount="", now_price="", 
                    buyer_reviews=[], price_currency="USD", redirected="",crawled_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.lang = lang
        self.brand = brand
        self.title = title
        self.asin = asin
        self.buybox_message = buybox_message
        self.categories = categories
        self.image_url = image_url
        self.image_urls = image_urls
        self.model = model
        self.reseller_id = reseller_id
        self.sku = sku
        self.stie = title
        self.upc = upc
        self.site_product_id = site_product_id
        self.short_description = short_description
        self.buyer_ratings = buyer_ratings
        self.variants = variants
        self.price_ammount = price_ammount
        self.now_price = now_price
        self.buyer_reviews = buyer_reviews
        self.price_currency = price_currency
        self.url = url
        self.status = status
        self.redirected = redirected
        self.crawled_at = crawled_at
