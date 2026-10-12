import unittest
from unittest.mock import patch, MagicMock

from app import app


class ProductsAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.ProductModel.select")
    def test_get_products(self, mock_select):
        mock_select.return_value = []

        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    @patch("app.create_product")
    def test_create_product(self, mock_create):
        product = MagicMock()
        product.id = 1
        mock_create.return_value = product

        response = self.client.post(
            "/api/products",
            json={"name": "Test product", "price": 10.0},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json()["message"],
            "Product added successfully.",
        )
        mock_create.assert_called_once_with(
            name="Test product",
            price=10.0,
        )

    @patch("app.get_product_by_id")
    def test_get_missing_product(self, mock_get):
        mock_get.return_value = None

        response = self.client.get("/api/products/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Product not found.",
        )


if __name__ == "__main__":
    unittest.main()
