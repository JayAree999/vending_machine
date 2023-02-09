import json


def test_vending_machine_api_post(client):
    data = {"location": "Location1", "name": "VendingMachine1"}
    response = client.post(
        "/vending-machines", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {
        "id": 1,
        "location": "Location1",
        "name": "VendingMachine1",
    }


def test_vending_machine_stock_api_post(client):
    data = {
        "items": [{"name": "item1", "quantity": 15}, {"name": "item2", "quantity": 20}]
    }
    response = client.post(
        "/vending-machines/1/stock",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"message": "Stock items added successfully"}


def test_vending_machine_stock_api_get(client):
    response = client.get("/vending-machines/1/stock")
    assert response.status_code == 200
    assert response.json == {
        "items": [{"name": "item1", "quantity": 15}, {"name": "item2", "quantity": 20}]
    }


def test_vending_machine_api_get(client):
    response = client.get("/vending-machines")
    assert response.status_code == 200
    assert response.json == {'machines': [{'id': 1, 'location': 'Location1', 'name': 'VendingMachine1',
                                           'stock': [{'product': 'item1', 'quantity': 15},
                                                     {'product': 'item2', 'quantity': 20}]}]}


def test_vending_machine_stock_api_put(client):
    data = {
        "items": [{"name": "item1", "quantity": 30}, {"name": "item2", "quantity": 25}]
    }
    response = client.put(
        "/vending-machines/1/stock",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json == {"message": "Stock items updated successfully"}


def test_vending_machine_stock_api_delete(client):
    data = {"items": [{"name": "item1"}, {"name": "item2"}]}
    response = client.delete(
        "/vending-machines/1/stock",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json == {"message": "Stock items deleted successfully"}


def test_vending_machine_delete(client):
    data = {"machines": [{"id": 1}]}
    response = client.delete(
        "/vending-machines/1",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json == {"message": "Machines deleted successfully"}
