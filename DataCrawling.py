from time import strftime

from bs4 import BeautifulSoup
import requests
import re # 파이썬 기본
import pandas as pd
import datetime # 파이썬 기본

# from unicodedata import category
# from urllib3 import request

category = ['Politics', 'Ecomnomic', 'Social', 'Culture', 'World', 'IT']

#url = 'https://news.naver.com/section/100'
#      'https://news.naver.com/section/101' # 경제 면 추가
#      'https://news.naver.com/section/102' # 사회 면 추가
#resp = requests.get(url) # 서버에 요청을한다 html문서
# 뉴스 제목만 가져오려고 한다)
#print(list(resp))

#응답받은 디스퀀스를 \
#soup = BeautifulSoup(resp.text, 'html.parser') # hd
#print(soup)

#title_tags = soup.select('.sa_text_strong')
#print(title_tags[0].text)

df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)  # 서버에 요청을한다 html문서
    soup = BeautifulSoup(resp.text, 'html.parser')  # hd
    title_tags = soup.select('.sa_text_strong') # 제목만 따오고
    titles = [] # 이걸 빼먹음# !!
    for title_tag in title_tags:
        title = title_tag.text
        title = re.compile('[^가-힣 ]').sub('', title)
                # 가-힣 뒤에 띄어쓰기 해야함 / ^가-힣(공백) 을 제외한 것을
                # sub(빼라)(''널문로 채워라, 타이틀에)
        titles.append(title)


    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index = True)
# df가 포문에 있어서 자꾸 중복됨

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d')), index=False)
