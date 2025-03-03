import re
from enum import Enum

from models import IncludeEnum

class QueryOperator(str, Enum):
    where_and = "$and"
    where_or = "$or"
    contains = "$contains"
    not_contains = "$not_contains"

class FilterPatterns(str, Enum):
    filter_words = ", . none output not having similar no keywords keyword included include exclude excluded without avoid dissimilar first line second photos image photo images pictures pic picture pics"

def filter_with_threshold(query_result, threshold = 0.80):
    max_image = 5
    max_mismatch = 1
    filtered_ids = []
    filtered_documents = []
    filtered_distances = []
    for i, dist in enumerate(query_result['distances'][0]):
        if dist < threshold and len(filtered_ids) < max_image:
            filtered_ids.append(query_result['ids'][0][i])
            filtered_documents.append(query_result['documents'][0][i])
            filtered_distances.append(dist)
    return {
        IncludeEnum.ids: [filtered_ids],
        IncludeEnum.documents: [filtered_documents],
        IncludeEnum.distances: [filtered_distances]
    }

def handle_keyword_type(keywords):
    if isinstance(keywords, str) and len(keywords) > 1:
        keywords = keywords.split(" ")
    elif len(keywords) == 1:
        keywords = keywords
    elif isinstance(keywords, list):
        keywords = keywords
    else:
        keywords = []
    return keywords

def keyword_validation(keywords):
    remove = [None, '', "", " ", "\n"] + FilterPatterns.filter_words.value.split()
    if len(keywords) == 0:
        return []
    else:
        return [keyword for keyword in keywords if keyword not in remove]

def handle_keywords(keywords):
    if isinstance(keywords, str):
        keywords = keywords.lower()
        keywords = re.sub(r'[^a-zA-Z\s]', '', keywords)
        keywords = keywords.split("\n")

    if len(keywords) > 1:
        with_keywords = handle_keyword_type(keywords[0])
        without_keywords = handle_keyword_type(keywords[1])
    elif len(keywords) == 1:
        with_keywords = handle_keyword_type(keywords[0])
        without_keywords = []
    else:
        with_keywords = []
        without_keywords = []
    with_keywords = keyword_validation(with_keywords)
    without_keywords = keyword_validation(without_keywords)
    return with_keywords, without_keywords

def filter_query(with_keywords, without_keywords):
    if with_keywords == [] and without_keywords == []:
        where_clause = False
    elif with_keywords == [] and without_keywords != []:
        if len(without_keywords) == 1:
              where_clause = {
                  QueryOperator.not_contains: without_keywords[0]
              }
        else:
              where_clause = {
                  QueryOperator.where_and: [{QueryOperator.not_contains: kw} for kw in without_keywords]
              }
    elif with_keywords != [] and without_keywords == []:
        if len(with_keywords) == 1:
              where_clause = {
                  QueryOperator.contains: with_keywords[0]
              }
        else:
              where_clause = {
                  QueryOperator.where_or: [{QueryOperator.contains: kw} for kw in with_keywords]
              }
    else:
        if len(with_keywords) == 1 and len(without_keywords) == 1:
            where_clause = {
                  QueryOperator.where_and: [
                      {QueryOperator.contains: with_keywords[0]},
                      {QueryOperator.not_contains: without_keywords[0]}
                  ]
            }
        elif len(with_keywords) == 1 and len(without_keywords) > 1:
            where_clause = {
                  QueryOperator.where_and: [
                      {QueryOperator.contains: with_keywords[0]},
                      {QueryOperator.where_and: [{QueryOperator.not_contains: kw} for kw in without_keywords]}
                  ]
            }
        elif len(with_keywords) > 1 and len(without_keywords) == 1:
            where_clause = {
                  QueryOperator.where_and: [
                      {QueryOperator.where_or: [{QueryOperator.contains: kw} for kw in with_keywords]},
                      {QueryOperator.not_contains: without_keywords[0]}
                  ]
            }
        else:
            where_clause = {
                QueryOperator.where_and: [
                    {QueryOperator.where_or: [{QueryOperator.contains: kw} for kw in with_keywords]},
                    {QueryOperator.where_and: [{QueryOperator.not_contains: kw} for kw in without_keywords]}
                ]
            }
    return where_clause
