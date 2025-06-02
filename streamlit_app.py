import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date, timedelta
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
#Sidebar Integration
with st.sidebar:
  st.header("Project Characteristics")
  # Getting Project Office
  project_office = st.selectbox('Project Office', ("Akron", "Beachwood", "Cleveland", "MCS", "Wooster"))
  # Getting Project Location
  project_state = st.selectbox('Project State', ("Alaska",	"Arkansas",	"Arizona",	"California",	"Colorado",	"Connecticut",	"District of Columbia",	"Florida",	"Georgia", "Iowa",	"Idaho",	"Illinois",	"Indiana",	"Kansas",	"Kentucky",	"Massachusetts",	"Maryland",	"Maine",	"Michigan",	"Minnesota",	"Missouri",	"Montana",	"North Carolina",	"New Mexico",	"Nevada",	"New York",	"Ohio",	"Oklahoma",	"Oregon", "Pennsylvania",	"Puerta Rico",	"South Carolina",	"Tennessee",	"Texas",	"Virginia",	"Washington",	"Wisconsin",	"West Virginia", "Other"))
  # Getting Project Client Type
  client_type = st.selectbox('Client Type', ("Corporation", "Fiduciary", "Individual", "Non-Profit", "Partnership"))
  # Getting Staff Composition
  selected_roles = st.multiselect("Select Seniority of Staff Member(s) on the Project", ["Senior Manager", "Administrator", "Staff", "Director", "Manager", "Officer", "Senior", "Associate", "Senior Executive", "Seasonal", "Owner", "Intern", "Intern PT", "Consultant", "Intern FT"])
  # Initialize workload dictionary
  staff_workload = {}
  total = 0
  
  st.write("#### Enter workload percentages (must total 100%)")
  
  # Display number inputs for selected roles
  cols = st.columns(2)
  for idx, role in enumerate(selected_roles):
      with cols[idx % 2]:
          percent = st.number_input(
              f"{role} (%)",
              min_value=0,
              max_value=100,
              step=1,
              key=f"work_{role}"
          )
          staff_workload[role] = percent
  
  # Total
  total = sum(staff_workload.values())
  st.markdown(f"**Total Allocated: {total}%**")
  
  # Validation
  if total < 100:
      st.warning("Total is less than 100%.")
  elif total > 100:
      st.error("Total exceeds 100%. Please adjust the values.")
  else:
      st.success("Total is exactly 100%. Ready to proceed!")
  # Getting Project Start Date
  start_date = st.date_input('Estimated Start and Finish Date')
