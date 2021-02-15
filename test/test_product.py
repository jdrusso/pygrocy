import pytest


class TestProduct:
    @pytest.mark.vcr
    def test_product_get_details_valid(self, grocy):
        product = grocy.product(10)

        assert product.name == "Cheese"
        assert product.available_amount == 5
        assert len(product.barcodes) == 0
        assert product.product_group_id == 6

    @pytest.mark.vcr
    def test_product_no_barcodes(self, grocy):
        stock = grocy.stock()
        product = next(prod for prod in stock if prod.id == 2)

        assert product.name == "Chocolate"
        assert product.product_barcodes is not None
        assert isinstance(product.product_barcodes, list)
        assert len(product.product_barcodes) == 0

    @pytest.mark.vcr
    def test_product_get_details_non_existant(self, grocy):
        import requests

        with pytest.raises(requests.exceptions.HTTPError):
            grocy.product(200)

    @pytest.mark.vcr
    def test_add_product_pic_valid(self, grocy, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = True

        mocker.patch("builtins.open", mocker.mock_open())

        assert grocy.add_product_pic(20, "/somepath/pic.jpg") is None
