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
  for level in staff_on_project:
    percent = st.slider(f'{level} - Estimated Percent of Work:', min_value=0, max_value=100, step=5, key=f"slider_{level}")
    staff_workload[level] = percent
