########################## IMPORTS ##########################
import streamlit as st
import pandas as pd
from datetime import datetime
import math
import sys
import psycopg2
# allows us to import utils by adding parent directory to path
sys.path.append('..')
import utils as ut

##########################SET UP ##########################

# Call and set up database
# Initialize connection to postgres tabletry:
try:
    conn = ut.init_connection("dataStudioPostgres")
except:
    st.error("Cannot Connect to Database. Check Connection and Try Again")
    st.stop()

project = ut.exectute_query_with_results("SELECT * FROM project", conn)
objective = ut.exectute_query_with_results("SELECT * FROM objective", conn)
key_result = ut.exectute_query_with_results("SELECT * FROM keyResult", conn)

# set up tables in db if not already existing
ut.execute_query("data/objective_DDL.sql", conn, f = True)



############# DISPLAY PAGE #############
st.title("DATA PRODUCT MANAGEMENT")
st.write("Use this page to set data product Objectives and Key Results. \
Start by selecting or creating a new project. Then, define your project Objectives,\
or the goals of your project. Finish by adding Key Results for each objective,\
which should encompass the ideal outcome for all users of your product.")

############# PROJECT SECTION #############
# if there are no project we must first add a project
if not project:
    st.write('You currently have no projects. Click "Add a Project" to Begin.')
else:
    # display all projects
    project_names = [x[1] for x in project]
    current_project = st.selectbox("Select a Project", project_names)

# if st.button('Add a Project'):
with st.form("project_form"):
    project_name = st.text_input("Enter New Project Name")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit Project")
    if submitted:
        # q = "INSERT INTO project (project_name) \
        # VALUES ('{project_name}');".format(project_name = project_name)
        # execute_query(q, conn)
        # # st.experimental_rerun()
        # st.write("Project Sucessfully Added!")
        st.write("Submitted :) ")




# if not objective:
#     st.write('You currently have no objectives for this project. Click "New Project Objective".')
# else:
#     objective_names = [x[1] for x in objective]
#     current_project = st.selectbox("Select a objective", objective_names)
#
# if st.button('Add an Objective'):
#     with st.form("objective_form"):
#         project_name = st.text_input("Enter New Objective Name")
#
#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit Objective")
#         if submitted:
#             q = "INSERT INTO objective (objective_name) \
#             VALUES ('{project_name}');".format(objective_name = objective_name)
#             execute_query(q, conn)
#             st.experimental_rerun()
