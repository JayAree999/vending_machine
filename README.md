# Vending Machine API

A RESTful API for managing vending machines and their stock.

## Installation

1. Set up a virtual environment and activate it.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set up the environment variable `SQLALCHEMY_DATABASE_URI` with the database connection string.
4. Run `app.py` to start the server.

## API Endpoints

### Vending Machine

- `GET /vending-machines`: Retrieve a list of all vending machines and their stock.
- `POST /vending-machines`: Add a new vending machine.

  Example payload:

  ```json
  {
      "location": "Lobby",
      "name": "Snack Machine"
  }
  ``` 

### Vending Machine Stock

- `GET /vending-machines/<int:vending_machine_id>/stock``: Retrieve the stock for a specific vending machine.

- `POST /vending-machines/<int:vending_machine_id>/stock`: Add stock to a specific vending machine.

Example payload:
  ```json
{
    "items": [
        {
            "name": "Pringles",
            "quantity": 10,
            "price": 1.50
        }
    ]
}
```

- `PUT /vending-machines/<int:vending_machine_id>/stock`: Update the stock for a specific vending machine.

Example payload:

```json

{
    "items": [
        {
            "name": "Pringles",
            "quantity": 5
        }
    ]
}
```
- `DELETE /vending-machines/<int:vending_machine_id>/stock``: Remove stock from a specific vending machine.

Example payload:

```json

{
    "items": [
        {
            "name": "Pringles"
        }
    ]
}
```
### Product Timeline
- `GET /products/<string:product_name>/timeline`: Get the total amount of the given product at each time by vending machine.
Vending Machine Timeline
- `GET /vending-machines/<int:vending_machine_id>/timeline`: Get the products in the given vending machine at each time.
### Testing
To run the tests, simply run python `test_app.py`.
