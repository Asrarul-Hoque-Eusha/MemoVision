import numpy as np
from PIL import Image
import chromadb
import os
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader

from services.filtering_query_result import filter_with_threshold
from services.ask_llama import generate_description, extract_keywords_from_text_query
from services.filtering_query_result import handle_keywords, filter_query
import constants
from models import IncludeEnum

# Initialize ChromaDB client
def initialize_client():
    create_client = chromadb.PersistentClient(path="./chroma_db_storage")
    return create_client

client = initialize_client()
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

# Ensure collection is loaded or created
def get_or_create_collection(get_collection_name, get_embedding_function, get_data_loader):
    # Check if the collection exists, if not, create it
    if get_collection_name not in client.list_collections():
        return client.create_collection(
            name=get_collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=get_embedding_function,
            data_loader=get_data_loader,
        )
    else:
        return client.get_collection(get_collection_name)

collection_name = IncludeEnum.collection_name
multimodal_collection = get_or_create_collection(collection_name, embedding_function, data_loader)


def add_to_db_collection(image, text, image_url):
    existing_image = multimodal_collection.get(ids=[image_url])
    if existing_image["ids"]:
        pass
    else:
        embeddings = embedding_function([np.array(image)])[0].tolist()
        multimodal_collection.add(
            ids = [image_url],
            documents = [text['description']],
            embeddings = [embeddings],
            metadatas = [{"tags" : text['tags']}],
        )

def get_image_details(filename):
    image_details = multimodal_collection.get(ids = [filename])
    print(image_details)
    if len(image_details['ids']) == 0:
        return IncludeEnum.empty_id.value, IncludeEnum.empty_string
    return image_details['documents'][0], image_details['metadatas'][0]['tags']

def get_filter_format(keywords):
    with_keywords, without_keywords = handle_keywords(keywords)
    where_clause = filter_query(with_keywords, without_keywords)
    return where_clause

def query_vector_db_without_filter(instructions_embedding, top_n = 5):
    results = multimodal_collection.query(
        query_embeddings=[instructions_embedding],
        n_results=top_n,
        include = [IncludeEnum.documents, IncludeEnum.metadata, IncludeEnum.distances]
    )
    return results

def query_vector_db(instructions_embedding, where_clause):
    top_n = 10
    results = multimodal_collection.query(
        query_embeddings=[instructions_embedding],
        n_results=top_n,
        where_document=where_clause,
        include=[IncludeEnum.documents, IncludeEnum.metadata, IncludeEnum.distances]
    )
    return results


def handle_where_clause_to_results(keywords, query_embeddings):
    where_clause = get_filter_format(keywords)
    print(where_clause)
    if where_clause:
        results = query_vector_db(query_embeddings, where_clause)
    else:
        results = query_vector_db_without_filter(query_embeddings)
    return results

def query_database(instructions = "", query_image = None):
    if instructions:
        instructions = instructions.lower()
    directory = IncludeEnum.directory
    if query_image is None:
        prompt = constants.text_query_keyword_extraction_prompt.format(instruction=instructions)
        keywords = extract_keywords_from_text_query(prompt)
        instructions_embedding = embedding_function([instructions])[0].tolist()
        results = handle_where_clause_to_results(keywords, instructions_embedding)
        results = filter_with_threshold(results)
    else:
        image_path = os.path.join(directory, query_image)
        image = Image.open(image_path)
        image = np.array(image)  #
        query_image_embedding = embedding_function([image])[0].tolist()
        if instructions is None:
            results = query_vector_db_without_filter(query_image_embedding)
            results = filter_with_threshold(results,0.456)
        else:
            prompt = constants.multimodal_query_keyword_extraction_prompt.format(instruction=instructions)
            keywords = generate_description(image_url=image_path, prompt=prompt)
            results = handle_where_clause_to_results(keywords, query_image_embedding)
            results = filter_with_threshold(results, 0.456)
    print(results)
    return instructions, results
