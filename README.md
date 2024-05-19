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
