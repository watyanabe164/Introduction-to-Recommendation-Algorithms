import random
import pandas as pd
import sqlite3

# データ件数
num_users = 100  # ユーザー数
num_books = 1000  # 書籍数
num_loans = 10000  # 貸出件数

# データベース接続
conn = sqlite3.connect('library.db')
cur = conn.cursor()

# ユーザー情報生成
user_ids = list(range(1, num_users + 1))
user_names = [f"ユーザー{i}" for i in user_ids]

# 書籍情報生成
book_ids = list(range(1, num_books + 1))
book_titles = [f"書籍{i}" for i in book_ids]
ratings = [random.randint(1, 5) for _ in book_ids]

# 貸出履歴情報生成
loan_dates = [pd.to_datetime('2023-01-01') + pd.DateOffset(days=random.randint(0, 365)) for _ in range(num_loans)]
loan_date_strings = [date.strftime('%Y-%m-%d') for date in loan_dates]
loan_data = pd.DataFrame({
    "user_id": [random.choice(user_ids) for _ in range(num_loans)],
    "book_id": [random.choice(book_ids) for _ in range(num_loans)],
    "loan_date": loan_date_strings
})

# ユーザー情報テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS user_info (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL
);
""")

# 書籍情報テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS book_master (
    book_id INTEGER PRIMARY KEY,
    book_title TEXT NOT NULL,
    rating INTEGER NOT NULL
);
""")

# 貸出履歴テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS loan_history (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TEXT  NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id),
    FOREIGN KEY (book_id) REFERENCES book_master(book_id)
);
""")


# ユーザー情報登録
cur.executemany("""
INSERT INTO user_info (user_id, user_name) VALUES (?, ?);
""", [(user_id, user_name) for user_id, user_name in zip(user_ids, user_names)])

# 書籍情報登録
cur.executemany("""
INSERT INTO book_master (book_id, book_title, rating) VALUES (?, ?, ?);
""", [(book_id, book_title, rating) for book_id, book_title, rating in zip(book_ids, book_titles, ratings)])

# 貸出履歴登録
cur.executemany("""
INSERT INTO loan_history (user_id, book_id, loan_date) VALUES (?, ?, ?);
""", loan_data.values)

# コミットとクローズ
conn.commit()
conn.close()

print("サンプルデータ作成完了")
