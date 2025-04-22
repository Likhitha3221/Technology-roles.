import streamlit as st
import pandas as pd
from io import BytesIO

# Load Excel
df = pd.read_excel("entry_level_chicagoland_jobs.xlsx")

# Sidebar filters
st.sidebar.title("🔍 Filter Jobs")
selected_city = st.sidebar.multiselect("City", sorted(df['city'].unique()), default=df['city'].unique())

# Extract skills as a list of unique skills
skills_list = sorted(set(", ".join(df['skills'].dropna()).split(", ")))
selected_skills = st.sidebar.multiselect("Skills", skills_list)

# Filter DataFrame based on user input
filtered_df = df[df['city'].isin(selected_city)]
if selected_skills:
    filtered_df = filtered_df[filtered_df['skills'].apply(lambda x: any(skill in x for skill in selected_skills))]

# Main display
st.title("💼 Entry-Level Tech Jobs - Chicagoland")
st.dataframe(filtered_df)

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered Jobs')
    processed_data = output.getvalue()
    return processed_data

# Download Excel Button
st.download_button(
    label="📥 Download Filtered Jobs (Excel)",
    data=to_excel(filtered_df),
    file_name="filtered_jobs.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


