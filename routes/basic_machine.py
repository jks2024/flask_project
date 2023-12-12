# 생성 분류 문제
import json
from sklearn.neighbors import KNeighborsClassifier
def bream_or_smelt():
    # 도미 데이터 준비
    bream_length = [25.4, 26.3, 26.5, 29.0, 29.0, 29.7, 29.7, 30.0, 30.0, 30.7, 31.0, 31.0,
                    31.5, 32.0, 32.0, 32.0, 33.0, 33.0, 33.5, 33.5, 34.0, 34.0, 34.5, 35.0,
                    35.0, 35.0, 35.0, 36.0, 36.0, 37.0, 38.5, 38.5, 39.5, 41.0, 41.0]
    bream_weight = [242.0, 290.0, 340.0, 363.0, 430.0, 450.0, 500.0, 390.0, 450.0, 500.0, 475.0, 500.0,
                    500.0, 340.0, 600.0, 600.0, 700.0, 700.0, 610.0, 650.0, 575.0, 685.0, 620.0, 680.0,
                    700.0, 725.0, 720.0, 714.0, 850.0, 1000.0, 920.0, 955.0, 925.0, 975.0, 950.0]

    # 빙어 데이터 준비
    smelt_length = [9.8, 10.5, 10.6, 11.0, 11.2, 11.3, 11.8, 11.8, 12.0, 12.2, 12.4, 13.0, 14.3, 15.0]
    smelt_weight = [6.7, 7.5, 7.0, 9.7, 9.8, 8.7, 10.0, 9.9, 9.8, 12.2, 13.4, 12.2, 19.7, 19.9]

    # 데이터 합치기
    length = bream_length + smelt_length # 도미와 빙어의 길이 데이터
    weight = bream_weight + smelt_weight # 도미와 빙어의 무게 데이터
    fish_data = [[l, w] for l, w in zip(length, weight)] # 도미와 빙어의 길이와 무게 데이터를 하나로 합침
    fish_target = [1] * 35 + [0] * 14  # 도미는 1, 빙어는 0

    # KNN 모델 훈련 및 평가
    kn = KNeighborsClassifier() # K-최근접 이웃 분류기 객체 생성
    kn.fit(fish_data, fish_target) # K-최근접 이웃 분류기 모델 훈련
    accuracy = kn.score(fish_data, fish_target) # 모델 평가

    # 데이터와 모델 결과 JSON 변환
    result_json = json.dumps({
        "fish_data": fish_data,
        "fish_target": fish_target,
        "accuracy": accuracy,
        "predict_example": int(kn.predict([[30, 600]])[0])
    })

    # JSON 데이터 출력
    print(result_json)
    return result_json