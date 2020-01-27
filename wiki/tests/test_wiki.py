import json
import unittest
import requests


class TestWikiApi(unittest.TestCase):

    def test_raw_sql_with_valid_query(self):
        response = requests.post('http://localhost:8000/api/v1/rawquery', json={"query": "select * from category limit 2"})
        self.assertEqual(response.status_code, 200)

    def test_raw_sql_with_injection_query(self):
        response = requests.post('http://localhost:8000/api/v1/rawquery', json={"query": "drop table category"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_sql_query(self):
        response = requests.post('http://localhost:8000/api/v1/rawquery', json={"query": "select from category"})
        self.assertEqual(response.status_code, 400)

    def test_raw_sql_with_no_body(self):
        response = requests.post('http://localhost:8000/api/v1/rawquery')
        self.assertEqual(response.status_code, 400)

    def test_outdated_category_with_param(self):
        response = requests.get('http://localhost:8000/api/v1/outdatedpages', params={'category_name': 'Commons_category_link_is_on_Wikidata'})
        self.assertEqual(response.status_code, 200)

    def test_outdated_category_with_invalid_param(self):
        response = requests.get('http://localhost:8000/api/v1/outdatedpages', params={'category_name': 'lynx'})
        self.assertFalse(json.loads(response.text), 'Result set is not empty..')

    def test_outdated_category_without_param(self):
        response = requests.get('http://localhost:8000/api/v1/outdatedpages')
        self.assertEqual(response.status_code, 200)

    def test_outdated_category_with_sql_query(self):
        response = requests.get('http://localhost:8000/api/v1/outdatedpages?category_name=select\ *\ from\ category')
        self.assertFalse(json.loads(response.text), 'Result set is not empty..')


if __name__ == '__main__':
    unittest.main()
