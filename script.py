import argparse
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Dictionary to map model identifiers to model names and their dimensions
model_choices = {
    'minilm': ('all-MiniLM-L6-v2', 384),
    'distilbert': ('distilbert-base-nli-stsb-mean-tokens', 768),
    'roberta': ('stsb-roberta-large', 1024)
}

def get_model_info(model_key):
    """Retrieve model info based on the model key."""
    model_name, dimensions = model_choices.get(model_key, ('all-MiniLM-L6-v2', 384))  # Default to MiniLM if key not found
    model = SentenceTransformer(model_name)
    return model, dimensions

def parse_args():
    parser = argparse.ArgumentParser(description="Run the embedding generation or query.")
    parser.add_argument('mode', choices=['generate', 'query'], help='Mode to run the script in')
    parser.add_argument('--model', type=str, default='minilm', choices=model_choices.keys(), help='Model identifier to use for embeddings.')
    return parser.parse_args()

def generate_index_json(dimensions):
    """Generate JSON for MongoDB vector search index creation."""
    index_config = {
        "fields": [
            {
                "type": "vector",
                "path": "embeddings",
                "numDimensions": dimensions,
                "similarity": "cosine"
            }
        ]
    }
    return json.dumps(index_config, indent=2)

def main():
    args = parse_args()
    model, dimensions = get_model_info(args.model)
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['homedepot']
    collection = db['inventory']

    if args.mode == 'generate':
        # Drop the existing collection and create a new one
        db.drop_collection('inventory')
        collection = db['inventory']

        # Assuming items to encode are already fetched or known
        items = [{"_id": 1, "description": "An example description"}]  # Placeholder for actual data fetch

        # Generate embeddings and update MongoDB
        for item in items:
            embeddings = model.encode(item['description']).tolist()
            collection.insert_one({'_id': item['_id'], 'embeddings': embeddings})
            print(f"Updated Item ID {item['_id']} with embeddings.")

        # Print index creation JSON
        print("Please use the following JSON to create the vector search index in MongoDB Atlas:")
        print(generate_index_json(dimensions))

    elif args.mode == 'query':
        query = input("Enter your search query: ")
        query_embeddings = model.encode(query).tolist()
        
        # Perform Vector Search in MongoDB
        query_result = collection.aggregate([
            {
                '$vectorSearch': {
                    "index": "vector_index",
                    "path": "embeddings",
                    "queryVector": query_embeddings,
                    "numCandidates": 50,
                    "limit": 3
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'description': 1,
                    'score': {
                        '$meta': 'vectorSearchScore'
                    }
                }
            }
        ])
        
        # Print results
        results_found = False
        for item in query_result:
            print(item)
            results_found = True

        if not results_found:
            print("No results found for your query.")

if __name__ == "__main__":
    main()
