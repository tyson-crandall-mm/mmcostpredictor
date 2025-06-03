import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date, timedelta
import gspread
import joblib
project_region = None

st.title('M&M Machine Learning Cost Proposal Tool')
st.info('This is an Aid, Final Proposals are Subject to Partner Reviews')

# Google Sheet ID and GID
sheet_id = "1-RpnD_G0mvaqWINletxUERqeQKOJ6K1ZiYyUqKIA6oU"
gid = "263876729"
# Construct export URL
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Load into DataFrame
df = pd.read_csv(url)
df

user_df = df
user_df = user_df.iloc[:0]
#Sidebar Integration
with st.sidebar:
  st.write("# Project Characteristics")
  # Getting Project Office
  project_office = st.selectbox('Project Office', ("Akron", "Beachwood", "Cleveland", "MCS", "Wooster"), index=None, placeholder="Location...")
  # Getting Project Location
  south = {"FL", "TX", "GA", "SC", "NC", "TN", "VA", "AR", "KY", "AL", "MD", "DC", "PR"}
  northeast = {"NY", "MA", "CT", "NJ", "PA", "ME"}
  midwest = {"IL", "IN", "OH", "MI", "WI", "MO", "IA"}
  west = {"AK", "CA", "CO", "WA", "OR", "NV", "AZ", "ID", "MT", "NM", "UT"}
  project_state = st.selectbox('Project State', ("AK",	"AR",	"AZ",	"CA",	"CO",	"CT",	"DC",	"FL",	"GA", "IA",	"ID",	"IL",	"IN",	"KS",	"KY",	"MA",	"MD",	"ME",	"MI",	"MN",	"MO",	"MT",	"NC",	"NM",	"NV",	"NY",	"OH",	"OK",	"OR", "PA",	"PR",	"SC",	"TN",	"TX",	"VA",	"WA",	"WI",	"WV"), index=None, placeholder="State...")
  def get_region(state):
    if state in south:
        return "South"
    elif state in northeast:
        return "Northeast"
    elif state in midwest:
        return "Midwest"
    elif state in west:
        return "West"
    else:
        return "Unknown"
  # Getting Client Region
  if project_state:
    project_region = get_region(project_state)
  # Getting Project Client Type
  client_type = st.selectbox('Client Type', ("Corporation", "Fiduciary", "Individual", "Non-Profit", "Partnership"), index=None, placeholder="Client Type...")
  # Getting Project Master Name
  services = st.multiselect('Proposed Services', ["1040 - Large Tax", "1099 Forms", "4868 Extension", "7004 Extension", "7004F Extension for Fiduciary Return", "8868 Extension", "Amended Return Corporate", "Amended Return Individual/Estate", "Annual Return/Report of Employee Benefit Plan", "Corporate Federal Tax Return", "Corporate Income Tax Return", "Corporate State Tax Return", "ERP Utilization or Improvement", "ERP or Other Upgrade", "Estates & Trusts Income Tax Return", "Individual Income Tax Return", "MCS-ECi-DEV", "MCS-Onsites", "MCS-SUPPORT PROJECT", "Ongoing Client Support", "Partnership Income Tax Return", "Payroll - Annual", "Payroll - Quarterly", "Payroll-Monthly", "Payroll- Quarterly", "Quartely Estimates", "Quarterly Estimates - Corporate", "Quarterly Estimates - Individual", "Return of Organization Exempt from Income Tax", "S Corporation Tax Return", "TAX PLANNING", "Tax One Time Only - Corporate", "Tax One Time Only - Individual", "U.S. Gift Tax Return"])
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
      st.warning("""**Total is less than 100%.**""")
  elif total > 100:
      st.error("""**Total exceeds 100%. Please adjust the values.**""")
  else:
      st.success("""**Total is exactly 100%. Ready to proceed!**""")
  # Getting Project Complexity
  complexity_levels = {1: "Basic", 2: "Easy", 3: "Moderate", 4: "Complex"}
  project_complexity = st.segmented_control("Project Complexity Level", options=complexity_levels.keys(), format_func=lambda option: complexity_levels[option], selection_mode="single")
  # Getting Project Hours
  hour_levels = {1: "Extremely Little", 2: "Quite Little", 3: "Little", 4: "Moderate", 5: "High", 6: "Quite High", 7:"Extremely High"}
  project_hours = st.pills("Project Hours", options=hour_levels.keys(), format_func=lambda option: hour_levels[option], selection_mode="single")
  st.warning("""\
  **Project Hours Guide**  
  - Extremely Little: 0 to 1 hours  
  - Quite Little: 1 to 2 hours  
  - Little: 2 to 5 hours  
  - Moderate: 5 to 11 hours  
  - High: 11 to 39 hours  
  - Quite High: 39 to 80 hours  
  - Extremely High: 80+ hours\
  """)
  # Getting Project Dates
  default_start = date.today()
  default_finish = default_start + timedelta(days=1)
  # Ask user for date range input
  estimated_dates = st.date_input("Project Estimated Start and Finish Date", value=(default_start, default_finish))
  # Check if a valid date range was returned
  if isinstance(estimated_dates, tuple) and len(estimated_dates) == 2:
    estimated_start_date, estimated_end_date = estimated_dates
  # Validation
  if estimated_start_date > estimated_end_date:
    st.error("Start date must be before or equal to end date.")
  else:
    st.error("Please select both a start and end date.")
  # Get User Input in DataFrame

