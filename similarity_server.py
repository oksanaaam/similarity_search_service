import os
import time

from dotenv import load_dotenv

load_dotenv()

import logging
import grpc
from concurrent import futures


import psycopg2

import similarity_pb2
import similarity_pb2_grpc


def check_database_connection():
    max_retries = 10
    retries = 0
    delay = 1

    while retries < max_retries:
        try:
            connection = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            )
            connection.close()
            print("Database connection successful")
            return True
        except psycopg2.OperationalError:
            print("Waiting for database connection...")
            time.sleep(delay)
            retries += 1

    print("Could not establish database connection")
    return False


class SimilaritySearchService(similarity_pb2_grpc.SimilaritySearchServiceServicer):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def AddItem(self, request, context):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO items (id, description) VALUES (%s, %s)",
                (request.id, request.description),
            )
            self.connection.commit()
            cursor.close()
            return similarity_pb2.AddItemResponse(
                status=0, message=f"{request.id} id added successfully"
            )
        except Exception as e:
            return similarity_pb2.AddItemResponse(status=1, message=str(e))

    def SearchItems(self, request, context):
        query = request.query

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id FROM items WHERE description ILIKE %s", ("%" + query + "%",)
            )
            row = cursor.fetchone()
            search_id = row[0] if row else ""
            cursor.close()

            return similarity_pb2.SearchItemsResponse(search_id=search_id)
        except Exception as e:
            return similarity_pb2.SearchItemsResponse(search_id="Not found")

    def GetSearchResults(self, request, context):
        search_id = request.search_id

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id, description FROM items WHERE id = %s", (search_id,)
            )
            row = cursor.fetchone()
            cursor.close()

            if row:
                result = similarity_pb2.SearchResult(id=row[0], description=row[1])
                return similarity_pb2.GetSearchResultsResponse(results=[result])
            else:
                return similarity_pb2.GetSearchResultsResponse(results=[])
        except Exception as e:
            return similarity_pb2.GetSearchResultsResponse(results=[])


def serve():
    if not check_database_connection():
        return

    port = "5001"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    similarity_pb2_grpc.add_SimilaritySearchServiceServicer_to_server(
        SimilaritySearchService(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
