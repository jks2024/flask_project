import json
import requests
from bs4 import BeautifulSoup
from flask import request
import datetime


def get_weather():
    url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    output = ""

    for loc in soup.select("location"):
        output += f"<h3>{loc.select_one('city').string}<h3>"
        output += f"날씨 : {loc.select_one('wf').string}</br>"
        output += f"최저/최고 기온 : {loc.select_one('tmn').string}/{loc.select_one('tmx').string}</br>"

    return output

def get_weather2():
    print("GET 요청을 받았습니다.")
    nx_val = request.args.get('x', default=None, type=None)
    ny_val = request.args.get('y', default=None, type=None)

    print("X : ", nx_val)
    print("Y : ", ny_val)
    API_KEY = 'LPh8U0fWWitEfCUYAQMCreTSbSbI4XqYB%2Bspk2jhS90QAcvAT1FforFEAfawd9rL4yV8Ecqs%2B0pv6G9eMYM5yA%3D%3D'
    API_KEY_decode = requests.utils.unquote(API_KEY)

    # 날짜 및 시간 설정
    now = datetime.datetime.now()

    # base_date에 날짜를 입력하기 위해 날짜를 출력 형식을 지정해 변수에 할당
    date = now.strftime('%Y%m%d')

    # base_time에 시간을 입력하기 위해 시간을 출력 형식을 지정해 변수에 할당
    time = now.strftime('%H%M')

    # 현재 분이 30분 이전이면 30분 전 시간으로 설정
    if now.minute < 30:
        now = now - datetime.timedelta(minutes=30)
        time = now.strftime('%H%M')
    else:
        time = now.strftime('%H%M')

    # 요청 주소 및 요청 변수 지정
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

    # 발표 일자 지정
    baseDate = date
    baseTime = time

    # 한 페이지에 포함된 결과 수
    num_of_rows = 6
    # 페이지 번호
    page_no = 1
    # 응답 데이터 형식 지정
    data_type = 'JSON'

    req_parameter = {'serviceKey': API_KEY_decode,
                     'nx': nx_val, 'ny': ny_val,
                     'base_date': baseDate, 'base_time': baseTime,
                     'pageNo': page_no, 'numOfRows': num_of_rows,
                     'dataType': data_type}

    # 요청 및 응답
    try:
        r = requests.get(url, params=req_parameter)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making a request: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

    # JSON 형태로 응답받은 데이터를 딕셔너리로 변환
    dict_data = r.json()

    # 출력을 이쁘게 하기 위해 json.dumps()를 사용하여 들여쓰기(indent) 옵션을 지정
    print(json.dumps(dict_data, indent=2))

    # 딕셔너리 데이터를 분석하여 원하는 데이터를 추출
    weather_items = dict_data['response']['body']['items']['item']

    print(f"[ 발표 날짜 : {weather_items[0]['baseDate']} ]")
    print(f"[ 발표 시간 : {weather_items[0]['baseTime']} ]")

    weather_data = {}

    # sky_value와 precipitation_value 변수 초기화
    sky_value = None
    precipitation_value = None

    for k in range(len(weather_items)):
        weather_item = weather_items[k]
        obsrValue = weather_item['obsrValue']

        if weather_item['category'] == 'T1H': # 기온
            weather_data['tmp'] = f"{obsrValue}℃"
        elif weather_item['category'] == 'REH': # 습도
            weather_data['hum'] = f"{obsrValue}%"
        elif weather_item['category'] == 'RN1': # 시간당 강수량
            weather_data['pre'] = f"{obsrValue}mm"
        # elif weather_item['category'] == 'SKY':  # 하늘 상태
            #sky_value = weather_item['obsrValue']
        elif weather_item['category'] == 'PTY':  # 강수 형태
            precipitation_value = weather_item['obsrValue']

        # print(f"하늘 상태 : {sky_value}")
        # print(f"강수 형태 : {precipitation_value}")

        #weather_data['sky'] = get_combined_weather(sky_value, precipitation_value)
    pty_type = ["없음", "비", "비/눈", "눈", "소나기", "빗방울", "빗방울/눈날림", "눈날림"]
    weather_data['pty'] = pty_type[int(precipitation_value)]

    # 딕셔너리를 JSON 형태로 변환, # ensure_ascii=False를 설정하여 JSON에 유니코드 문자 포함
    json_weather = json.dumps(weather_data, ensure_ascii=False, indent=4)
    return json_weather
