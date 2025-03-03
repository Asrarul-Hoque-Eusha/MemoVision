import pandas as pd
from enum import Enum

from services.vectordb import initialize_client

class CategoryVariables(str, Enum):
    collection_name = "text_collection"
    category = "category"
    csv_path = "./question.csv"

client = initialize_client()
def get_or_create_collection(get_collection_name):
    if get_collection_name not in client.list_collections():
        return client.create_collection(
            name=get_collection_name,
            metadata={"hnsw:space": "cosine"},
        )
    else:
        return client.get_collection(get_collection_name)

collection_name = CategoryVariables.collection_name
text_collection = get_or_create_collection(collection_name)

def add_to_text_collection(index, text, category):
    existing_image = text_collection.get(ids=[str(index)])
    if existing_image["ids"]:
        text_collection.update(
            ids=[str(index)],
            documents=[text],
            metadatas=[{CategoryVariables.category: category}],
        )
    else:
        text_collection.add(
            ids = [str(index)],
            documents = [text],
            metadatas = [{CategoryVariables.category : category}],
        )

def read_documents(file):
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        text = row["text"]
        category = row["category"]
        add_to_text_collection(index, text, category)

if text_collection.count() <= 200:
    read_documents(file = CategoryVariables.csv_path)

def find_query_type(query):
    results = text_collection.query(
        query_texts = [query],
        n_results = 1,
        include = ["metadatas"],
    )
    return results["metadatas"][0][0]['category']
