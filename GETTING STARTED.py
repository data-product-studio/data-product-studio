########################## IMPORTS ##########################
import streamlit as st
import utils as ut

########################## PAGE SET UP ##########################
# try:
conn = ut.init_connection("dataStudioPostgres")
# except:
#     st.error("Cannot Connect to Database. Check Connection and Try Again")
#     st.stop()

# set up tables in db if not already existing
ut.execute_query("data/objective_DDL.sql", conn, f = True)

# query each of the tables and store results
project = ut.exectute_query_with_results("SELECT * FROM project", conn)

# Session state allows us to control the state of buttons and warning when page re reruns
# must initialize them all

if 'rerun' not in st.session_state:
    st.session_state['rerun'] = 0
else:
    st.session_state['rerun'] +=1
st.write(st.session_state['rerun'])

if 'Add a Project' not in st.session_state:
    st.session_state['Add a Project'] = False
if 'View Projects' not in st.session_state:
    st.session_state['View Projects'] = False
if 'Edit Project' not in st.session_state:
    st.session_state['Edit Project'] = False
if 'Delete Project' not in st.session_state:
    st.session_state['Delete Project'] = False



# initalize session state of flags/pop-ups
if 'Project Submitted' not in st.session_state:
    st.session_state['Project Submitted'] = False
if "Project Delete Cancelled" not in st.session_state:
    st.session_state['Project Delete Cancelled'] = False
if "Project Delete Confirm" not in st.session_state:
    st.session_state['Project Delete Confirm'] = False
if "Project Edit Confirm" not in st.session_state:
    st.session_state['Project Edit Confirm'] = False

# initalize session state of flags/pop-ups
if 'Global Project' not in st.session_state:
    st.session_state['Global Project'] = False

# functions to set the state on button Click
# this alllows use to switch between buttons without saving the state of the other buttons
# Ex., If we opened "Add a Project" it will not close untill "st.session_state['Add a Project']" is set to False
# So, on click of the other buttons we need to update the state
def set_project_view_button():
    st.session_state['View Projects'] = not st.session_state['View Projects']
    st.session_state['Add a Project'] = False
    st.session_state['Edit Project'] = False
    st.session_state['Delete Project'] = False

def set_project_add_button():
    st.session_state['View Projects'] = False
    st.session_state['Add a Project'] = not st.session_state['Add a Project']
    st.session_state['Edit Project'] = False
    st.session_state['Delete Project'] = False

def set_project_edit_button():
    st.session_state['View Projects'] = False
    st.session_state['Add a Project'] = False
    st.session_state['Edit Project'] = not st.session_state['Edit Project']
    st.session_state['Delete Project'] = False

def set_project_delete_button():
    st.session_state['View Projects'] = False
    st.session_state['Add a Project'] = False
    st.session_state['Edit Project'] = False
    st.session_state['Delete Project'] = not st.session_state['Delete Project']

def reset_project_state():
    st.session_state['View Projects'] = False
    st.session_state['Add a Project'] = False
    st.session_state['Edit Project'] = False
    st.session_state['Delete Project'] = False


def update_select_box():
    st.session_state['View Projects'] = False
    st.session_state['Add a Project'] = False
    st.session_state['Edit Project'] = False
    st.session_state['Delete Project'] = False


########################## PAGE HEADER ##########################


"## Getting Started with the Data Product Studio"
"An open-source workflow for teams to get on the same page. We hope your teams use the Data Product Studio to collaborate, communicate, and create data products faster and easier than ever before."


st.write("### To begin, please select or create a project.")

########################## PROJECT BODY ##########################
# check if any flags need to be set
# Raise pop ups for flags
if st.session_state['Project Submitted']:
    st.success("Project Sucessfully Submitted!")
    st.session_state['Project Submitted'] = False

if st.session_state['Project Delete Cancelled']:
    st.warning("Project Delete Cancelled")
    st.session_state['Project Delete Cancelled'] = False

if st.session_state['Project Delete Confirm']:
    st.success("Project Delete Successful")
    st.session_state['Project Delete Confirm'] = False

if st.session_state['Project Edit Confirm']:
    st.success("Project Edit Successful")
    st.session_state['Project Edit Confirm'] = False


# if there are no projects we must first add a project
if not project:
    st.write('You currently have no projects. Click "Add a Project" to Begin.')
    st.session_state['Global Project'] = False
