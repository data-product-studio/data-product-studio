import psycopg2
import pandas as pd
import streamlit as st

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


# run any query
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)
# given a correct plsql query, returns the results in a dict
def run_query_all(query, n=100):
    with conn.cursor() as cur:
        try:
          cur.execute(query)
          cur.connection.commit()
        except Exception as err:
            print(err)
            cur.connection.rollback()
        return cur.fetchall()

def run_query_none(query, n=100):
    with conn.cursor() as cur:
        try:
          cur.execute(query)
          cur.connection.commit()
        except Exception as err:
            print(err)
            cur.connection.rollback()
        return conn.cursor()

# get the cursor description from a given table, includes column names, datatype
# @st.experimental_memo(ttl=600)
def get_table_metadata(table):
    query = "SELECT * FROM {table} LIMIT 1".format(table = table)

    with conn.cursor() as cur:
        try:
            cur.execute(query)
            cur.connection.commit()
        except Exception as err:
            cur.connection.rollback()
        return cur.description

conn = init_connection()

run_query_none("DROP TABLE IF EXISTS test;") 
run_query_none("CREATE TABLE test (id SERIAL PRIMARY KEY, bi text, taxonomy text, url text);")
run_query_none("INSERT INTO test (bi, taxonomy, url) VALUES ('https://tabluea.com/ddsf','YTD Formula: sales since January 1st till now as a sum', 'https://data_product_studio/taxonomy/YTD');")
# run_query_none("INSERT INTO test (name) VALUES ('hello world2');")
# run_query_none("ALTER TABLE test ADD COLUMN foo int;")
# run_query_none("INSERT INTO test (name, foo) VALUES ('hello world2', 1);")
# run_query_none("INSERT INTO test (name, foo) VALUES ('hello world2', 2);")

test_meta = get_table_metadata('test')
select_cols = [desc[0] for desc in test_meta]
results_data = run_query_all("SELECT * FROM test")
df = pd.DataFrame(results_data, columns = select_cols)
st.table(df)

