# MongoDB Vector Search with Sentence Transformers

This repository contains a Python script that integrates MongoDB with Sentence Transformers for generating document embeddings and performing vector searches. The script offers functionalities to either generate new embeddings for a collection of descriptions in MongoDB or to query against these embeddings using vector search.

## Features

- **Model Selection**: Allows users to choose from different transformer models for generating embeddings.
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

Additionally, create a .env file in the root directory of this project with your MongoDB connection string:

```bash
MONGO_URI=mongodb+srv://your_user:your_password@your_cluster/?retryWrites=true&w=majority&appName=VectorSearchApp

## Usage
### Setting Up
Before you run the script in either mode, ensure your MongoDB connection string is set in the .env file as MONGO_URI.

## Generate Mode
This mode drops the existing MongoDB collection, creates a new one, generates embeddings for the stored descriptions, updates the collection, and prints the JSON necessary to create a vector search index:

```bash
python script.py generate --model minilm

After running this command, you should manually create the vector search index in MongoDB Atlas using the provided JSON configuration.

## Query Mode
To search the database using vector search, use the query mode. This mode prompts you for a search query and displays the most relevant documents based on the embeddings:

```bash
python script.py query --model minilm

When prompted, enter your search query. The script will then output the most relevant documents based on cosine similarity scores.

## Running Examples

* Generating Embeddings: Run python script.py generate --model distilbert. This will regenerate the database entries with new embeddings and suggest a JSON configuration for an index.
* Querying: Run python script.py query --model distilbert. Enter a search term when prompted to see the top results.

## Supported Models
Currently, the script supports the following models:

* minilm: 'all-MiniLM-L6-v2' (384 dimensions)
* distilbert: 'distilbert-base-nli-stsb-mean-tokens' (768 dimensions)
* roberta: 'stsb-roberta-large' (1024 dimensions)

You can select the model using the --model flag followed by the model identifier when running the script.

## Contributions
Contributions to this project are welcome! Please consider forking this repository and submitting a pull request.


