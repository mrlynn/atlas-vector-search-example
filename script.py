import argparse
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Define static inventory data
# Define static inventory data with 30 items
inventory_data = [
    {"item_id": 1, "description": "Compact cordless drill, 12V", "category": "Tools", "price": 99.99},
    {"item_id": 2, "description": "Waterproof outdoor paint, blue", "category": "Paint", "price": 39.99},
    {"item_id": 3, "description": "Stainless steel garden shovel", "category": "Gardening", "price": 29.99},
    {"item_id": 4, "description": "LED floor lamp, adjustable brightness", "category": "Lighting", "price": 49.99},
    {"item_id": 5, "description": "Bamboo indoor flooring, 10 sq ft", "category": "Flooring", "price": 59.99},
    {"item_id": 6, "description": "Ergonomic office chair with lumbar support", "category": "Furniture", "price": 199.99},
    {"item_id": 7, "description": "Heavy-duty extension cord, 50ft", "category": "Tools", "price": 34.99},
    {"item_id": 8, "description": "Organic potting mix, 50lb bag", "category": "Gardening", "price": 22.99},
    {"item_id": 9, "description": "Industrial air compressor 5 HP", "category": "Tools", "price": 889.99},
    {"item_id": 10, "description": "Designer table lamp, modern aesthetic", "category": "Lighting", "price": 120.50},
    {"item_id": 11, "description": "Wireless doorbell with two receivers", "category": "Electronics", "price": 24.99},
    {"item_id": 12, "description": "Smart thermostat with Wi-Fi feature", "category": "Electronics", "price": 249.99},
    {"item_id": 13, "description": "Electric pressure washer 1800 PSI", "category": "Tools", "price": 150.99},
    {"item_id": 14, "description": "Luxury silk curtains 90-inch length", "category": "Home Decor", "price": 85.99},
    {"item_id": 15, "description": "Robotic vacuum cleaner with app control", "category": "Electronics", "price": 299.99},
    {"item_id": 16, "description": "Rustic wooden coffee table", "category": "Furniture", "price": 219.95},
    {"item_id": 17, "description": "Professional gas chainsaw 60cc", "category": "Tools", "price": 239.99},
    {"item_id": 18, "description": "Luxury goose down comforter king size", "category": "Bedding", "price": 179.99},
    {"item_id": 19, "description": "Multi-purpose kitchen blender 6-speed", "category": "Appliances", "price": 99.99},
    {"item_id": 20, "description": "Professional ceramic hair straightener", "category": "Beauty", "price": 79.99},
    {"item_id": 21, "description": "Non-stick cookware set 10 pieces", "category": "Kitchen", "price": 129.99},
    {"item_id": 22, "description": "Outdoor patio heater 48000 BTU", "category": "Garden", "price": 149.99},
    {"item_id": 23, "description": "Decorative outdoor string lights, 48 ft", "category": "Lighting", "price": 59.99},
    {"item_id": 24, "description": "Ultralight camping tent for 4 persons", "category": "Outdoors", "price": 99.99},
    {"item_id": 25, "description": "Wall-mounted coat rack with shelf", "category": "Home Decor", "price": 45.99},
    {"item_id": 26, "description": "Adjustable dumbbell set, up to 40 lbs", "category": "Fitness", "price": 399.99},
    ]


# Dictionary to map model identifiers to model names and their dimensions
model_choices = {
    'minilm': ('all-MiniLM-L6-v2', 384),
    'distilbert': ('distilbert-base-nli-stsb-mean-tokens', 768),
    'roberta': ('stsb-roberta-large', 1024),
    'msmarco': ('msmarco-distilbert-base-v2', 768)  # Added model
}

def get_model_info(model_key):
    """Retrieve model info based on the model key."""
    model_name, dimensions = model_choices.get(model_key, ('all-MiniLM-L6-v2', 384))  # Default to MiniLM if key not found
    model = SentenceTransformer(model_name)
    return model, dimensions

def parse_args():
    parser = argparse.ArgumentParser(description="Run the data loading, embedding generation, or query.")
    parser.add_argument('mode', choices=['load', 'generate', 'query'], help='Mode to run the script in')
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
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['homedepot']
    collection = db['inventory']

    if args.mode == 'load':
        # Drop the existing collection and create a new one
        db.drop_collection('inventory')
        collection = db['inventory']
        # Insert the static data
        collection.insert_many(inventory_data)
        print("Loaded data into MongoDB collection 'inventory'.")

    elif args.mode == 'generate':
        model, dimensions = get_model_info(args.model)
        # Generate embeddings for the existing data in MongoDB
        for item in collection.find({}):
            embeddings = model.encode(item['description']).tolist()
            collection.update_one({'_id': item['_id']}, {'$set': {'embeddings': embeddings}})
            print(f"Generated embeddings for Item ID {item['_id']}.")

        # Provide JSON for creating the vector search index
        print("Please use the following JSON to create the vector search index in MongoDB Atlas:")
        print(generate_index_json(dimensions))

    elif args.mode == 'query':
        model, _ = get_model_info(args.model)
        query = input("Enter your search query: ")
        query_embeddings = model.encode(query).tolist()
        # Perform Vector Search in MongoDB
        query_result = collection.aggregate([
            {
                '$vectorSearch': {
                    "index": "vector_index",  # Replace with your actual index name
                    "path": "embeddings",
                    "queryVector": query_embeddings,
                    "numCandidates": 50,  # Adjust the number of candidates as needed
                    "limit": 3  # You can adjust the limit based on how many results you want
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
