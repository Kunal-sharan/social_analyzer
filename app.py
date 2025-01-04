import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Set page configuration
st.set_page_config(page_title="Post Analytics Dashboard", layout="wide")

# Sidebar
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    data = load_data(uploaded_file)
    st.sidebar.header("Filter Options")

    # Filter options
    post_types = st.sidebar.multiselect(
        "Select Post Types:",
        options=data["PostType"].unique(),
        default=data["PostType"].unique()
    )

    # Apply filters
    filtered_data = data[data["PostType"].isin(post_types)]

    # Main content
    st.title("Social Media Post Analytics")

    # Display filtered data
    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    # Key Metrics
    st.header("Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Likes", value=filtered_data["Likes"].sum())
    with col2:
        st.metric(label="Total Comments", value=filtered_data["Comments"].sum())
    with col3:
        st.metric(label="Total Shares", value=filtered_data["Shares"].sum())
    with col4:
        st.metric(label="Total Views", value=filtered_data["Views"].sum())
    with col5:
        st.metric(label="Total Clicks", value=filtered_data["Clicks"].sum())

    # Visualization section
    st.header("Visual Analytics")

    # Bar Chart: Likes by Post Type
    st.subheader("Likes by Post Type")
    bar_chart = px.bar(
        filtered_data,
        x="PostType",
        y="Likes",
        color="PostType",
        title="Likes by Post Type",
        labels={"Likes": "Number of Likes", "PostType": "Post Type"},
        template="plotly_white"
    )
    st.plotly_chart(bar_chart, use_container_width=True)

    # Line Chart: Engagement Trends
    st.subheader("Engagement Trends")
    line_chart = px.line(
        filtered_data.melt(id_vars=["PostType"], value_vars=["Likes", "Comments", "Shares", "Clicks"], var_name="Metric", value_name="Value"),
        x="PostType",
        y="Value",
        color="Metric",
        title="Engagement Trends by Post Type",
        labels={"Value": "Engagement Value", "PostType": "Post Type"},
        template="plotly_white"
    )
    st.plotly_chart(line_chart, use_container_width=True)

    # Pie Chart: Views Distribution
    st.subheader("Views Distribution")
    pie_chart = px.pie(
        filtered_data,
        names="PostType",
        values="Views",
        title="Views Distribution by Post Type",
        template="plotly_white"
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    # Scatter Plot: Likes vs Comments
    st.subheader("Likes vs Comments")
    scatter_chart = px.scatter(
        filtered_data,
        x="Likes",
        y="Comments",
        color="PostType",
        size="Shares",
        hover_data=["Views", "Clicks"],
        title="Likes vs Comments",
        labels={"Likes": "Number of Likes", "Comments": "Number of Comments"},
        template="plotly_white"
    )
    st.plotly_chart(scatter_chart, use_container_width=True)

else:
    st.title("Welcome to the Post Analytics Dashboard")
    st.write("Please upload a CSV file to get started.")
