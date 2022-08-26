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

st.title("INITIALIZATION") 
 
st.write("**Project to Objective to Key Result Tables**")
st.write("These tables represent a collection of PROJECT OBJECTS. Each PROJECT OBJECT can contain many objectives. Each OBJECTIVE OBJECT is a collection of KEY RESULT OBJECTS.")
st.image("./images/objectives_model.jpg")


run_query_none("DROP TABLE IF EXISTS project;") 
run_query_none("CREATE TABLE project (project_id SERIAL PRIMARY KEY, project_name TEXT, project_createdDate DATE, project_owner TEXT);")

run_query_none("DROP TABLE IF EXISTS objective;") 
run_query_none("CREATE TABLE objective (objective_id SERIAL PRIMARY KEY, objective_name TEXT, objective_createdDate DATE, CONSTRAINT fk_project FOREIGN KEY(project_id) REFERENCES project);")

# run_query_none("DROP TABLE IF EXISTS keyResult;") 
# run_query_none("CREATE TABLE keyResult (keyResult_id SERIAL PRIMARY KEY, keyResult_definition TEXT, keyResult_status TEXT, CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES customers(customer_id));")
# run_query_none("INSERT INTO project (projectName, createdDate, projectOwner) VALUES ('Dogs vs Cats', '2022-07-26', 'Ron');")
# run_query_none("DROP TABLE IF EXISTS objective;") 
# run_query_none("CREATE TABLE objective (objectiveID SERIAL PRIMARY KEY, objectiveName TEXT, createDate DATE, createdBy TEXT);")
# run_query_none("INSERT INTO objective (objectiveName, createdDate) VALUES ('');")


project_metadata = get_table_metadata('project')
project_metadata_cols = [desc[0] for desc in project_metadata]
project_data = run_query_all("SELECT * FROM project")
project_df = pd.DataFrame(project_data, columns = project_metadata_cols)
st.table(project_df)

objective_metadata = get_table_metadata('objective')
objective_metadata_cols = [desc[0] for desc in objective_metadata]
objective_data = run_query_all("SELECT * FROM objective")
objective_df = pd.DataFrame(objective_data, columns = objective_metadata_cols)
st.table(objective_df)

keyResult_metadata = get_table_metadata('keyResult')
keyResult_metadata_cols = [desc[0] for desc in keyResult_metadata]
keyResult_data = run_query_all("SELECT * FROM keyResult")
keyResult_df = pd.DataFrame(keyResult_data, columns = keyResult_metadata_cols)
st.table(keyResult_df)


