import os
import responses
import requests
from django.conf import settings
from django.core.cache import cache
from loguru import logger

@responses.activate
def get_products_by_id(product_id):
    try:
        cache_key = f"product:{product_id}"
        cached_product = cache.get(cache_key)

        if cached_product:
            logger.info(f"Cache hit for product {product_id}")
            return cached_product

        url = f"{os.getenv('API_PRODUCTS_URL')}/api/product/{product_id}/"
        responses.add(
            method=responses.GET,
            url=url,
            json={
                "id": product_id,
                "title": "Test Product",
                "price": 199.90,
                "image": "http://image.com/product.jpg",
                "brand": "Brand X",
                "reviewScore": 4.5
            },
            status=200
        )

        response = requests.get(url)

        if response.status_code == 200:
            logger.info(f"Caching product {product_id}")
            cache.set(cache_key, response, timeout=3600)

        return response

    except Exception as e:
        logger.error(f"Error at get products by id: {e}")
        raise