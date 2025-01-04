import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    likes_chart = plt.figure(figsize=(12, 6))
    sns.barplot(
        x="Likes", y="PostType", data=filtered_data.sort_values("Likes", ascending=False), palette="viridis"
    )
    plt.title("Likes by Post Type", fontsize=16)
    plt.xlabel("Likes")
    plt.ylabel("Post Type")
    st.pyplot(likes_chart)

    # Line Chart: Engagement Trends
    st.subheader("Engagement Trends")
    engagement_chart = plt.figure(figsize=(12, 6))
    filtered_data.set_index("PostType")[['Likes', 'Comments', 'Shares', 'Clicks']].plot(kind="line", marker="o")
    plt.title("Engagement Trends by Post Type", fontsize=16)
    plt.ylabel("Engagement")
    plt.xlabel("Post Type")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(engagement_chart)

    # Pie Chart: Views Distribution
    st.subheader("Views Distribution")
    views_chart = plt.figure(figsize=(8, 8))
    filtered_data.groupby("PostType")["Views"].sum().plot(kind="pie", autopct='%1.1f%%', startangle=140, colormap='viridis')
    plt.ylabel("")
    plt.title("Views Distribution by Post Type")
    st.pyplot(views_chart)

    # Scatter Plot: Likes vs Comments
    st.subheader("Likes vs Comments")
    scatter_chart = plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x="Likes", y="Comments", data=filtered_data, hue="PostType", palette="tab10", s=100
    )
    plt.title("Likes vs Comments")
    plt.xlabel("Likes")
    plt.ylabel("Comments")
    plt.grid(True)
    st.pyplot(scatter_chart)

else:
    st.title("Welcome to the Post Analytics Dashboard")
    st.write("Please upload a CSV file to get started.")