# Only populate if required fields are filled
user_data = {}
if all([project_office, project_state, project_region, client_type, services, staff_workload, project_complexity, project_hours, isinstance(estimated_dates, tuple) and len(estimated_dates) == 2]):
  user_data = {
      "ProjectOffice": project_office,
      "ProjectState": project_state,
      "ProjectRegion": project_region,
      "ClientType": client_type,
      "Services": services,
      "StaffWorkDistribution": staff_workload,
      "ProjectComplexity": project_complexity,
      "ProjectHours": project_hours,
      "EstimatedDates": estimated_dates
  }
  st.success("All inputs collected successfully!")
  user_df.drop(columns = "ActualBudgetAmount")

  # Start with all zeros
  new_row = {col: 0 for col in user_df.columns}
  
  # Set encoded flags
  if project_office in user_df.columns:
      new_row[project_office] = 1
  
  if project_state in user_df.columns:
      new_row[project_state] = 1
  
  if project_region in user_df.columns:
      new_row[project_region] = 1
  
  if client_type in user_df.columns:
      new_row[client_type] = 1

  new_row['ProjectEstimatedHours'] = project_hours
  new_row['ProjectComplexityEncoded'] = project_complexity

  for position, time in staff_workload.items():
      if position in user_df.columns:
          new_row[position] = (time/100)

  for service in services:
      if service in user_df.columns:
          new_row[service] = 1

  new_row["StartYear"] = estimated_start_date.year
  new_row["StartMonth"] = estimated_start_date.month
  new_row["StartDay"] = estimated_start_date.day
  new_row["StartDayOfWeek"] = estimated_start_date.weekday()
  new_row["FinishYear"] = estimated_end_date.year
  new_row["FinishMonth"] = estimated_end_date.month
  new_row["FinishDay"] = estimated_end_date.day
  new_row["FinishDayOfWeek"] = estimated_end_date.weekday()
  project_duration_days = (estimated_end_date - estimated_start_date).days
  new_row["ProjectDurationDays"] = project_duration_days
  
  user_df = pd.concat([user_df, pd.DataFrame([new_row])], ignore_index=True)
else:
  st.warning("Please complete all required fields to generate a project summary.")
user_df
model = joblib.load('xgb_model.pkl')
prediction = model.predict(user_df)
st.subheader("Predicted Budget Amount")
st.write(f"${prediction[0]:,.2f}")
