import requests
import json
import random

# ElasticsearchのURL
url = 'http://localhost:9200/resume_for_rank_feature_2'

# インデックスの作成
index_settings = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "job_title": {"type": "rank_features"},
            "industry": {"type": "rank_features"},
            "skills": {"type": "rank_features"}
        }
    }
}

response = requests.put(url, headers={"Content-Type": "application/json"}, data=json.dumps(index_settings))
print(response.json())

# 職種、業種、スキルの具体的なデータ
job_titles = [
    "ソフトウェアエンジニア", "プロジェクトマネージャー", "データサイエンティスト",
    "フロントエンドエンジニア", "システムアナリスト", "UX/UIデザイナー",
    "ネットワークエンジニア", "セールスエンジニア", "データベースアドミニストレーター", "テクニカルライター"
]

industries = [
    "ITコンサルティング", "製造業", "金融業", "ヘルスケア", "教育",
    "小売業", "自動車産業", "エネルギー", "メディア・エンターテインメント", "不動産業"
]

skills = [
    "プログラミング（Python, Java）", "プロジェクト管理（アジャイル, スクラム）", "データ分析（SQL, R）",
    "クラウドコンピューティング（AWS, Azure）", "ウェブ開発（HTML, CSS, JavaScript）",
    "ネットワークセキュリティ", "データベース管理（MySQL, PostgreSQL）",
    "デザインツール（Adobe XD, Figma）", "ビジネス分析", "ソフトウェアテスト（ユニットテスト, 自動化テスト）"
]

# 職務経歴書データの投入
documents = []
for i in range(20, 31):  # 20~30件のデータ
    document = {
        "name": f"Candidate {i}",
        "job_title": {f"{job_title}": random.randint(1, 10) for job_title in job_titles},
        "industry": {f"{industry}": random.randint(1, 10) for industry in industries},
        "skills": {f"{skill}": random.randint(1, 10) for skill in skills}
    }
    documents.append(document)

for i, doc in enumerate(documents, 1):
    response = requests.put(f'{url}/_doc/{i}?refresh=true', headers={"Content-Type": "application/json"}, data=json.dumps(doc))
    print(response.json())

# rank_featureクエリを実行
rank_feature_query = {
    "query": {
        "bool": {
            "should": [
                {
                    "rank_feature": {
                        "field": "skills.プログラミング（Python, Java）",
                        "boost": 2.0  # スキルに高い重みを付与
                    }
                },
                {
                    "rank_feature": {
                        "field": "job_title.ソフトウェアエンジニア",
                        "boost": 1.5  # 職種に中程度の重みを付与
                    }
                },
                {
                    "rank_feature": {
                        "field": "industry.ITコンサルティング",
                        "boost": 1.0  # 業種に標準的な重みを付与
                    }
                }
            ]
        }
    }
}

response = requests.post(f'{url}/_search', headers={"Content-Type": "application/json"}, data=json.dumps(rank_feature_query))
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
