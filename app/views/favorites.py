from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Client, FavoriteProduct
from app.repositories.product_repository import get_products_by_id
from app.serializers import FavoriteProductSerializer


class FavoriteProductView(APIView):
    def post(self, request, client_id):
        try:
            logger.info(f"Adding product at wishlist for client {client_id}")
            product_id = request.data.get("product_id")
            if not product_id:
                logger.error(f"Missing product_id in request for client {client_id}")
                return Response({"error": "product_id is required"}, status=400)

            client = get_object_or_404(Client, id=client_id)

            if FavoriteProduct.objects.filter(client=client, product_id=product_id).exists():
                logger.error(f"Product {product_id} already in wishlist for client {client_id}")
                return Response({"error": f"Product already in wishlist for client {client_id}"}, status=400)

            response = get_products_by_id(product_id)
            if response.status_code != 200:
                logger.error(f"Product {product_id} not found in external API")
                return Response({"error": f"Product {product_id} not found in external API"}, status=404)

            fav = FavoriteProduct.objects.create(client=client, product_id=product_id)
            logger.success(f"Product {product_id} added at wishlist successfully for client {client_id}")
            return Response(FavoriteProductSerializer(fav).data, status=201)

        except Exception as e:
            logger.error(f"Error to add product at wishlist for client {client_id}: {e}")
            return Response({"error": f"{e}"}, status=500)

    def get(self, request, client_id):
        try:
            logger.info(f"Getting favorites for client {client_id}")
            client = get_object_or_404(Client, id=client_id)
            favorites = FavoriteProduct.objects.filter(client=client)
            logger.info(f"Found {len(favorites)} favorites products for client {client_id}")

            wishlist = []
            for fav in favorites:
                response = get_products_by_id(fav.product_id)
                if response.status_code == 200:
                    product_data = response.json()
                    wishlist.append(product_data)
                    logger.info(f"Product {fav.product_id} details retrieved successfully")
                else:
                    logger.warning(f"Failed to retrieve product {fav.product_id} details")
                    wishlist.append({"product_id": fav.product_id, "error": "Product not found"})

            return Response(wishlist)

        except Exception as e:
            logger.error(f"Error to get wishlist for client {client_id}: {e}")
            return Response({"error": f"{e}"}, status=500)

    def delete(self, request, client_id, product_id):
        try:
            logger.info(f"Deleting favorite product {product_id} for client {client_id}")
            client = get_object_or_404(Client, id=client_id)
            fav = FavoriteProduct.objects.filter(client=client, product_id=product_id).first()

            if not fav:
                logger.error(f"Product {product_id} not found in wishlist for client {client_id}")
                return Response({"error": "Product not found in wishlist"}, status=404)

            fav.delete()
            logger.success(f"Product {product_id} removed from favorites for client {client_id}")
            return Response(status=204)
        except Exception as e:
            logger.error(f"Error to delete product from wishlist for client {client_id}: {e}")
            return Response({"error": f"{e}"}, status=500)
