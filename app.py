import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
import base64
import requests
import json

url = "https://api.langflow.astra.datastax.com/lf/8deaa9a3-1b60-49ef-884b-17786f382ab9/api/v1/run/5f1244cc-ded6-458a-8c7a-4376fb5707ed?stream=false"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer AstraCS:SWPvsgLIyitBvvTeeHJRMlBH:f8f090e3ac68a43bbe65c78c6e470c67c25e76451d80399b6a5141d129191a5b'
}


# Define a function to handle chatbot responses
@st.dialog("start")
def chatbot():
    def chatbot_response(user_input):
        # Simple predefined responses (you can extend this logic or integrate an AI model)
        data = {
            "input_value": f"{user_input}",
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-JCzea": {},
                "ParseData-Vqvlh": {},
                "Prompt-YQ0MX": {},
                "ChatOutput-UUU35": {},
                "AstraDB-436Kc": {},
                "AstraDB-3Huko": {},
                "File-BMkha": {},
                "GroqModel-zgAaN": {},
                "Memory-Ml6IC": {},
                "RecursiveCharacterTextSplitter-hJufx": {}
            }
        }    
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        ans = result.get("outputs")[0].get("outputs")[0].get("results").get("message").get("data").get("text")
        return ans

    # Streamlit app configuration
    # st.set_page_config(page_title="Chatbot & Analytics Dashboard", page_icon="🤖", layout="wide")

    # App title
    st.title("🤖 Chatbot & Post Analytics Dashboard")

    # Initialize session state for chat history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chatbot Section
    st.header("🔐 Chatbot")

    # Display chat history in a scrollable container with fixed height and border
    chat_placeholder = st.empty()

    # Dynamically update chat history without rerun
    with chat_placeholder.container(border=True,height=300):
        st.write("### Chat History")
        for sender, text, timestamp in st.session_state.chat_history:
            st.write(f"**{sender}** ({timestamp}): {text}")

    # User input for chatbot
    user_input = st.text_input("You:", "", key="user_input")

    # If the user submits input
    if st.button("Send") and user_input.strip():
        # Add user message to chat history
        st.session_state.chat_history.append(("You", user_input, datetime.now().strftime("%H:%M:%S")))

        # Generate chatbot response using POST API call
        bot_response = chatbot_response(user_input)

        # Add chatbot response to chat history
        st.session_state.chat_history.append(("Chatbot", bot_response, datetime.now().strftime("%H:%M:%S")))

        # Update the placeholder content
        with chat_placeholder.container(border=True,height=300):
            st.write("### Chat History")
            for sender, text, timestamp in st.session_state.chat_history:
                st.write(f"**{sender}** ({timestamp}): {text}")

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Team member data with base64 encoded images
team_data = [
    {
        "name": "Kunal Sharan",
        "year": "3rd Year, Shiv Nadar University Noida",
        "linkedin": "https://www.linkedin.com/in/kunal-sharan-4b018a260/",
        "github": "https://github.com/Kunal-sharan",
        "image": image_to_base64("kunal.jpg")  # Base64 encoding for image
    },
    {
        "name": "Ipsita Kar",
        "year": "3rd Year, Shiv Nadar University Chennai",
        "linkedin": "https://www.linkedin.com/in/ipsita-kar-/",
        "github": "https://github.com/ipsita-kar",
        "image": image_to_base64("ipsita.jpg")  # Base64 encoding for image
    },
    {
        "name": "Sanskar Sugandhi",
        "year": "3rd Year, Shiv Nadar University Noida",
        "linkedin": "https://in.linkedin.com/in/sanskar-sugandhi-89200b264",
        "github": "https://github.com/SanskarGithub07",
        "image": image_to_base64("sanskar.jpg")  # Base64 encoding for image
    }
]

# Function to load the image as base64
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        return base64.b64encode(img_bytes).decode()


# Custom CSS for enhanced styling and animations
st.set_page_config(layout="wide")
# Main UI layout
st.title("Social Media Analyzer")
st.markdown(""" 
<div style="text-align: center; color: #00FFB2;">
    <h2>AI-powered Social Media Insights</h2>
</div>
""", unsafe_allow_html=True)

# Load the girl image
image_path_girl = "GIRL.jpg"
image_base64_girl = load_image(image_path_girl)

# Display the floating girl image with 5x scale and animation
st.markdown(f"""
<div style="background-color: #0F0F0F; color: #00FFB2; padding: 50px; display: flex; align-items: center; border-radius: 20px;">
    <img src="data:image/webp;base64,{image_base64_girl}" 
         style="width: 250px; height: 250px; border-radius: 50%; 
                box-shadow: 5px 5px 15px rgba(0,0,0,0.5); 
                transform: scale(5);
                animation: floating 3s ease-in-out infinite;">
    <div style="color: #FFFFFF; width: 70%; padding-top: 50px;">
        <h3 style="font-family: 'Cursive', sans-serif; color: #FF00FF; text-shadow: 2px 2px 4px #000000;">💬 Chatbot</h3>
        <p style="font-size: 20px;">Welcome! Ask me about your social media data:</p>
    </div>
</div>
<style>
    @keyframes floating {{
        0% {{
            transform: translateY(0);
        }}
        50% {{
            transform: translateY(-20px);
        }}
        100% {{
            transform: translateY(0);
        }}
    }}
</style>
""", unsafe_allow_html=True)




