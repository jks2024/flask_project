import pandas as pd
import json

def non_name_data():
    df = pd.read_csv('./data/220900_DB_RAW.csv')

    # print(df.head())
    # selected_columns = [
    #     "식별구분", "PRE_LMT", "PRE_RT", "GOODS_CD", "INA_CD", "AD_NO", "LIV_ADD", "RES_ADD", "ADD_YN", "SALE_TRM", "RRC_CD", "HAC_CD", "B12000100",
    #     "B22000200", "B22000300", "B32000100", "BS0000164", "BS0000772", "BS0000930", "C00000001", "C00000023",
    #     "C00000035", "C00000052", "C00000090", "C00000093", "C11061000", "CA1200001", "CA2400001", "CA3600001",
    #     "CE0000004", "CF0100902", "CF0100906", "CF0100919", "CF0100932", "CF0300611", "CF0300902", "CF0331605",
    #     "CF0332605", "CF0600157", "CF0600611", "CF0600615", "CF0600913", "CF0600943", "CF0631605", "CF0632605",
    #     "CF1200619", "CF1200620", "CF1200622", "CF1200902", "CF1200946", "CF1231601", "CF1231602", "CF1231604",
    #     "CF1231605", "CF1232601", "CF1232602", "CF1232604", "CF1232605", "CF9900907", "CL0631905", "CL0631906",
    #     "CS0000050", "DQ0052001", "DQ0152001", "DQ0352001", "DQ0352601", "DQ0652001", "DQ0652601", "DQ1200001",
    #     "DQ1251001", "DQ1251011", "DQ1252001", "DQ1252004", "DQ1252601", "G00000001", "G00010001", "G00060001",
    #     "GU0024001", "IDT000003", "KC1000001", "KC1000025", "KC5000016", "KC5000017", "KC5000019", "KC5000020",
    #     "KC5000021", "L00000001", "L00000002", "L00000004", "L00060002", "L00080002", "L00140002", "L00990004",
    #     "L00990005", "L21170900", "L21171100", "L21200200", "L21211300", "L22000500", "L22000900", "L22001700",
    #     "L22001800", "L22001900",
    #     "L22002000", "L22002005", "L22002011", "L22002012", "L22002013", "L22002014", "L22002700", "L22002800",
    #     "L22002900", "L22003000", "L22003100", "L22003200", "L23001901", "L23001909", "L23001911", "L23001916",
    #     "L23003700", "L2A000105", "LA0000038", "LA0000039", "LA0000040", "LA0052601", "LA0052602", "LA0099212",
    #     "LA0099227", "LA1200017", "LA1200018", "LA1200019", "LA1200020", "LA1200021", "LA1200022", "LA6000005",
    #     "LC0000001", "LC0000002", "LC0000021", "LC0000101", "LC0000202", "LC0000607", "LC0017001", "LC0017201",
    #     "LC0021001", "LC0021010", "LC0021102", "LC0021103", "LC0021602", "LC0025002", "LC0025018", "LC0025202",
    #     "LC0027001", "LC0027002", "LC0027010", "LC0027021", "LC0027023", "LC0099020", "LC0099024", "LC0099045",
    #     "LC0099046", "LC0099047", "LC0099101", "LC0099103", "LC0099901", "LC1200102", "LC1221101", "LC2421801",
    #     "LE0000213", "LH0000013", "LH0000147", "LH0000151", "LH0000154", "LRZ021201", "LS0000067", "LS0000124",
    #     "LS0000125", "LS0000176", "LS0000180", "LS0000574", "LS0000864", "LS0000866", "LS0000892", "LS0001144",
    #     "LS0001196", "LS0001197", "LU0024001", "LU0024101", "LU0024201", "LU0624001", "P27000100", "P3O000500",
    #     "P3O003900", "P44003901", "PE0000025", "PE0000026", "PH0000092", "PS0000090", "PS0000279", "PS0000282",
    #     "PS0000500", "PS0001894", "PS0001895", "PS0001896", "PS0001897", "CB", "SP", "결과값(연체회차)"
    #]
    required_columns = [
        "HAC_CD",    # 직업 구분 (1:급여소득자, 2:개인사업자, 3:연금소득자, 4:주부, 5:전문직, 7:프리랜서, 8:무직, 9:기타)
        "B22000200", # (채무불이행-신용정보사)미해제등록 총 건수
        "B32000100", # (채무불이행/공공+금융질서문란)등록 총 건수
        "DQ0052001", # 대부업계 30일이상 연체 미해제 총 건수
        "KC5000016", # 최근 3개월내 경험 최장 연체일수
        "C00000001", # 최근3년내 미해지 신용카드 총건수
        "L00000001", # 미상환 대출총건수
        "CF0100902", # 최근1개월 신용카드 일시불이용률(15일기준)
        "CF0300611", # 최근3개월 신용카드 현금서비스사용개월수(15일기준)
        "KC1000001", # 총신용공여
        "KC1000025", # 총신용공여 건수
        "L00000002", # 미상환 대출총금액
        "L23001911", # 최근 미상환 주택담보제외 대출개설일로부터의 기간
        "CA1200001", # 최근1년내신용카드개설기관수
        "CF0600943", # 최근6개월 신용카드 현금서비스이용률(15일기준)
        "BS0000164", # 신용회복지원여부
        "PS0000500", # 최근6개월내 해제연체 중 최장연체일수
        "PS0001895", # 최근3개월내 경험한 연체 총 건수(10만원미만제외)
        "PE0000025", # 최근3개월내 경험한 최장 연체경험기간
        "CB", # NICE, KCB에서 제공하는 신용평가 등급(1~10등급)
        "SP", # 대부업권 대출을 이용 중인 고갟을 대상으로 하는 신용평가 등급(1~10등급)
        ]


    # 선택한 컬럼으로 데이터프레임 필터링
    filtered_df = df[required_columns]
    filtered_df.to_csv('./data/filtered.csv', index=False)
    # 데이터프레임을 JSON 형식으로 변환
    # json_data = filtered_df.to_json(orient='records', force_ascii=False)
    # print(json_data)
    # return json_data

    # pretty_json = json.dumps(json_data, indent=4, ensure_ascii=False)
    # return pretty_json

def processed_data():
    df = pd.read_csv('./data/filtered.csv')
    print(df.head())
    # 데이터프레임을 JSON 형식으로 변환
    json_data = df.to_json(orient='records', force_ascii=False)
    print(json_data)
    return json_data