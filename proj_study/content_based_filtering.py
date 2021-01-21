import pandas as pd
import ast

data = pd.read_csv('tmdb_5000_movies.csv')

data = data[['id', 'genres', 'vote_average', 'vote_count', 'popularity', 'title', 'keywords', 'overview']]

m = data['vote_count'].quantile(0.9)

data = data.loc[data['vote_count'] >= m]

C = data['vote_average'].mean()

print(data.head(2))

def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m)*R) + (m/(m+v) * C)


data['score'] = data.apply(weighted_rating, axis=1)

print(type(data['score'][1]))

data['genres'] = data['genres'].apply(ast.literal_eval)

print(data['genres'], '\n===========================\n')
print(data['genres'][0], '\n===========================\n')
data['keywords'] = data['keywords'].apply(ast.literal_eval)

data['genres'] = data['genres'].apply(lambda x : [d['name'] for d in x]).apply(lambda x : " ".join(x))
print(data['genres'], '\n===========================\n')
print(type(data['genres']))
print(type(data['genres'][0]))
print(data['genres'][0])
print(data['genres'][1],'\n===========================\n')
data['keywords'] = data['keywords'].apply(lambda x : [d['name'] for d in x]).apply(lambda x : " ".join(x))

from sklearn.feature_extraction.text import CountVectorizer

count_vector = CountVectorizer(ngram_range=(1,3))
c_vector_genres = count_vector.fit_transform(data['genres'])

from sklearn.metrics.pairwise import cosine_similarity

gerne_c_sim = cosine_similarity(c_vector_genres, c_vector_genres).argsort()[:, ::-1]

def get_recommend_movie_list(df, movie_title, top=30):
    target_movie_index = df[df['title'] == movie_title].index.values
    print(target_movie_index, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sim_index = gerne_c_sim[target_movie_index, :top].reshape(-1)
    sim_index = sim_index[sim_index != target_movie_index]
    result = df.iloc[sim_index].sort_values('score', ascending=False)[:10]
    return result

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(get_recommend_movie_list(data, movie_title='The Dark Knight Rises'))