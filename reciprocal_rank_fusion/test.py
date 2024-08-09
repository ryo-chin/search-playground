import requests
import json

# ElasticsearchのURL
ES_URL = 'http://localhost:9200'
INDEX_NAME = 'rrf_example_index'

# インデックスの作成
def create_index():
    index_settings = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "vector": {
                    "type": "dense_vector",
                    "dims": 3,  # ベクトルの次元数
                    "index": True,
                    "similarity": "l2_norm",
                    "index_options": {"type": "hnsw"}
                },
                "integer": {"type": "integer"}
            }
        }
    }
    response = requests.put(f'{ES_URL}/{INDEX_NAME}', headers={"Content-Type": "application/json"}, data=json.dumps(index_settings))
    print('Index creation response:', response.json())

# テストデータの投入
def index_documents():
    documents = [
        {"id": 1, "text": "rrf", "vector": [5, 1, 2], "integer": 1},
        {"id": 2, "text": "rrf rrf", "vector": [4, 2, 3], "integer": 2},
        {"id": 3, "text": "rrf rrf rrf", "vector": [3, 3, 4], "integer": 1},
        {"id": 4, "text": "rrf rrf rrf rrf", "vector": [2, 4, 5], "integer": 2},
        {"id": 5, "vector": [1, 5, 6], "integer": 1}
    ]
    
    for doc in documents:
        response = requests.put(f'{ES_URL}/{INDEX_NAME}/_doc/{doc["id"]}', headers={"Content-Type": "application/json"}, data=json.dumps(doc))
        print(f'Document {doc["id"]} indexing response:', response.json())
    
    # インデックスをリフレッシュしてすぐに検索可能にする
    response = requests.post(f'{ES_URL}/{INDEX_NAME}/_refresh')
    print('Index refresh response:', response.json())

# RRFを使用した検索の実行
def search_with_rrf():
    query = {
        "retriever": {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": {
                                "term": {
                                    "text": "rrf"
                                }
                            }
                        }
                    },
                    {
                        "knn": {
                            "field": "vector",
                            "query_vector": [3, 3, 3],
                            "k": 5,
                            "num_candidates": 5
                        }
                    }
                ],
                "rank_window_size": 5,
                "rank_constant": 1
            }
        },
        "size": 3,
        "aggs": {
            "int_count": {
                "terms": {
                    "field": "integer"
                }
            }
        }
    }
    
    response = requests.post(f'{ES_URL}/{INDEX_NAME}/_search', headers={"Content-Type": "application/json"}, data=json.dumps(query))
    print('Search response:', json.dumps(response.json(), ensure_ascii=False, indent=2))

# 実行フロー
if __name__ == "__main__":
    # インデックス作成
    create_index()
    # ドキュメントの投入
    index_documents()
    # RRFを使用した検索
    search_with_rrf()
