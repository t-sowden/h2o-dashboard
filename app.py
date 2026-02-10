import streamlit as st
import pandas as pd

st.set_page_config(page_title="Water Quality Inspector")

# Centered title using HTML markdown
st.markdown(
    "<h1 style='text-align: center;'>Water Quality Inspector</h1>", unsafe_allow_html=True
)

df = pd.read_csv("water_data.csv")

# Sidebar to select a location to look at
location_options = df['Location'].unique() if 'Location' in df.columns else []
selected_location = st.sidebar.selectbox(
    "Select Location", 
    options=location_options if len(location_options) > 0 else ["All"],
    index=0
) if len(location_options) > 0 else "All"

# Filter dataframe based on selected location
if selected_location != "All" and 'Location' in df.columns:
    filtered_df = df[df['Location'] == selected_location]
else:
    filtered_df = df

# Calculate metrics for the selected location or all data
avg_ph = filtered_df['pH'].mean()
max_turbidity = filtered_df['Turbidity_NTU'].max()
avg_flow_cfs = filtered_df['Flow_cfs'].mean()
max_flow_cfs = filtered_df['Flow_cfs'].max()

# Create a chart-like metrics box with blue borders
st.markdown(
    """
    <div style="
        border: 3px solid #228be6;
        border-radius: 10px;
        padding: 20px 10px 15px 10px;
        background-color: #f8fbff; 
        margin-bottom: 25px;">
        <div style='display: flex; justify-content: space-between;'>
            <div style='flex:1; text-align: center;'>
                <div style='font-size: 18px; color: #337;'>Average pH</div>
                <div style='font-weight: bold; font-size: 26px;'>{avg_ph:.2f}</div>
            </div>
            <div style='flex:1; text-align: center;'>
                <div style='font-size: 18px; color: #337;'>Max Turbidity (NTU)</div>
                <div style='font-weight: bold; font-size: 26px;'>{max_turbidity:.2f}</div>
            </div>
            <div style='flex:1; text-align: center;'>
                <div style='font-size: 18px; color: #337;'>Average Flow (cfs)</div>
                <div style='font-weight: bold; font-size: 26px;'>{avg_flow_cfs:.2f}</div>
            </div>
            <div style='flex:1; text-align: center;'>
                <div style='font-size: 18px; color: #337;'>Max Flow (cfs)</div>
                <div style='font-weight: bold; font-size: 26px;'>{max_flow_cfs:.2f}</div>
            </div>
        </div>
    </div>
    """.format(
        avg_ph=avg_ph,
        max_turbidity=max_turbidity,
        avg_flow_cfs=avg_flow_cfs,
        max_flow_cfs=max_flow_cfs,
    ),
    unsafe_allow_html=True,
)

st.dataframe(filtered_df)
