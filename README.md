# Similarity Search Service

The Similarity Search Service is a gRPC-based service that allows you to perform similarity searches on a database of items. It provides functionality to add new items to the database, search for similar items based on a query, and retrieve the search results.

## Features

- Add new items to the database
- Search for similar items based on a query
- Retrieve search results

## Technologies Used

- Python
- gRPC
- Docker
- PostgreSQL (or the database of your choice)

## Installation

1. Clone the repo
`git clone https://github.com/oksanaaam/similarity_search_service.git`

2. Open the project folder in your IDE
3. Open a terminal in the project folder
4. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
```
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

### Configuration
Modify the .env file in the project root directory:

```
POSTGRES_HOST=<database_host>
POSTGRES_PORT=<database_port>
POSTGRES_DB=<database_name>
POSTGRES_USER=<database_username>
POSTGRES_PASSWORD=<database_password>
```

Run local server:

`python similarity_server.py`

![run_server.png](img%20for%20REAdME.md%2Frun_server.png)

Run client:

`python similarity_client.py`

![client.png](img%20for%20REAdME.md%2Fclient.png)


Build and run the Docker containers:

`docker-compose up`

This will start the PostgreSQL database and the similarity search service containers.

### Usage

Once the Docker containers are up and running, you can interact with the similarity search service using a gRPC client.   
Refer to the similarity.proto file for the available methods and message formats.

### Testing

To run the unit tests for the similarity search service, use the following command:

`python -m unittest discover tests`

![tests.png](img%20for%20REAdME.md%2Ftests.png)
