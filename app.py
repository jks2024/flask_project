from flask import Flask
from flask_apscheduler import APScheduler
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
from routes.elastic import send_to_elasticsearch, get_movie_from_elasticsearch_by_title, get_movie_from_elasticsearch

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://localhost:8111'])

scheduler = APScheduler() # 스케줄러 초기화
scheduler.init_app(app) # 스케줄러 초기화
scheduler.start() # 스케줄러 시작

# 매 분마다 실행
# scheduler.add_job(func=send_to_elasticsearch, trigger="cron", minute='*/1', id="get_movie")
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
app.add_url_rule('/api/elastic', 'send_to_elasticsearch', send_to_elasticsearch, methods=['GET'])
app.add_url_rule('/api/el_movie/<title>', 'get_movie_from_elasticsearch_by_title', get_movie_from_elasticsearch_by_title, methods=['GET'])
app.add_url_rule('/api/el_movie', 'get_movie_from_elasticsearch', get_movie_from_elasticsearch, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
