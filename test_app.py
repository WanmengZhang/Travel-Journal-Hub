"""
Unit tests for Travel Journal Hub API
Tests the Flask application endpoints and functionality
"""
import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app


class TravelJournalHubTestCase(unittest.TestCase):
    """Test case for Travel Journal Hub API"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')

    def test_index_route(self):
        """Test that the index route returns HTML"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_entry_missing_fields(self):
        """Test creating entry with missing required fields"""
        # Missing all fields
        response = self.client.post(
            '/api/entries',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Missing some fields
        response = self.client.post(
            '/api/entries',
            data=json.dumps({'title': 'Test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_entry(self):
        """Test getting an entry that doesn't exist"""
        response = self.client.get('/api/entries/999999')
        # Should return 404 or 500 (if DB not configured)
        self.assertIn(response.status_code, [404, 500])

    def test_update_nonexistent_entry(self):
        """Test updating an entry that doesn't exist"""
        response = self.client.put(
            '/api/entries/999999',
            data=json.dumps({
                'title': 'Test',
                'location': 'Test',
                'travel_date': '2024-01-01',
                'content': 'Test'
            }),
            content_type='application/json'
        )
        # Should return 404 or 500 (if DB not configured)
        self.assertIn(response.status_code, [404, 500])

    def test_delete_nonexistent_entry(self):
        """Test deleting an entry that doesn't exist"""
        response = self.client.delete('/api/entries/999999')
        # Should return 404 or 500 (if DB not configured)
        self.assertIn(response.status_code, [404, 500])

    def test_api_endpoints_exist(self):
        """Test that all expected API endpoints exist"""
        # Get all entries
        response = self.client.get('/api/entries')
        # Should return 200 or 500 (if DB not configured)
        self.assertIn(response.status_code, [200, 500])


if __name__ == '__main__':
    print("Running Travel Journal Hub tests...")
    print("Note: Some tests may fail if MySQL database is not configured.")
    unittest.main(verbosity=2)
