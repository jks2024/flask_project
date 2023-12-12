from flask import Flask
from flask_apscheduler import APScheduler
from elasticsearch import Elasticsearch
from flask_cors import CORS
from routes.data import get_data
from routes.weather import get_weather, get_weather2
from routes.query import get_query
from routes.item import get_path_item
from routes.movie import get_movie
from routes.data_analysis import demo_graph, gender_data
from routes.non_name_data import non_name_data, processed_data
from routes.basic_machine import bream_or_smelt
from routes.credit_rating import train_and_save_model, predict

import json

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://localhost:3000'])

scheduler = APScheduler() # 스케줄러 초기화
scheduler.init_app(app) # 스케줄러 초기화
scheduler.start() # 스케줄러 시작

def send_to_elasticsearch():
    es = Elasticsearch("http://localhost:9200")
    index_name = "movie"
    # get_movie() 함수에서 반환된 JSON 데이터를 파싱
    movie_data = json.loads(get_movie())
    # 각 영화 항목을 별도의 문서로 인덱싱
    for movie in movie_data:
        response = es.index(index=index_name, body=movie)
        print(response)
    print("Data sent to Elasticsearch")

# 매 분마다 실행
#scheduler.add_job(func=send_to_elasticsearch, trigger="cron", minute='*/1', id="get_movie")
# 5시간 마다 실행
#scheduler.add_job(func=send_to_elasticsearch, trigger="cron", hour='*/5', id="get_weather")

app.add_url_rule('/api/data', 'get_data', get_data, methods=['GET'])
app.add_url_rule('/api/weather', 'get_weather', get_weather, methods=['GET'])
app.add_url_rule('/api/weather2', 'get_weather2', get_weather2, methods=['GET'])
app.add_url_rule('/api/query', 'get_query', get_query, methods=['GET'])
app.add_url_rule('/api/item/<item_id>', 'get_path_item', get_path_item, methods=['GET'])
app.add_url_rule('/api/movie', 'get_movie', get_movie, methods=['GET'])
app.add_url_rule('/api/graph', 'demo_graph', demo_graph, methods=['GET'])
app.add_url_rule('/api/gender/<region>', 'gender_data', gender_data, methods=['GET'])
#app.add_url_rule('/api/non-name-data', 'non_name_data', non_name_data, methods=['GET'])
app.add_url_rule('/api/non-name-data', 'processed_data', processed_data, methods=['GET'])
app.add_url_rule('/api/basic-machine', 'bream_or_smelt', bream_or_smelt, methods=['GET'])
app.add_url_rule('/api/train', 'train_and_save_model', train_and_save_model, methods=['GET'])
app.add_url_rule('/api/predict', 'predict', predict, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
