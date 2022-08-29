import streamlit as st
import psycopg2

#### Functions to connect to DB ####

# make sure "secretes.tohml" file includes db connection criteria
# TODO: Dynamically handle cursor

# Initialize connection.
# https://docs.streamlit.io/library/advanced-features/caching#example-1-pass-a-database-connection-around
@st.cache(allow_output_mutation=True)
def init_connection(db):
    return psycopg2.connect(**st.secrets[db])

# run file given location
def execute_query(query, conn, f = False):
    # if not given a file to execute
    with conn.cursor() as cur:
        if not f:
            try:
                res = cur.execute(query)
                cur.connection.commit()
                cur.close()
                return res
            except Exception as err:
                st.warning(err)
                cur.connection.rollback()
        # if is a file
        else:
            try:
                res = cur.execute(open(query, "r").read())
                cur.connection.commit()
                cur.close()
                return res
            except Exception as err:
                st.warning(err)
                cur.connection.rollback()



# run any query
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# given a correct plsql query, returns the results in a dict
# Only works for queries that return more than one row
def exectute_query_with_results(query, conn):
    with conn.cursor() as cur:
        try:
            cur.execute(query)
            cur.connection.commit()
        except Exception as err:
            st.warning(err)
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
