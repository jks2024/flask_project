from elasticsearch import Elasticsearch
from routes.movie import get_movie
import json

es = Elasticsearch("http://localhost:9200")
index_name = "movie"

# 영화 정보를 Elasticsearch에 전송
def send_to_elasticsearch():
    # get_movie() 함수에서 반환된 JSON 데이터를 파싱
    movie_data = json.loads(get_movie()) # JSON 문자열을 파이썬 객체로 변환
    # 각 영화 항목을 별도의 문서로 인덱싱
    for movie in movie_data:
        response = es.index(index=index_name, body=movie) # 인덱싱, 색인화 과정
        print(response)
    print("Data sent to Elasticsearch")

# 모든 영화 정보 검색
def get_movie_from_elasticsearch():
    search_body = {
        "query": {
            "match_all": {}
        },
        "size": 30
    }
    response = es.search(index="movie", body=search_body)

    # Elasticsearch 응답 객체에서 필요한 데이터 추출
    hits = response.get("hits", {}).get("hits", []) # 검색 결과 중에서 문서 목록을 가져옴
    result = [{"title": hit["_source"]["title"]} for hit in hits] # 검색 결과에서 영화 제목을 추출하여 리스트로 저장

    # 결과 데이터를 JSON 형식의 문자열로 변환
    response_json = json.dumps(result, ensure_ascii=False, indent=2)
    print("결과 : " + response_json)
    return response_json

# 영화 제목으로 검색
def get_movie_from_elasticsearch_by_title(title):
    search_body = {
        "_source": ["title"],
        "query": {
            "match_all": {}
        },
        "size": 30
    }
    response = es.search(index="movie", body=search_body)
    response_json = json.dumps(response, indent=2)
    print(response_json)
    return response_json
