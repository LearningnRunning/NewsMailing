from PyNaver import Naver
from auth import *
import pandas as pd
import re

def remove_special_characters(input_string):
    # Replace all special characters (except spaces) with an empty string
    return re.sub(r'[^\w\s]', '', input_string)

def main(query):
    # 애플리케이션 인증 정보
    client_id = NaverClientId
    client_secret = NaverClientSecret

    # 네이버 API 인스턴스 생성
    api = Naver(client_id, client_secret)

    # 파라미터
    display = 15
    sort = "sim" # date

    # 실행
    df = api.search_news(query, display=display, sort=sort)

    df['pubDate'] = pd.to_datetime(df['pubDate'])
    df['Date']= df['pubDate'].dt.date
    df['Time']= df['pubDate'].dt.time

    df = df[['title', 'description','link','Date','Time']]
    df['title'] = df['title'].apply(remove_special_characters)
    df['description'] = df['description'].apply(remove_special_characters)
    df['keyword'] = query
    df.to_csv("./data/TodayNews.csv", index=False, encoding="utf-8-sig")
    all_df = pd.read_csv("./data/AllNews.csv")
    all_df = pd.concat([df, all_df])
    all_df.drop_duplicates(subset=['title', 'description','link','Date','Time'], keep="first")
    all_df.sort_values(by=['Date','Time'], inplace=True, ascending=False)
    all_df.to_csv("./data/AllNews.csv", index=False, encoding="utf-8-sig")

if __name__=="__main__":
    query = "즉시배송+이커머스+"
    main(query)