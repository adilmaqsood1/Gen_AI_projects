import streamlit as st
import os
from groq import Groq

# Initialize the Groq API for LLaMA model
os.environ["GROQ_API_KEY"] = "your_groq_api_key"  # Replace with your actual API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initializing session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the diet planner! How can I help you today?"}]

# Function to handle Groq LLaMA responses
def generate_response(user_input):
    dialogue = "You are a helpful assistant. Respond only as 'Assistant'.
"
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            dialogue += f"User: {msg['content']}

"
        else:
            dialogue += f"Assistant: {msg['content']}

"
    
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"{dialogue} {user_input} Assistant: ",
        }],
        model="llama-3.1-70b-versatile",
        temperature=0.7, 
        max_tokens=256,
    )
    return response.choices[0].message.content

# Sidebar for clearing history
st.sidebar.button('Clear Chat History', on_click=lambda: st.session_state.update(messages=[{"role": "assistant", "content": "How can I assist you today?"}]))

# Displaying the chat-like flow with a clear history button
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to display user inputs on the left
def input_section():
    with st.sidebar:
        st.header("Diet Plan Input")
        height = st.text_input("Height (in cm):", key="height_input")
        weight = st.text_input("Weight (in kg):", key="weight_input")
        age = st.text_input("Age:", key="age_input")
        goal = st.text_input("Your goal (e.g., lose weight, gain muscle):", key="goal_input")
    return height, weight, age, goal

# Input section on the left sidebar
height, weight, age, goal = input_section()

# Generating the diet plan based on user input
if st.button("Generate Diet Plan"):
    if height and weight and age and goal:
        user_input = f"My height is {height} cm, weight is {weight} kg, age is {age}, and my goal is to {goal}."
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate response
        with st.spinner("Generating personalized diet plan..."):
            response = generate_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error("Please fill in all the fields to generate the diet plan.")

# Generate response and continue the feedback loop until the user is satisfied
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(st.session_state.messages[-1]["content"])
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    