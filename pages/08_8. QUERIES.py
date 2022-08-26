import streamlit as st
import psycopg2
import pandas as pd
st.title("Query Cookbook")


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
    return pd.DataFrame(select_query_res, columns = select_cols), select_query

#### Data Source Page ####

# Initialize connection to postgres table
try:
    conn = init_connection()
except:
    st.error("Cannot Connect to Database. Check Connection and Try Again")



"### Objective: Average Employyee Tenure"

# collected all table names in current DB
table_res = run_query("""SELECT table_schema, table_name
                      FROM information_schema.tables
                      WHERE table_schema != 'pg_catalog'
                      AND table_schema != 'information_schema'
                      AND table_type='BASE TABLE'
                      ORDER BY table_schema, table_name""")
# parse out table names from results

"#### Data Source: Sample_HR"
table_names = [desc[1] for desc in table_res]

"##### SELECT Query"
select_table = st.selectbox("Table to Query", table_names)
tm = get_table_metadata(select_table)
tm_cols = [desc[0] for desc in tm]
select_fields = st.multiselect("Select fields to Query:",tm_cols )
if select_fields:
    fields = ", ".join(select_fields)
    q = " SELECT {fields} FROM {table};".format(fields = fields, table = select_table)
    res = run_query(q)
    st.write("**Query:** {}".format(q))
    df = pd.DataFrame(res, columns = select_fields)
    st.table(df)
else:
    res = get_pd_table(select_table)
    st.write("**Query:** SELECT * FROM {table};".format(table = select_table))
    st.table(res[0])
"##### COUNT Query"
counting_table = st.selectbox("Table to Query", table_names, key = "count_table")
query = "SELECT COUNT(*) FROM {};".format(counting_table)
st.write("**Query:** {}".format(query))
st.write("**Result:** {res}".format(res = run_query(query)[0][0]))
