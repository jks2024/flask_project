import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from flask import Flask, request, jsonify
from joblib import dump, load

# 사전 학습 단계
def train_and_save_model():
    # 데이터 불러오기
    df = pd.read_csv('./data/filtered.csv')
    df.replace('*', pd.NA, inplace=True) # * 문자열을 결측치로 변환
    df.dropna(inplace=True) # 결측치가 있는 행 제거

    # 타겟 변수와 특성 분리
    X = df.drop('CB', axis=1)
    y = df['CB']

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 데이터 정규화
    scaler = StandardScaler() # 스케일러 객체 생성
    X_train = scaler.fit_transform(X_train) # 학습 데이터에 스케일러 적용

    # 모델 학습
    model = RandomForestClassifier(random_state=42) # 랜덤 포레스트 모델
    model.fit(X_train, y_train) # 모델 학습

    # 모델과 스케일러 저장
    dump(model, 'trained_model.joblib')
    dump(scaler, 'scaler.joblib')

    return "Model and scaler saved successfully."

# 예측 단계
def predict():
    # 모델과 스케일러 불러오기
    model = load('trained_model.joblib')
    scaler = load('scaler.joblib')

    # 예측에 사용할 데이터 불러오기
    data = request.get_json(force=True)

    # 타겟 변수 'CB' 제외
    if 'CB' in data:
        del data['CB']

    # 수정된 데이터로 데이터프레임 생성
    df = pd.DataFrame([data])

    # 데이터 정규화
    df = scaler.transform(df)

    # 예측
    prediction = model.predict(df)

    # 예측 결과를 Python 기본 int 타입으로 변환
    prediction = [int(p) for p in prediction]

    return jsonify({'prediction': list(prediction)})