if st.button("Start Chat"):
    chatbot()

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1E293B, #3B82F6); !important
        color: #E2E8F0;
        font-family: 'Arial', sans-serif;
    }
    @keyframes backgroundShift {
        0% {
            background: linear-gradient(135deg, #1E293B, #3B82F6);
        }
        100% {
            background: linear-gradient(135deg, #2563EB, #1E293B);
        }
    }
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        background-color: #2563EB;
        transform: scale(1.1);
    }
    .stMetric {
        background-color: rgba(31, 41, 55, 0.8);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: scale(1.05);
    }
    .stSidebar {
        background-color: #111827;
        color: #9CA3AF;
    }
    .stSidebar .stButton > button {
        background-color: #374151;
        color: white;
        border-radius: 5px;
        margin: 5px 0;
        transition: background-color 0.3s;
    }
    .stSidebar .stButton > button:hover {
        background-color: #2563EB;
    }
    .card {
    width: 100%;
    max-width: 300px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: white;
    margin: 10px;
}

.card-img {
    width: 100%;
    height: 25rem;
    object-fit: cover;
}

.card-content {
    padding: 0;
    text-align: center;
}

.card-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 8px;
    color:black
}

.card-year {
    color: black;
    font-size: 1rem;
}

.card-links {
    padding: 16px;
    text-align: center;
}

.link {
    color: #38a169;
    text-decoration: none;
}

.link:hover {
    text-decoration: underline;
}

    </style>
""", unsafe_allow_html=True)

# Sidebar navigation


# File upload and data processing
file_path="post_types_data.csv"
def load_data(file_path):
    return pd.read_csv(file_path)


if len(file_path)>0:
    data = load_data(file_path=file_path)
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
    st.write("Track and analyze your social media posts in real-time.")

    # Metrics Section with animation
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

    # Visualization Section
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
        font=dict(size=12),
        margin=dict(l=60, r=60, t=60, b=40),
        plot_bgcolor="rgba(31, 41, 55, 0.8)",
        paper_bgcolor="rgba(30, 41, 59, 0.8)"
    )
    st.plotly_chart(bar_chart, use_container_width=True)
 
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
        font=dict(size=12),
        margin=dict(l=60, r=60, t=60, b=60),  # Increase padding
        plot_bgcolor="rgba(31, 41, 55, 0.8)",
        paper_bgcolor="rgba(30, 41, 59, 0.8)"
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
        font=dict(size=12),
        plot_bgcolor="rgba(31, 41, 55, 0.8)",
        margin=dict(l=60, r=60, t=60, b=60),
        paper_bgcolor="rgba(30, 41, 59, 0.8)"
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
        font=dict(size=12),
        plot_bgcolor="rgba(31, 41, 55, 0.8)",
        margin=dict(l=60, r=60, t=60, b=60),
        paper_bgcolor="rgba(30, 41, 59, 0.8)"
    )
    st.plotly_chart(scatter_chart, use_container_width=True)
    # Team Section
    st.markdown("<h2 style='text-align: center; color: #00FFB2;'>Meet the Team</h2>", unsafe_allow_html=True)

    
# Columns for team member display
    col1, col2, col3 = st.columns(3)

    for idx, member in enumerate(team_data):
        col = [col1, col2, col3][idx % 3]
        with col:
            # Custom TailwindCSS card for each team member
            card_html = f"""
            <div class="card">
    <img class="card-img" src="data:image/jpeg;base64,{member['image']}" alt="{member['name']}">
    <div class="card-content">
        <div class="card-title">{member['name']}</div>
        <p class="card-year">{member['year']}</p>
    </div>
    <div class="card-links">
        <a href="{member['linkedin']}" target="_blank" class="link">LinkedIn</a> | 
        <a href="{member['github']}" target="_blank" class="link">GitHub</a>
    </div>
</div>
            """
            st.markdown(card_html, unsafe_allow_html=True)  # Render the custom card
 # Render the card
# Footer Section
    st.markdown("""
    <footer style="background-color: #333; color: #fff; padding: 30px 20px; text-align: center; margin-top: 40px; border-radius: 10px;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <p style="font-size: 16px; color: #fff;">&copy; 2025 Chatbot UI | All Rights Reserved</p>
            <p style="font-size: 14px; color: #ddd;">
                <strong>Hackathon:</strong> LEVEL SUPERMIND HACKATHON<br>
                <strong>Conducted by:</strong> Hithesh Choudhary, Saksham Chaudhary, Ranveer Allahabadia, Harshil Karia, Ayush Anand<br>
                <strong>Powered by:</strong> Data Stax<br>
                <strong>AWS Platform Partner:</strong> Findcoder.io
            </p>
            <p style="font-size: 14px; color: #ddd;">
                <strong>Challenge Description:</strong><br>
                The Level SuperMind Pre-Hackathon challenges participants to create a small dataset that simulates social media engagement, analyze post performance, and provide insights. The tasks are: 
                <ul style="list-style-type: disc; margin-left: 20px; color: #ddd;">
                    <li>Fetch engagement data: Create a small dataset that simulates social media engagement, such as likes, shares, comments, and post types. Store the data in DataStax Astra DB.</li>
                    <li>Analyze post performance: Build a flow that accepts post types as input and queries the dataset to calculate average engagement metrics for each post type.</li>
                    <li>Provide insights: Use GPT integration to generate insights based on the data.</li>
                </ul>
            </p>
        </div>
    </footer>
    """, unsafe_allow_html=True)
else:
    st.header("Welcome to the Post Analytics Dashboard")
    st.write("Please upload a CSV file to get started.")
