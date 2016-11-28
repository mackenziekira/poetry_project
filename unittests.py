import unittest
from server import app
import server
from model import example_data, connect_to_db, db, Poem, PoemSubject, Author, Subject

class FlaskTests(unittest.TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

  def test_homepage(self):
      """Test homepage"""

      result = self.client.get("/")
      self.assertEqual(result.status_code, 200)
      self.assertIn('Search for a word...', result.data)

  def test_kmeans_page(self):
      """Test kmeans page"""

      result = self.client.get("/kmeans")
      self.assertEqual(result.status_code, 200)
      self.assertIn('k=4', result.data)

class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_subjects_page(self):
        """Test subjects page."""
        
        result = self.client.get("/subjects")
        self.assertIn("delight", result.data)

    def test_authors_page(self):
        """Test authors page."""

        result = self.client.get("/authors")
        self.assertIn("Nellie Bly", result.data)

    def test_lda_page(self):
        """Test lda page."""

        result = self.client.get("/lda")
        self.assertIn("Studs Terkel", result.data)



if __name__ == '__main__':
    unittest.main()