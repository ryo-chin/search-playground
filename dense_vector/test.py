import requests
import json
import numpy as np

# ElasticsearchのURL
url = 'http://localhost:9200/dense_vector_index'

# インデックスの作成
index_settings = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "vector": {
                "type": "dense_vector",
                "dims": 3,  # 次元数を3に設定
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}

response = requests.put(url, headers={"Content-Type": "application/json"}, data=json.dumps(index_settings))
print(response.json())

# 3次元のベクトルをランダムに生成
def generate_random_vector(dim):
    return np.random.rand(dim).tolist()

# ドキュメントの作成
documents = []
for i in range(1, 21):  # 20件のデータ
    document = {
        "name": f"Document {i}",
        "vector": generate_random_vector(3)
    }
    documents.append(document)

# データの投入
for i, doc in enumerate(documents, 1):
    response = requests.put(f'{url}/_doc/{i}?refresh=true', headers={"Content-Type": "application/json"}, data=json.dumps(doc))
    print(response.json())

# 検索クエリベクトル
query_vector = generate_random_vector(3)

# dense_vectorクエリを実行
dense_vector_query = {
    "knn": {
        "field": "vector",
        "query_vector": query_vector,
        "k": 5,  # 近傍数を5に設定
        "num_candidates": 10  # 検索対象の候補数
    }
}

response = requests.post(f'{url}/_search', headers={"Content-Type": "application/json"}, data=json.dumps(dense_vector_query))
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
