import sqlite3
import pandas as pd
from sklearn.metrics import pairwise_distances

# データベース接続
conn = sqlite3.connect('library.db')
cur = conn.cursor()

# 貸出履歴情報の取得
sql = """
SELECT lh.user_id, lh.book_id, bm.rating, lh.loan_date
FROM loan_history AS lh  -- Alias loan_history as lh
JOIN book_master AS bm ON lh.book_id = bm.book_id;  -- Alias book_master as bm
"""
df_history = pd.read_sql_query(sql, conn)

# ユーザー類似度計算
# ユーザーごとに借りた本のリストを作成
#user_books = df_history.groupby('user_id')['book_id'].tolist()

# Get the grouped data
grouped_books = df_history.groupby('user_id')['book_id']

# Extract book lists for each user and calculate similarity
user_books = []
for user_id, group_data in grouped_books:
    user_books.append(group_data.tolist())  # Convert group data to a list

# Find the maximum list length (number of books borrowed by a user)
max_book_count = max(len(user_list) for user_list in user_books)

# Pad shorter lists with a dummy value (e.g., -1) to ensure consistent length
user_books = [list(user_list) + [-1] * (max_book_count - len(user_list)) for user_list in user_books]

# ユーザー間の類似度をコサイン類似度で計算
#from sklearn.metrics import pairwise_distances
user_sim = 1 - pairwise_distances(user_books, metric='cosine')


# おすすめ書籍の算出
# 各ユーザーに対して、類似ユーザーが高評価した書籍を候補として抽出
def recommend_books(user_id):
  # 対象ユーザーの類似ユーザーを取得
  similar_users = user_sim[user_id, :].argsort()[::-1][1:]

  # Calculate the number of users representing the top 10%
  top_10_percent_count = int(len(similar_users) * 0.1)

  # Extract the top 10% of similar users
  top_10_percent_users = similar_users[:top_10_percent_count]

  print(f"Top 10% similar users for user {user_id}: {top_10_percent_users}")

  # 類似ユーザーが高評価した書籍のリストを作成
  candidate_books = []
#  for similar_user in similar_users:
#    candidate_books += user_books[similar_user]
  for similar_user in top_10_percent_users:
    candidate_books += user_books[similar_user]


  # 重複を除いた書籍IDのリストを作成
  candidate_books = list(set(candidate_books))

  # 候補書籍をレーティング値でソート
  df_candidates = df_history[df_history['book_id'].isin(candidate_books)]
  df_candidates = df_candidates.sort_values(by='rating', ascending=False)

  # おすすめ書籍のリストを返す
  recommended_books = df_candidates['book_id'].tolist()[:10]
  return recommended_books

# 特定のユーザーへのおすすめ書籍を表示
user_id = 1  # 例：ユーザーID1
recommended_books = recommend_books(user_id)
print(f"ユーザー {user_id} へのおすすめ書籍： {recommended_books}")
