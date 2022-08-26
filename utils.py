import streamlit as st

def print_hello():
    st.write("Hello World")
    return 1


#### Functions to connect to DB ####

# make sure "secretes.tohml" file includes db connection criteria
# TODO: Dynamically handle cursor

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


# run any query
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
# given a correct plsql query, returns the results in a dict
def run_query(query, n=100):
    with conn.cursor() as cur:
        try:
            cur.execute(query)
            cur.connection.commit()
        except Exception as err:
            print(err)
            cur.connection.rollback()
        return cur.fetchall()

# get the cursor description from a given table, includes column names, datatype
@st.experimental_memo(ttl=600)
def get_table_metadata(table):
    query = "SELECT * FROM {table} LIMIT 1".format(table = table)

    with conn.cursor() as cur:
        try:
            cur.execute(query)
            cur.connection.commit()
        except Exception as err:
            cur.connection.rollback()
        return cur.description


# given a table name, select all in the table and convert to a pandas df
def get_pd_table(table_name):
    select_query = "SELECT * FROM {table}".format(table = table_name)
    select_query_res= run_query(select_query)
    # select_query_res
    select_cols = get_table_metadata(table_name)
    select_cols = [desc[0] for desc in select_cols]
    # create and display dataframe
    return pd.DataFrame(select_query_res, columns = select_cols)

#### Data Source Page ####
