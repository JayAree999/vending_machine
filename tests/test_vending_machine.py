import unittest
import requests


class APITest(unittest.TestCase):

    def test_post(self):
        data = {'name': 'Vending_Machine_1', 'location': "MUIC Building"}
        response = requests.post('http://localhost:5000/vending-machines', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Vending_Machine_1')
        self.assertEqual(response.json()['location'], 'MUIC Building')

    def test_delete(self):
        response = requests.post('http://localhost:5000/vending-machines')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
