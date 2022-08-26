import streamlit as st
import psycopg2
import pandas as pd
st.title("Data Sources")


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

# Initialize connection to postgres table
try:
    conn = init_connection()
except:
    st.error("Cannot Connect to Database. Check Connection and Try Again")

# create connection details


db_name = "sample_hr"
conn_string = "postgresql://localhost:5432/{dbname}?user=[USER]&password=[PASSWORD]".format(dbname= db_name)

st.write("""#### The *Average Employee Tenure* objective uses the following data sources
- {db_name} : [{conn}]({conn})
""".format(db_name = db_name, conn = conn_string))

"#### The tables used in this caclulation:"
table_choice = st.radio( "", ('employees', 'jobs'))
"##### Table Metadata"
tm = get_table_metadata(table_choice)
tm_cols = [desc[0] for desc in tm]
tm_OID = [str(desc[1]) for desc in tm]
tmdata = {"Field Name": tm_cols, "OID": tm_OID }
df = pd.DataFrame(tmdata)
df
