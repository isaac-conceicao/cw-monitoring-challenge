import psycopg2 as pg
import pandas as pd

# open db connection
conn = pg.connect(
    host="your_host",
    database="monitoring_challenge",
    user="postgres",
    password="172839"
)

# create a cursor
cur = conn.cursor()

# create checkout_1 table
cur.execute("""
    CREATE TABLE checkout_1 (
        time VARCHAR(5),
        today INTEGER,
        yesterday INTEGER,
        same_day_last_week INTEGER,
        avg_last_week FLOAT,
        avg_last_month FLOAT
    );
""")

# create checkout_2 table
cur.execute("""
    CREATE TABLE checkout_2 (
        time TIME,
        today INTEGER,
        yesterday INTEGER,
        same_day_last_week INTEGER,
        avg_last_week FLOAT,
        avg_last_month FLOAT
    );
""")

conn.commit()

# Read CSV files
data_file1 = pd.read_csv("checkout_1.csv", encoding='latin-1')
data_file2 = pd.read_csv("checkout_2.csv", encoding='latin-1')

# insert csv data into checkout_1 table
for _, row in data_file1.iterrows():
    cur.execute("""
        INSERT INTO checkout_1 (time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (row["time"], row["today"], row["yesterday"], row["same_day_last_week"],
          row["avg_last_week"], row["avg_last_month"]))

# insert csv data into checkout_2 table
for _, row in data_file2.iterrows():
    cur.execute("""
        INSERT INTO checkout_1 (time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (row["time"], row["today"], row["yesterday"], row["same_day_last_week"],
          row["avg_last_week"], row["avg_last_month"]))

conn.commit()

# create joined_checkouts table
cur.execute("""
    CREATE TABLE joined_checkouts AS
    SELECT
        c2.time,
        c2.today,
        c2.yesterday,
        c1.yesterday AS "2d_ago",
        c2.same_day_last_week AS "7d_ago",
        c1.same_day_last_week AS "8d_ago"
    FROM
        checkout_1 c1
    JOIN checkout_2 c2 ON c1.today = c2.yesterday
    AND c1.time = c2.time;
""")

# query joined_checkouts
query = "SELECT * FROM joined_checkouts"
joined_checkouts = pd.read_sql_query(query, conn)

print(joined_checkouts.head())

# close db connection
cur.close()
conn.close()