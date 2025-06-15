import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="BiUrbs Development Simulator",
    page_icon="🌳",
    layout="wide"
)

# --- Title and Introduction ---
st.title("BiUrbs Interactive Development Simulator 🌳")
st.markdown("""
This prototype demonstrates how different development choices impact biodiversity and cost, based on the BiUrbs project research. 
Select a development option for **Site 1** from the dropdown menu to see the results.
""")

# --- Load Data ---
# Load the structured data we created in Phase 1
try:
    df = pd.read_csv("economic_data.csv")
except FileNotFoundError:
    st.error("Error: 'economic_data.csv' not found. Please make sure the data file is in the same folder as this script.")
    st.stop()


# --- Interactive Widget: Dropdown Menu ---
# Create a list of options for the dropdown menu
option_names = df['Option_Name'].tolist()
selected_option_name = st.selectbox(
    "Select a Development Option:",
    option_names
)

# --- Filter Data Based on Selection ---
# Find the row in the dataframe that corresponds to the user's selection
selected_data = df[df['Option_Name'] == selected_option_name].iloc[0]


# --- Display Results ---
st.header(f"Results for: {selected_option_name}")

# Create columns for a cleaner layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Biodiversity Net Gain (BNG)", value=selected_data['BNG'])

with col2:
    st.metric(label="Habitat Units", value=f"{selected_data['Habitat_Units']:.2f}")

with col3:
    st.metric(label="Cost of Habitats", value=f"£{selected_data['Cost_of_Habitats']:,}")

st.markdown(f"This option has a habitat cost that is **{selected_data['Cost_Percentage']}** of the total development cost.")


# --- Visualization ---
st.header("Cost Breakdown")

# Create a simple dataframe for the chart
cost_data = {
    'Cost Type': ['Habitat Cost', 'Other Development Costs (Estimated)'],
    'Value': [
        selected_data['Cost_of_Habitats'],
        # Estimate total cost to show context
        (selected_data['Cost_of_Habitats'] / (float(selected_data['Cost_Percentage'].strip('%')) / 100)) - selected_data['Cost_of_Habitats']
    ]
}
cost_df = pd.DataFrame(cost_data)

# Create a bar chart with Plotly
fig = px.bar(
    cost_df,
    x='Value',
    y='Cost Type',
    orientation='h',
    text='Value',
    title=f"Cost Structure for '{selected_option_name}'",
    labels={'Value': 'Cost (£)', 'Cost Type': ''}
)
fig.update_traces(texttemplate='£%{text:,.0f}', textposition='outside')
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

st.info("Source: Data derived from the BiUrbs project presentation, slide titled 'Site 1 - Options'.", icon="ℹ️")