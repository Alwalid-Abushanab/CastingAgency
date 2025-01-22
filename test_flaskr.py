from dotenv import load_dotenv
import os
import unittest
import json
from flaskr import create_app
from models.actor import Actor
from models.movie import Movie
from database import db
from datetime import date
import json

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("TEST_DB_NAME")

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhmMTI5MGFmN2I5ZDI0NmYyOGFiMGUiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NTA1MzEwLCJleHAiOjE3Mzc1MTI1MTAsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.cM9pqSekkiBBKDaNcJ-oDnchPxQayiYH6k9odH9Bra5uAkJW-86q6brv0is3yuH_gi_wa8pbrzuCS1gKrrLezavZs7tzAtRNOKZhf3n5a2OjzMSoHRZA3e_a93P6yy1ia16hlYf0pkRpgboNJJHDVBBiJDmC1rMp-cX_qLKcOzJu97MaR3yiaDLZZKbflYN6s-efXxFnAo-p_hFnIypscL1-i835pWpD5kPq-m4pouMs7x1NqqFPn7S5cq1c3cPpMv_Wo6zM-5Oz1K9rK6F04W9qTcIvioomF5B788D3EPJfWieiq7Xl1_kg2CmkD3igkjVtyEEqh_1-OERtrftWpA'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhkYTJlYjFhZDEyZDIxOThmYjg3NWIiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NTA1MjEzLCJleHAiOjE3Mzc1MTI0MTMsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3IiXX0.JFv04b7IukcysaOfznyABNZ_HsuvqQOJajVOn3BpDDe9hWlZeW09RX343SZ0nwp2UZeFU3NKjL9L1Xe3cb9JS5tgnBEPs4l-3zd7EyZld2lBI-c0u7DZGI0F9T6xhDy8a72RC4y66VOijPuVLX6xjpA9RjsTpdj3lP4dEAvInFk4fCvDMupMNsYiZKzisVXiIRXGasJtaaISuPgnZItC7usUstdqQl8ctjOC9b2HIAxdmm2aydfyavGW2-6rBQxdP2Ta9MyvuWjdtyRYyMjdV3K2Al9HfnWkIO4rcLJP6_s6ZSjvb6trwsGtt7mDVek1EtsxO4CQ_MyTROq0cZ7YxQ'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhkYTMwMjM3MmRmMTZiMTAzYTczNTUiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NTA1MjY4LCJleHAiOjE3Mzc1MTI0NjgsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZXMiXX0.BadC5j7VeCGotvA59E10M_Hh72htmxkmhAimPvC6MHdkV7g_OdnGfTQbXx54G2KynCoFfYxpSBGpC040_IpC6_FAkT4iyaJzeI8H5aYaNLhPCuSaLi7zMxOaR_SMqRYoX_YXN2Bk70DgQRaNiz2qvLf9V-alh-et059yp_PYvCh6YJPODPwGparaibtmJ7RhFe7H4UW3_smsXPmZFDZEW1rnkEGyHIlTd3wVOXEir8hDFu9tj27IfIzN1Wskj36171n9VhcOpPBTEp9pQRDLtSjfLE0ReEv4EcoF4pdBbtewp_fT63roEcwAXsp9pQ9i9EU0Px9YOeverNugZZ4DXQ'


class CastingAgencyTestCases(unittest.TestCase):
    """This class represents the Casting Agency test case"""
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_header = {'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
        self.director_header = {'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
        self.producer_header = {'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        
        self.database_name = DB_NAME
        self.database_user = DB_USER
        self.database_password = DB_PASSWORD
        self.database_host = DB_HOST
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": self.database_path,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "TESTING": True,
            }
        )
        
        self.app_context = self.app.app_context()
        self.app_context.push() 
        
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

            movie = Movie(title='tt', release_date=date(year=2024, month=10, day=12))
            movie.insert()
            
            actor = Actor(name='aa', age=18, gender='male')
            actor.insert()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_retrieve_movies(self):
        res = self.client.get("/movies", headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["movies"]), 0)
        
    def test_retrieve_actors(self):
        res = self.client.get("/movies", headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["movies"]), 0)
        
    def test_add_actor(self):
        new_actor = {
            'name': 'bb',
            'age': 25,
            'gender': 'female'
        }

        res = self.client.post("/actors", json=new_actor, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        
    def test_add_movie(self):
        new_movie = {
            'title': 'New Movie',
            'release_date': '2025-01-01'
        }

        res = self.client.post("/movies", json=new_movie, headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        
    def test_update_actor(self):
        actor = Actor.query.first()

        updated_data = {
            'name': 'Updated Name',
            'age': 30
        }

        res = self.client.patch(f"/actors/{actor.id}", json=updated_data, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        updated_actor = Actor.query.get(actor.id)
        self.assertEqual(updated_actor.name, 'Updated Name')
        self.assertEqual(updated_actor.age, 30)
        
    def test_update_movie(self):
        movie = Movie.query.first()

        updated_data = {
            'title': 'Updated Movie',
            'release_date': '2025-12-12'
        }

        res = self.client.patch(f"/movies/{movie.id}", json=updated_data, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        updated_movie = Movie.query.get(movie.id)
        self.assertEqual(updated_movie.title, 'Updated Movie')
        self.assertEqual(updated_movie.release_date, date(2025, 12, 12))
        
    def test_delete_actor(self):
        actor = Actor.query.first()

        res = self.client.delete(f"/actors/{actor.id}", headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        deleted_actor = Actor.query.get(actor.id)
        self.assertIsNone(deleted_actor)
        
    def test_delete_movie(self):
        movie = Movie.query.first()

        res = self.client.delete(f"/movies/{movie.id}", headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        deleted_movie = Movie.query.get(movie.id)
        self.assertIsNone(deleted_movie)
        
    def test_assistant_cannot_delete_movie(self):
        movie = Movie.query.first()

        res = self.client.delete(f"/movies/{movie.id}", headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"], "Permission not found.")
        
    def test_assistant_cannot_delete_acotr(self):
        actor = Actor.query.first()

        res = self.client.delete(f"/actors/{actor.id}", headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"], "Permission not found.")
        
    def test_director_can_delete_movie(self):
        movie = Movie.query.first() 

        res = self.client.delete(f"/movies/{movie.id}", headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"], "Permission not found.")
        
    def test_director_can_retrieve_movies(self):
        res = self.client.get("/movies", headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["movies"]), 0)
        
    def test_producer_can_retrieve_movies(self):
        res = self.client.get("/movies", headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["movies"]), 0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
