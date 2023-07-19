import os
import unittest
import grpc
import psycopg2

import similarity_pb2
import similarity_pb2_grpc
import similarity_server

from dotenv import load_dotenv

load_dotenv()


class SimilaritySearchServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the gRPC server
        cls.server = similarity_server.SimilaritySearchService()
        cls.server.connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    @classmethod
    def tearDownClass(cls):
        cls.server.connection.close()

    def setUp(self):
        self.clear_items_table()
        self.create_items_table()

    def tearDown(self):
        self.clear_items_table()

    def clear_items_table(self):
        cursor = self.server.connection.cursor()
        cursor.execute("DELETE FROM items")
        self.server.connection.commit()

    def create_items_table(self):
        cursor = self.server.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, description VARCHAR(255))"
        )
        self.server.connection.commit()
        cursor.close()

    def test_add_item(self):
        request = similarity_pb2.AddItemRequest(id="4", description="Fourth item")

        channel = grpc.insecure_channel("localhost:5000")
        stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

        response = stub.AddItem(request)

        self.assertEqual(response.status, 0)
        self.assertEqual(response.message, "4 id added successfully")

    def test_search_items(self):
        channel = grpc.insecure_channel("localhost:5000")
        stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

        add_request1 = similarity_pb2.AddItemRequest(id="1", description="First item")
        add_request2 = similarity_pb2.AddItemRequest(id="2", description="Second item")
        stub.AddItem(add_request1)
        stub.AddItem(add_request2)

        request = similarity_pb2.SearchItemsRequest(query="first")

        response = stub.SearchItems(request)

        self.assertEqual(response.search_id, "1")

    def test_get_search_results(self):
        channel = grpc.insecure_channel("localhost:5000")
        stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

        add_request = similarity_pb2.AddItemRequest(id="1", description="First item")
        stub.AddItem(add_request)

        request = similarity_pb2.GetSearchResultsRequest(search_id="1")

        response = stub.GetSearchResults(request)

        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].id, "1")
        self.assertEqual(response.results[0].description, "First item")


if __name__ == "__main__":
    unittest.main()
