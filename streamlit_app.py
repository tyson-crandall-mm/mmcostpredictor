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
