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

# initalize session states
if 'Global Project' not in st.session_state:
    st.session_state['Global Project'] = False

if 'Global Objective' not in st.session_state:
    st.session_state['Global Objective'] = False

# Session state allows us to control the state of buttons and warning when page re reruns
# must initialize them all
if 'Add an Objective' not in st.session_state:
    st.session_state['Add an Objective'] = False
if 'Edit Objective' not in st.session_state:
    st.session_state['Edit Objective'] = False
if 'Delete Objective' not in st.session_state:
    st.session_state['Delete Objective'] = False


# flags to display after a add/edit/delete action is completed
if 'Objective Submitted' not in st.session_state:
    st.session_state['Objective Submitted'] = False
if "Objective Edit Confirm" not in st.session_state:
    st.session_state['Objective Edit Confirm'] = False
if "Objective Delete Cancelled" not in st.session_state:
    st.session_state['Objective Delete Cancelled'] = False
if "Objective Delete Confirm" not in st.session_state:
    st.session_state['Objective Delete Confirm'] = False

# functions to set the state on button Click
# this alllows use to switch between buttons without saving the state of the other buttons
# Ex., If we opened "Add a Project" it will not close untill "st.session_state['Add a Project']" is set to False
# So, on click of the other buttons we need to update the state
def set_objective_add_button():
    st.session_state['Add an Objective'] = not st.session_state['Add an Objective']
    st.session_state['Edit Objective'] = False
    st.session_state['Delete Objective'] = False

def set_objective_edit_button():
    st.session_state['Add an Objective'] = False
    st.session_state['Edit Objective'] = not st.session_state['Edit Objective']
    st.session_state['Delete Objective'] = False

def set_objective_delete_button():
    st.session_state['Add an Objective'] = False
    st.session_state['Edit Objective'] = False
    st.session_state['Delete Objective'] = not st.session_state['Delete Objective']

def reset_objective_state():
    st.session_state['Add an Objective'] = False
    st.session_state['Edit Objective'] = False
    st.session_state['Delete Objective'] = False




########################## PAGE HEADER ##########################

st.write("## DATA PRODUCT MANAGEMENT")
# TO DO FIX
st.markdown(""" - Define how an objective creates business value
- Align teams on the purpose and meaning of those objectives.
- Key results are how your team defines success so that you know it is done.
""")

st.write("Tip: Ask for team members' perspectives on the performance reviews of systems and their efficiencies, ask about their pain points using data.")

# st.write(st.session_state)
# message to displacy if we have a Global Project SELECTED
status_slot = st.empty()

default_ix = True
########################## OBJECTIVE BODY ##########################

# get the project selected in "getting started"
current_project = st.session_state['Global Project']

#reset_objective_state() -- problem line
# if there is currently a project, then we can procced

