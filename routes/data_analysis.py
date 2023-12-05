import csv
import json
from flask import jsonify


def demo_graph():
    f = open('./data/age.csv', encoding='cp949')
    data = csv.reader(f)
    for row in data:
        if '서울특별시 구로구 신도림동(1153051000)' == row[0]:
            json_data = json.dumps(row, ensure_ascii=False, indent=4)
            return json_data

def gender_data():
    # CSV 파일 읽기
    with open('./data/gender.csv', encoding='cp949') as f:
        reader = csv.reader(f)
        m = []
        f = []
        for row in reader:
            if '신도림' in row[0]:
                m = [-int(i) for i in row[3:104]]
                f = [int(i) for i in row[106:]]

    # JSON 형태로 데이터 변환
    data = {'male': m, 'female': f}
    return jsonify(data)