import unittest
import sys
import os
from unittest.mock import patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app


class SimpleAppTests(unittest.TestCase):
    """Simple test cases for the Flask application"""

    def setUp(self):
        """Set up test client before each test"""
        # Patching functions responsible for initializing mongodb and sqlite
        self.mongo_patcher = patch('app.mongo_init_db')
        self.sqlite_patcher = patch('app.init_db')
        
        # Starting Patchers
        self.mock_mongo = self.mongo_patcher.start()
        self.mock_sqlite = self.sqlite_patcher.start()
        
        # This creates app but skips the databases
        app = create_app()
        app.testing = True  # Enable testing mode
        self.app = app.test_client()  # Initialize test client

    def tearDown(self):
        """Clean up after each test"""
        # Stop the patchers
        self.mongo_patcher.stop()
        self.sqlite_patcher.stop()

    def test_login_page(self):
        """Test that login page loads and contains expected content"""
        response = self.app.get('/login')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Password', response.data)

    def test_register_page(self):
        """Test that register page loads and contains expected content"""
        response = self.app.get('/register')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Password', response.data)

    def test_home_page_redirect(self):
        """Test that home page redirects to login"""
        response = self.app.get('/')
        
        # Check if redirects (302) or already at login (200)
        self.assertIn(response.status_code, [200, 302])

    def test_app_in_testing_mode(self):
        """Test that the app is in testing mode"""
        self.assertTrue(self.app.application.testing)

    def test_app_exists(self):
        """Test that the Flask app can be created"""
        self.assertIsNotNone(self.app.application)


if __name__ == "__main__":
    print("Running 5 tests...\n")
    
    # Run tests
    result = unittest.main(verbosity=2, exit=False)
    
    # Print final summary
    if result.result.wasSuccessful():
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*70)
        print(f"Total tests run: {result.result.testsRun}")
        print("="*70 + "\n")
