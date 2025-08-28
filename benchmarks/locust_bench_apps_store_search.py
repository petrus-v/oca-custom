from pathlib import Path
from random import choice

from locust import HttpUser, between, task


class AppStoreSearch(HttpUser):
    wait_time = between(1, 5)

    @task(60)
    def shop_get(self):
        self.client.get(choice(HTTP_SHOP_REQUESTS), name="/shop")

    @task(35)
    def shop_category_get(self):
        self.client.get(choice(HTTP_SHOP_CATEGORY_REQUESTS), name="/shop/category")

    @task(2)
    def shop_page_get_page(self):
        self.client.get(choice(HTTP_SHOP_PAGE_REQUESTS), name="/shop/page")

    @task(1)
    def shop_product_autocomplete_post(self):
        self.client.post(
            "/shop/products/autocomplete",
            json={
                "term": choice(PRODUCT_AUTO_COMPLETE_CALL),
            },
        )

    # def on_start(self):
    # self.client.post("/login", json={"username":"foo", "password":"bar"})


PRODUCT_AUTO_COMPLETE_CALL = (
    Path("./assets/product_autocomplete.txt").open("r").readlines()
)
HTTP_SHOP_CATEGORY_REQUESTS = (
    Path("./assets/uri_shop_category.txt").open("r").readlines()
)
HTTP_SHOP_REQUESTS = Path("./assets/uri_shop.txt").open("r").readlines()
HTTP_SHOP_PAGE_REQUESTS = Path("./assets/uri_shop_page.txt").open("r").readlines()
