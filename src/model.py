class Product():
    def __init__(self, product_id: int, asin: str, title: str = None, product_group: str = None, salesrank: int = None, review_total: int = None, review_downloaded: int = None, review_avg: float = None):
        self.product_id = product_id
        self.asin = asin
        self.title = title
        self.product_group = product_group
        self.salesrank = salesrank
        self.review_total = review_total
        self.review_downloaded = review_downloaded
        self.review_avg = review_avg

    def to_str(self):
        print(f"product_id = {self.product_id}")
        print(f"asin = {self.asin}")
        print(f"title = {self.title}")
        print(f"product_group = {self.product_group}")
        print(f"salesrank = {self.salesrank}")
        print(f"review_total = {self.review_total}")
        print(f"review_downloaded = {self.review_downloaded}")
        print(f"review_avg = {self.review_avg}")

class Category():
    def __init__(self, category_id: int, name: str, parent_id: int = None):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id

class ProductCategory():
    def __init__(self, product_id: int, category_id: int):
        self.product_id = product_id
        self.category_id = category_id

class SimilarProduct():
    def __init__(self, product_asin: str, similar_asin: str):
        self.product_asin = product_asin
        self.similar_asin = similar_asin

class Review():
    def __init__(self, product_id: int, customer_id: str, review_date: str, rating: int=None, votes: int=None, helpful: int=None):
        self.product_id = product_id
        self.customer_id = customer_id
        self.review_date = review_date
        self.rating = rating
        self.votes = votes
        self.helpful = helpful