import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import gspread

st.title('M&M Machine Learning Cost Proposal Tool')
st.info('This is an Aid, Final Proposals are Subject to Partner Reviews')

# Google Sheet ID and GID
sheet_id = "1BXiGbxDcj7unwDmS4G3yg72_jORQYJejDYc7S4jEcl4"
gid = "1289547923"

# Construct export URL
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Load into DataFrame
df = pd.read_csv(url)
df

with st.sidebar:
  st.header("Project Characteristics")
  project_office = st.selectbox('Project Office', ("Akron", "Beachwood", "Cleveland", "MCS", "Wooster"))
  project_state = st.selectbox('Project State', ("Alaska",	"Arkansas",	"Arizona",	"California",	"Colorado",	"Connecticut",	"District of Columbia",	"Florida",	"Georgia", "Iowa",	"Idaho",	"Illinois",	"Indiana",	"Kansas",	"Kentucky",	"Massachusetts",	"Maryland",	"Maine",	"Michigan",	"Minnesota",	"Missouri",	"Montana",	"North Carolina",	"New Mexico",	"Nevada",	"New York",	"Ohio",	"Oklahoma",	"Oregon", "Pennsylvania",	"Puerta Rico",	"South Carolina",	"Tennessee",	"Texas",	"Virginia",	"Washington",	"Wisconsin",	"West Virginia", "Other"))
  client_type = st.selectbox('Client Type', ("Corporation", "Fiduciary", "Individual", "Non-Profit", "Partnership"))
  staff_workload = {}
  staff_on_project = st.multiselect("Select Seniority of Staff Member(s) on the Project", ["Senior Manager", "Administrator", "Staff", "Director", "Manager", "Officer", "Senior", "Associate", "Senior Executive", "Seasonal", "Owner", "Intern", "Intern PT", "Consultant", "Intern FT"])
  # Initialize session state
  if 'staff_workload' not in st.session_state:
    st.session_state.staff_workload = {role: 0 for role in selected_roles}
  # Total so far
  current_total = sum(st.session_state.staff_workload.get(role, 0) for role in selected_roles)
  remaining = max(0, 100 - current_total)
  st.write(f"Total allocated: {current_total}%. Remaining: {remaining}%")
  # Input sliders with dynamic max based on remaining percent
  for role in selected_roles:
    # Set dynamic max value
    current_value = st.session_state.staff_workload.get(role, 0)
    max_allowed = min(100, remaining + current_value)
    new_val = st.slider(
        f"{role} - Estimated % of Work",
        min_value=0,
        max_value=max_allowed,
        step=5,
        value=current_value,
        key=f"slider_{role}"
    )
    st.session_state.staff_workload[role] = new_val
    # Optional: Warning if total ≠ 100%
  if current_total != 100:
    st.warning("Total must equal 100% before submitting.")
  else:
    st.success("Total is 100%. Ready to submit.")
