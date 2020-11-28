""" Separated tests for Products. """

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_city_data_getter():
    product_creation_params = {
            'id': 10,
            'name': 'some prediction',
            'stock_balance': 10,
            'reserved_number': 2,
            'description': 'hello',
    }

    response = client.post(
        '/prediction/create/',
        json=product_creation_params
    )
    assert response.json() == {'status_code': '200'}