else:
    # display all projects
    project_names = [x[1] for x in project]
    project_ids = [x[0] for x in project]

    # if a project is added, we want that to become the new default select box option
    # this needs to be here, because we can not acces project len earlier
    # we only need to consider this if we have not already selected a gloab project

    # if a project was just added (which sets default_ix to False), we want that to be the default
    # if not default_ix:
    #     select_ix = len(project_names) -1
    # # # elif we have an existing global project, we want that to be the deault value
    # if st.session_state['Global Project']:
    #     select_ix = project_names.index(st.session_state['Global Project'])
    # # otherwise the first value can be the deafult
    # else:
    #     select_ix = False

### # TODO:  FIX SELECT BOX DEFAULT LOGIC
    #  select a project dropdown
    # when an option is selected, it becomes the global project
    # st.write(st.session_state["Global Project"], select_ix)
    st.session_state
     # index = select_ix,
    current_project = st.selectbox(label = "", options = project_names,  label_visibility = "collapsed")
    st.write(current_project)
    st.session_state
    st.session_state['Global Project'] = current_project

    # select_ix = current_project.index(st.session_state['Global Project'])
    st.write("Made it here")
    # st.write(st.session_state["Global Project"], select_ix)


# create column of buttons for project options
col2, col3, col4  = st.columns(3)

# hiding view for now, might want later
# with col1:
#     view = st.button("View Projects", on_click = set_project_view_button)
with col2:
    add = st.button('Add a Project', on_click = set_project_add_button)
if project:
    with col3:
        edit = st.button("Edit Project", on_click = set_project_edit_button)
    with col4:
        delete = st.button("Delete Project", on_click = set_project_delete_button)

if st.session_state['Add a Project']:
    with st.form("project_form"):
        # initialize entry sanitization
        valid_entry = True
        reason = ""
        # ask user to enter new name
        new_project_name = st.text_input("Enter New Project Name")
        if project and (new_project_name.lower() in [x.lower() for x in project_names]):
            valid = False
            reason = "Project name already exists"
        elif len(new_project_name) < 4:
            valid = False
            reason = "Project name must be at least 5 characters."
        else:
            valid = True
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not valid:
                st.error(reason)
            else:
                q = "INSERT INTO project (project_name) \
                VALUES ('{project_name}');".format(project_name = new_project_name)
                ut.execute_query(q, conn)
                # update session states
                reset_project_state()
                st.session_state['Project Submitted'] = True
                st.experimental_rerun()

elif (st.session_state['Edit Project']) and project:
    st.warning('You are editing "{project_name}"'.format(project_name = current_project))
    with st.form("projectEditForm"):
        # initalize input sanitization
        valid_entry = True
        reason = ""
        edit_name = st.text_input("What would you like to rename your project?",value = current_project)
        # Validate edited name
        if edit_name.lower() in [x.lower() for x in project_names]:
            valid = False
            reason = "Project name already exists"
        elif len(edit_name) < 1:
            valid = False
            reason = "Project name must be at least 2 characters."
        else:
            valid = True
        # Every form must have a submit button.
        submitted = st.form_submit_button("Edit Project")
        if submitted:
            if not valid:
                st.error(reason)
            else:
                q = "UPDATE project set project_name = '{new_name}' where project_name = '{current_project}';".format(new_name = edit_name, current_project = current_project)
                ut.execute_query(q, conn)
                reset_project_state()
                st.session_state['Project Edit Confirm'] = True
                st.experimental_rerun()

elif (st.session_state['Delete Project']) and project:
    # use error message to
    st.error('Do you wish to delete "{current_project}" ?'.format(current_project = current_project))
    # c
    space, no, yes, space  = st.columns(4)
    with no:
        no_button = st.button("NO")
    with yes:
        yes_button = st.button("YES (DELETE PROJECT)" )

    # if the users says no, set a
    if no_button:
        reset_project_state()
        st.session_state["Project Delete Cancelled"] = True
        st.experimental_rerun()
    elif yes_button:
        # TODO: FIX TO HANDLE IF MULTIPLE PROJECTS NAMES ARE THE SAME
        q = "DELETE FROM project WHERE project_name = '{current_project}';".format(current_project = current_project)
        # st.write(q)
        ut.execute_query(q, conn)
        reset_project_state()
        st.session_state["Project Delete Confirm"] = True
        st.experimental_rerun()
