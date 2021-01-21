# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import warnings
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#경고메시지 숨기기
#warnings.filterwarnings(action='ignore')

# 실행방법 python recommender_system.py 재료1 재료2 재료3 재료4 ... 건강정보1 건강정보2 ...
#arguments 들어오는 값들 newmenuarray에 저장
argnum = 0
newmenuarray = []
for arg in sys.argv:
    if argnum > 0:
        newmenuarray.append(arg)
    argnum = argnum + 1

data = pd.read_csv('./newexample3.csv')

#조회수 데이터(string형태) 중간에 ','로 나눈후 다시 합친후 int형으로 변환 
for i in range(data['조회수'].size):
    data['조회수'][i] = data['조회수'][i].split(',')
    data['조회수'][i] = "".join(data['조회수'][i])
    
#조회수데이터 int형으로 변환
data['조회수'] = pd.to_numeric(data['조회수'], errors='coerce')

data['재료'] = data['재료'].apply(literal_eval)
data['건강정보'] = data['건강정보'].apply(literal_eval)

data.loc[data['재료'].size] = ['새로운메뉴', '', '', '', newmenuarray, [], '', '']

#data['재료']에 건강정보까지 합침
for i in range(data['재료'].size):
    data['재료'][i] = " ".join(data['재료'][i]+data['건강정보'][i])
    #data['건강정보'][i] = " ".join(data['건강정보'][i])


def get_recommend_racipe_list(df, recipe_title, top=10):
    count_vector = CountVectorizer(ngram_range=(1, 3))
    c_vector_ingredient = count_vector.fit_transform(data['재료'])
    #코사인 유사도를 구한 벡터를 미리 저장
    ingredient_c_sim = cosine_similarity(c_vector_ingredient, c_vector_ingredient).argsort()[:, ::-1]
    # 재료와 건강정보가 일치하는 특정 레시피와 비슷한 레시피를 추천해야 하기 때문에 '특정 레시피' 정보를 뽑아낸다.
    target_recipe_index = df[df['이름'] == recipe_title].index.values
    #코사인 유사도 중 비슷한 코사인 유사도를 가진 정보를 뽑아낸다.
    sim_index = ingredient_c_sim[target_recipe_index, :top].reshape(-1)
    #본인을 제외
    sim_index = sim_index[sim_index != target_recipe_index].reshape(-1)
    #중복제거
    sim_index = np.asarray(list(set(sim_index)))
    #data frame으로 만들고 조회수로 정렬한 뒤 return
    result = df.iloc[sim_index].sort_values(by='조회수', ascending=False)[:10]
    return result

print("\n$$$$$$$$$$$$$$$$$$$$입력$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
print(newmenuarray)
print("\n@@@@@@@@@@@@@@@@@@@@출력@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(get_recommend_racipe_list(data, recipe_title='새로운메뉴'))
