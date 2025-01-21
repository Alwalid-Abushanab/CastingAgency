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

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhmMTI5MGFmN2I5ZDI0NmYyOGFiMGUiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NDI5Njg4LCJleHAiOjE3Mzc0MzY4ODgsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.RQr566YofXPHPiVfZlucU63H9brSJBxbuiMvlDWRFBBeRNuyq2oswx6oqIoUONmqHU_1jgEjSwUuNZb18mPhoYTPEd-qA6JsaBDo-gS1P1Fh_CA1WNvoNFr9NIvqDpukRpBwxZoUNeeTi0J_HWeNa8IBd4jGuxUHDP-8UZkR8Sc10-iWb07EoRgTpOLslD98Cf4aZJcUxPf7qe61cNmQylhYGfUnTSb-BoyugdPLepgCWyA-rNr3ZyWMfRuMpt232Itcrtvg9mGAxizmJlfFTyQ8FKmXGESO5Y64OY8pz0idmWaj3iTn-t46Qf-2XuEGiqkv2iyGzUNadvI4lvVOrg'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhkYTJlYjFhZDEyZDIxOThmYjg3NWIiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NDI5NDMyLCJleHAiOjE3Mzc0MzY2MzIsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3IiXX0.Obfs1EqIYWbCedoeA1l0IIrrRyciojjTYdMojjsdq-QQ_FeT1bcvXYgbtwJDYidpQhN1K0rZgsiIRdxZ2CrtI4ljtQTKzzmKMsJkqNzRxmwebl_HcpXUGhZCjZdDEPOtO2FBKkgBDdBiDu62ZbBdJqRglm7johjKZuoBR6oHwByN4UmMKEWRC93RZmv7xPbnBhDSRHuvPd1y6ZhVbxfm_28C9bNWTUCQWJiqxzCW8sa4UaNWbOhlHIoQ4t_85dmM5aVETpywpP5BJdAdSAwlME4GipkYr2AuYxjsAcYSYoPV-bD1-PAdiqhmEw5uMaqgldfAAVjSKaYaYsMf6StMYw'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZ4UjZGVFZXZHlYNXAtUFBUMXJtOSJ9.eyJpc3MiOiJodHRwczovL2Rldi14OGhzc3BvcmxjeWh1cWt2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzhkYTMwMjM3MmRmMTZiMTAzYTczNTUiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNzM3NDI5NTA0LCJleHAiOjE3Mzc0MzY3MDQsInNjb3BlIjoiIiwiYXpwIjoiOFh5VjJQY1QyanFZNmozcEIwOXcwWnVNWnZVbjVrdDciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZXMiXX0.cI0FlTEmKNMLD9v0WO7ZW0ki2G6CHfrGAtQi-W9_q_fUtc1fn9sUtomBDKyA_FS-nzpfLgF3FCOx2pil-cDVstESyuKIm9gRQv9QrQVvvnD29b_YsN4ycMLEUGpis0Bwu0cW-l6IYjDlhqaIqjSDwmMA9_ZjXbaYzXFeqZFQVmU1vuTmQm4cw3AwIwAOxP5naTFpvLjHIyIji7SmrP3T3c854LwGM6JtlV5y4GO__5P7jCemlZDat_H4mKinSFM3iVopj0QAubcFA_ljkEeW-9ifSU1uTHOtfe8lKTdVLwq4qiyYTFbJFYEPloeIOVmdNyzwrwP99uyxBLBPPqPdeg'


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
