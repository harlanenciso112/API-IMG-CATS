import sys
sys.path.append('..')

import unittest
import hashlib
from datetime import datetime
from app.app import app

class TestUnitarios(unittest.TestCase):
    
    def test_hash_md5(self):
        data = b'imagen de prueba'
        result = hashlib.md5(data).hexdigest()
        self.assertEqual(len(result), 32)
    
    def test_hash_consistente(self):
        data = b'misma imagen'
        hash1 = hashlib.md5(data).hexdigest()
        hash2 = hashlib.md5(data).hexdigest()
        self.assertEqual(hash1, hash2)
    
    def test_datetime_formato(self):
        now = datetime.now().isoformat()
        self.assertIn('T', now)

class TestIntegracion(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()
    
    def test_get_cat(self):
        response = self.client.get('/cat')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')
    
    def test_get_count(self):
        response = self.client.get('/count')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('total_images', data)
    
    def test_get_image_not_found(self):
        response = self.client.get('/image/9999')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_not_found(self):
        response = self.client.delete('/delete/9999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()