import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Define a function to handle chatbot responses
def chatbot_response(user_input):
    # Simple predefined responses (you can extend this logic or integrate an AI model)
    responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What can I do for you?",
        "how are you": "I'm just a bot, but I'm functioning as expected. How about you?",
        "bye": "Goodbye! Have a great day!",
    }

    # Check for response or default to a fallback
    return responses.get(user_input.lower(), "I'm not sure how to respond to that. Can you rephrase?")

# Streamlit app configuration
st.set_page_config(page_title="Chatbot & Analytics Dashboard", page_icon="🤖", layout="wide")

# App title
st.title("🤖 Chatbot & Post Analytics Dashboard")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chatbot Section
st.header("🔐 Chatbot")

# Display chat history in a scrollable container with fixed height and border
with st.container():
    st.markdown(
        """
        <div style="border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto;">
        """,
        unsafe_allow_html=True,
    )
    chat_display = "<br>".join(
        [f"<strong>{sender}</strong> ({timestamp}): {text}" for sender, text, timestamp in st.session_state.chat_history]
    )
    st.markdown(chat_display, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# User input for chatbot
user_input = st.text_input("You:", "", key="user_input")

# If the user submits input
if st.button("Send") and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append(("You", user_input, datetime.now().strftime("%H:%M:%S")))

    # Generate chatbot response
    response = chatbot_response(user_input)

    # Add chatbot response to chat history
    st.session_state.chat_history.append(("Chatbot", response, datetime.now().strftime("%H:%M:%S")))

    # Auto-scroll to the bottom by refreshing the container
    st.experimental_rerun()

# Analytics Section
def load_data(file_path):
    return pd.read_csv(file_path)

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
    st.header("🔍 Social Media Post Analytics")

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
    bar_chart.update_layout(
        title_font=dict(size=18, weight="bold"),
        xaxis_title_font=dict(size=14, weight="bold"),
        yaxis_title_font=dict(size=14, weight="bold"),
        font=dict(size=12)
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
    line_chart.update_layout(
        title_font=dict(size=18, weight="bold"),
        xaxis_title_font=dict(size=14, weight="bold"),
        yaxis_title_font=dict(size=14, weight="bold"),
        font=dict(size=12)
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
    pie_chart.update_layout(
        title_font=dict(size=18, weight="bold"),
        font=dict(size=12)
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
    scatter_chart.update_layout(
        title_font=dict(size=18, weight="bold"),
        xaxis_title_font=dict(size=14, weight="bold"),
        yaxis_title_font=dict(size=14, weight="bold"),
        font=dict(size=12)
    )
    st.plotly_chart(scatter_chart, use_container_width=True)

else:
    st.header("Welcome to the Post Analytics Dashboard")
    st.write("Please upload a CSV file to get started.")