if current_project:
    # query the objectives for the choosen project
    # find the id for the current project
    q = "select project_id from project where project_name = '{}'".format(current_project)
    current_project_id = ut.exectute_query_with_results(q, conn)[0][0]
    q = """SELECT * FROM objective o JOIN project p
            ON o.project_id = p.project_id
            WHERE o.project_id = {pid}""".format(pid = current_project_id)

    objectives = ut.exectute_query_with_results(q, conn)
    objective_names = [x[1] for x in objectives]

    if st.session_state['Objective Delete Cancelled']:
        st.warning("Objective Delete Cancelled")
        st.session_state['Objective Delete Cancelled'] = False

    if st.session_state['Objective Delete Confirm']:
        st.success("Objective Delete Successful")
        st.session_state['Objective Delete Confirm'] = False

    if not objectives:
        st.write('You currently have no objectives for this project. Click "Add Objective" to Begin.')
        st.session_state["Global Objective"] = False
        ut.update_message_slot(status_slot)
    else:
        # display any flags
        if st.session_state['Objective Submitted']:
            default_ix = False
            st.success("Objective Sucessfully Submitted!")
            st.session_state['Objective Submitted'] = False
        if st.session_state['Objective Edit Confirm']:
            default_ix = False
            st.success("Objective Edit Successful")
            st.session_state['Objective Edit Confirm'] = False

        # display all projects
        objectives_names = [x[1] for x in objectives]
        objectives_ids = [x[0] for x in objectives]
        # If a project was just added or edited, make that the default selection
        if default_ix:
            default_ix = 0
        else:
            default_ix = len(objectives_names) -1
        current_objective = st.selectbox("Objective", objectives_names, index = default_ix)
        st.session_state['Global Objective'] = current_objective
        ut.update_message_slot(status_slot)
    # create column of buttons for project options
    col1, col2, col3  = st.columns(3)

    # hiding view for now, might want later
    # with col1:
    #     view = st.button("View Projects", on_click = set_project_view_button)
    with col1:
        add = st.button('Add an Objective', on_click = set_objective_add_button)
    if objectives:
        with col2:
            edit = st.button("Edit Objective", on_click = set_objective_edit_button)
        with col3:
            delete = st.button("Delete Objective", on_click = set_objective_delete_button)

    # Add button is clicked
    if st.session_state['Add an Objective']:
        with st.form("objective_form"):
            # initialize entry sanitization
            valid_entry = True
            reason = ""
            # ask user to enter new name
            new_objective_name = st.text_input("Enter New Objective")
            if objectives and (new_objective_name.lower() in [x.lower() for x in objective_names]):
                valid = True
                reason = "Objective already exists for this project"
            elif len(new_objective_name) < 2:
                valid = True
                reason = "Objective must be at least 2 characters."
            else:
                valid = True
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                if not valid:
                    st.error(reason)
                else:
                    q = "INSERT INTO objective (objective_name, project_id) \
                    VALUES ('{objective_name}', {project_id});".format(objective_name = new_objective_name, project_id = current_project_id)
                    # st.write(q)
                    ut.execute_query(q, conn)
                    # update session states
                    reset_objective_state()
                    st.session_state['Objective Submitted'] = True
                    st.experimental_rerun()

    # Edit button is Clicked
    elif (st.session_state['Edit Objective']) and objectives:
        # st.warning('You are editing "{objective_name}"'.format(objective_name = current_objective))
        with st.form("ObjectiveEditForm"):
            # initalize input sanitization
            valid_entry = True
            reason = ""
            edit_name = st.text_input("What would you like to rename your objective?",value = current_objective)
            # Validate edited name
            if edit_name.lower() in [x.lower() for x in objective_names]:
                valid = False
                reason = "Objective name already exists"
            elif len(edit_name) < 1:
                valid = False
                reason = "Objective name must be at least 2 characters."
            else:
                valid = True
            # Every form must have a submit button.
            submitted = st.form_submit_button("Edit Project")
            if submitted:
                if not valid:
                    st.error(reason)
                else:
                    q = "UPDATE objective set objective_name = '{new_name}' where objective_name = '{current_objective}';".format(new_name = edit_name, current_objective = current_objective)
                    ut.execute_query(q, conn)
                    reset_objective_state()
                    st.session_state['Objective Edit Confirm'] = True
                    st.experimental_rerun()
    elif (st.session_state["Delete Objective"]) and objectives:
            # use error message to confirm delte
            st.error('Do you wish to delete "{current_objective}" ?'.format(current_objective = current_objective))
            # c
            space, no, yes, space  = st.columns(4)
            with no:
                no_button = st.button("NO")
            with yes:
                yes_button = st.button("YES (DELETE PROJECT)" )

            # if the users says no, set a
            if no_button:
                reset_objective_state()
                st.session_state["Objective Delete Cancelled"] = True
                st.experimental_rerun()
            elif yes_button:
                # TODO: FIX TO HANDLE IF MULTIPLE PROJECTS NAMES ARE THE SAME
                q = "DELETE FROM objective WHERE objective_name = '{current_objective}';".format(current_objective = current_objective)
                # st.write(q)
                ut.execute_query(q, conn)
                reset_objective_state()
                st.session_state["Objective Delete Confirm"] = True
                st.experimental_rerun()

st.markdown("""---""")
# reset_objective_state() ##I put this here randomly because otherwise if you hit add objective and then try to reset, it keeps evaluating to true
########################## KEY RESULT BODY ##########################

## To DoL
if current_project and st.session_state['Global Objective']:
    # st.session_state['Global Objective']
    q = "select objective_id from objective where objective_name = '{}'".format(st.session_state['Global Objective'])
    current_objective_id = ut.exectute_query_with_results(q, conn)[0][0]
    q = """SELECT * FROM keyResult k JOIN objective o
            ON k.objective_id = o.objective_id
            WHERE k.objective_id = {oid}""".format(oid = current_objective_id)

    objectives = ut.exectute_query_with_results(q, conn)

    st.write(objectives)
