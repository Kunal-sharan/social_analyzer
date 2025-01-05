# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# import requests
# from langflow.load import run_flow_from_json
# TWEAKS = {
#   "ChatInput-JCzea": {},
#   "ParseData-Vqvlh": {},
#   "Prompt-YQ0MX": {},
#   "ChatOutput-UUU35": {},
#   "AstraDB-436Kc": {},
#   "AstraDB-3Huko": {},
#   "File-BMkha": {},
#   "GroqModel-zgAaN": {},
#   "Memory-Ml6IC": {},
#   "RecursiveCharacterTextSplitter-hJufx": {}
# }

# # Define a function to handle chatbot responses
# def chatbot_response(user_input):
#     # Simple predefined responses (you can extend this logic or integrate an AI model)
#     result = run_flow_from_json(flow="Vector Store RAG.json",
#                             input_value=user_input, # provide a session id if you want to use session state
#                             fallback_to_env_vars=True, # False by default
#                             tweaks=TWEAKS)

#     # Check for response or default to a fallback
#     return result

# # Function to make a POST API call

# # Streamlit app configuration
# st.set_page_config(page_title="Chatbot & Analytics Dashboard", page_icon="🤖", layout="wide")

# # App title
# st.title("🤖 Chatbot & Post Analytics Dashboard")

# # Initialize session state for chat history if it doesn't exist
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Chatbot Section
# st.header("🔐 Chatbot")

# # Display chat history in a scrollable container with fixed height and border
# with st.container(border=True,height=500):
#     st.write("### Chat History")
#     chat_placeholder = st.empty()
#     with chat_placeholder.container():
#         for sender, text, timestamp in st.session_state.chat_history:
#             st.write(f"**{sender}** ({timestamp}): {text}")

# # User input for chatbot
# user_input = st.text_input("You:", "", key="user_input")

# # If the user submits input
# if st.button("Send") and user_input.strip():
#     # Add user message to chat history
#     st.session_state.chat_history.append(("You", user_input, datetime.now().strftime("%H:%M:%S")))

#     # Generate chatbot response using POST API call
   

#     bot_response = chatbot_response(user_input)

#     # Add chatbot response to chat history
#     st.session_state.chat_history.append(("Chatbot", bot_response, datetime.now().strftime("%H:%M:%S")))

#     # Auto-scroll to the bottom by refreshing the container
#     st.rerun()

# # Example POST API call usage
# st.sidebar.header("Test API Call")
# api_url = st.sidebar.text_input("API URL", "https://example.com/api")
# payload = st.sidebar.text_area("Payload (JSON)", "{\"key\": \"value\"}")
# if st.sidebar.button("Call API"):
#     try:
#         payload_dict = eval(payload)  # Convert string to dictionary
#         api_response = post_api_call(api_url, payload_dict)
#         st.sidebar.write("Response:", api_response)
#     except Exception as e:
#         st.sidebar.write("Error:", str(e))

# # Analytics Section
# def load_data(file_path):
#     return pd.read_csv(file_path)

# st.sidebar.header("Upload CSV File")
# uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# if uploaded_file:
#     data = load_data(uploaded_file)
#     st.sidebar.header("Filter Options")

#     # Filter options
#     post_types = st.sidebar.multiselect(
#         "Select Post Types:",
#         options=data["PostType"].unique(),
#         default=data["PostType"].unique()
#     )

#     # Apply filters
#     filtered_data = data[data["PostType"].isin(post_types)]

#     # Main content
#     st.header("🔍 Social Media Post Analytics")

#     # Display filtered data
#     st.subheader("Filtered Data")
#     st.dataframe(filtered_data)

#     # Key Metrics
#     st.header("Key Metrics")
#     col1, col2, col3, col4, col5 = st.columns(5)

#     with col1:
#         st.metric(label="Total Likes", value=filtered_data["Likes"].sum())
#     with col2:
#         st.metric(label="Total Comments", value=filtered_data["Comments"].sum())
#     with col3:
#         st.metric(label="Total Shares", value=filtered_data["Shares"].sum())
#     with col4:
#         st.metric(label="Total Views", value=filtered_data["Views"].sum())
#     with col5:
#         st.metric(label="Total Clicks", value=filtered_data["Clicks"].sum())

#     # Visualization section
#     st.header("Visual Analytics")

