# MongoDB Vector Search with Sentence Transformers

This repository contains a Python script that integrates MongoDB with Sentence Transformers for generating document embeddings and performing vector searches. The script offers functionalities to load data, generate new embeddings for a collection of descriptions in MongoDB, or to query against these embeddings using vector search.

## Features

- **Model Selection**: Allows users to choose from different transformer models for generating embeddings.
- **Load Mode**: Loads predefined static inventory data into MongoDB.
- **Generate Mode**: Generates embeddings for descriptions stored in a MongoDB collection and updates the collection with these embeddings.
- **Query Mode**: Performs vector searches on the generated embeddings to find relevant documents based on a user query.
- **Index Management**: Provides JSON configuration for creating a MongoDB vector search index tailored to the dimensions of the selected model.

## Prerequisites

- Python 3.6+
- MongoDB Atlas Account
- MongoDB Cluster with network access configured

## Installation

Before running the script, ensure you have the necessary Python packages installed:

```bash
pip install pymongo sentence-transformers python-dotenv
```

Additionally, create a .env file in the root directory of this project with your MongoDB connection string:

```bash
MONGODB_URI=mongodb+srv://your_user:your_password@your_cluster/?retryWrites=true&w=majority&appName=VectorSearchApp
```

## Usage

The script is designed to demonstrate 3 basic modes of operation: 
1. **Load** Load data into the database. This mode will load a very simple, very small basic hardware inventory database into your Atlas instance.
2. **Generate** Generate vector embeddings using one of several transformer models. You can choose which model to use for the `generate` mode but remember to use the same model choice for `query` mode.
3. **Query** Ask a question of the database. This question will be encoded using the model of your choice and sent to MongoDB using `$vectorSearch`.

### Setting Up
Before you run the script in any mode, ensure your MongoDB connection string is set in the .env file as `MONGODB_URI`.  

## Load Mode
Loads static inventory data into the MongoDB 'inventory' collection. This is useful for initially populating the database with sample data.

```bash
python script.py load
```

## Generate Mode
This mode generates embeddings for the stored descriptions, updates the collection, and prints the JSON necessary to create a vector search index:

```bash
python script.py generate --model minilm
```

After running this command, you should manually create the vector search index in MongoDB Atlas using the provided JSON configuration.

## Query Mode
To search the database using vector search, use the query mode. This mode prompts you for a search query and displays the most relevant documents based on the embeddings:

```bash
python script.py query --model minilm
```

When prompted, enter your search query. The script will then output the most relevant documents based on cosine similarity scores.

## Running Examples

* Generating Embeddings: Run `python script.py generate --model distilbert`. This will regenerate the database entries with new embeddings and suggest a JSON configuration for an index.
* Querying: Run `python script.py query --model distilbert`. Enter a search term when prompted to see the top results. This will perform a semantic search against the inventory database and return the top 3 suggestions along with a search score.  Note that different models will have different results.

## Supported Models
Currently, the script supports the following models:

* **minilm**: 'all-MiniLM-L6-v2' (384 dimensions)
* **distilbert**: 'distilbert-base-nli-stsb-mean-tokens' (768 dimensions)
* **roberta**: 'stsb-roberta-large' (1024 dimensions)
* **msmarco**: 'msmarco-distilbert-base-v2' (768 dimensions)

You can select the model using the --model flag followed by the model identifier when running the script.

## Contributions
Contributions to this project are welcome! Please consider forking this repository and submitting a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