#     # Bar Chart: Likes by Post Type
#     st.subheader("Likes by Post Type")
#     bar_chart = px.bar(
#         filtered_data,
#         x="PostType",
#         y="Likes",
#         color="PostType",
#         title="Likes by Post Type",
#         labels={"Likes": "Number of Likes", "PostType": "Post Type"},
#         template="plotly_white"
#     )
#     bar_chart.update_layout(
#         title_font=dict(size=18, weight="bold"),
#         xaxis_title_font=dict(size=14, weight="bold"),
#         yaxis_title_font=dict(size=14, weight="bold"),
#         font=dict(size=12)
#     )
#     st.plotly_chart(bar_chart, use_container_width=True)

#     # Line Chart: Engagement Trends
#     st.subheader("Engagement Trends")
#     line_chart = px.line(
#         filtered_data.melt(id_vars=["PostType"], value_vars=["Likes", "Comments", "Shares", "Clicks"], var_name="Metric", value_name="Value"),
#         x="PostType",
#         y="Value",
#         color="Metric",
#         title="Engagement Trends by Post Type",
#         labels={"Value": "Engagement Value", "PostType": "Post Type"},
#         template="plotly_white"
#     )
#     line_chart.update_layout(
#         title_font=dict(size=18, weight="bold"),
#         xaxis_title_font=dict(size=14, weight="bold"),
#         yaxis_title_font=dict(size=14, weight="bold"),
#         font=dict(size=12)
#     )
#     st.plotly_chart(line_chart, use_container_width=True)

#     # Pie Chart: Views Distribution
#     st.subheader("Views Distribution")
#     pie_chart = px.pie(
#         filtered_data,
#         names="PostType",
#         values="Views",
#         title="Views Distribution by Post Type",
#         template="plotly_white"
#     )
#     pie_chart.update_layout(
#         title_font=dict(size=18, weight="bold"),
#         font=dict(size=12)
#     )
#     st.plotly_chart(pie_chart, use_container_width=True)

#     # Scatter Plot: Likes vs Comments
#     st.subheader("Likes vs Comments")
#     scatter_chart = px.scatter(
#         filtered_data,
#         x="Likes",
#         y="Comments",
#         color="PostType",
#         size="Shares",
#         hover_data=["Views", "Clicks"],
#         title="Likes vs Comments",
#         labels={"Likes": "Number of Likes", "Comments": "Number of Comments"},
#         template="plotly_white"
#     )
#     scatter_chart.update_layout(
#         title_font=dict(size=18, weight="bold"),
#         xaxis_title_font=dict(size=14, weight="bold"),
#         yaxis_title_font=dict(size=14, weight="bold"),
#         font=dict(size=12)
#     )
#     st.plotly_chart(scatter_chart, use_container_width=True)

# else:
#     st.header("Welcome to the Post Analytics Dashboard")
#     st.write("Please upload a CSV file to get started.")
import streamlit as st
from datetime import datetime

# Streamlit app configuration
st.set_page_config(page_title="Streamlit Row Layout", page_icon="📊", layout="wide")

# App title
st.title("📊 Streamlit App with Row Layout")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define chatbot response function
def chatbot_response(user_input):
    responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What can I do for you?",
        "bye": "Goodbye! Have a great day!",
    }
    return responses.get(user_input.lower(), "I'm not sure how to respond to that. Can you rephrase?")

# Row layout for Chatbot and Analytics
col1, col2 = st.columns([1, 2])

# Chatbot Section
with col1:
    st.header("🤖 Chatbot")
    with st.container():
        st.write("### Chat History")
        for sender, text, timestamp in st.session_state.chat_history:
            st.write(f"**{sender}** ({timestamp}): {text}")
    user_input = st.text_input("You:", "")
    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append(("You", user_input, datetime.now().strftime("%H:%M:%S")))
        response = chatbot_response(user_input)
        st.session_state.chat_history.append(("Chatbot", response, datetime.now().strftime("%H:%M:%S")))
        st.rerun()

# Analytics Section
with col2:
    st.header("📈 Analytics")
    st.write("This section can display your analytics data and visualizations.")

    # Example metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Metric 1", "100")
    with metric_col2:
        st.metric("Metric 2", "200")
    with metric_col3:
        st.metric("Metric 3", "300")

    # Example visualization placeholder
    st.write("### Example Visualization")
    st.area_chart({"data": [1, 2, 3, 4, 5]})

st.write("---")
st.write("This app demonstrates a row layout using Streamlit columns.")
