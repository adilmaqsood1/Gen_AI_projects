import streamlit as st
import os
from groq import Groq

# Initialize the Groq API for LLaMA model
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Set a predefined temperature value (used in the API call but not shown to the user)
temperature = 0.1  # You can adjust this as needed

# Set up the main app layout
st.set_page_config(page_title="Llama Diet Assistant", layout="wide")

# Sidebar for user inputs
with st.sidebar:
    st.title('Llama Diet Assistant')
    

    # if 'GROQ_API_KEY' in os.environ:
    #     st.success('API key already provided!', icon='✅')
    # else:
    #     st.warning('Please set your API key!', icon='⚠️')

    # Diet plan input section
    st.header("Diet Plan Input")
    height = st.text_input("Height (in cm):", key="height_input")
    weight = st.text_input("Weight (in kg):", key="weight_input")
    age = st.text_input("Age:", key="age_input")
    goal = st.text_input("Your goal (e.g., lose weight, gain muscle):", key="goal_input")
    
    # Button to clear chat history
    st.button('Clear Chat History', on_click=lambda: st.session_state.clear())

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the diet planner! Please provide your details to get started."}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to handle Groq LLaMA responses
def generate_response(user_input):
    dialogue = "You are a helpful assistant. Respond only as 'Assistant'.\n"
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            dialogue += f"User: {msg['content']}\n\n"
        else:
            dialogue += f"Assistant: {msg['content']}\n\n"
    
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"{dialogue} {user_input} Assistant: ",
        }],
        model="llama-3.1-70b-versatile",
        temperature=temperature  # Use the predefined temperature value
    )
    return response.choices[0].message.content

# If the diet plan has not been generated, ask for input
if "diet_plan_generated" not in st.session_state or not st.session_state.diet_plan_generated:
    if st.button("Generate Diet Plan"):
        if height and weight and age and goal:
            user_input = f"My height is {height} cm, weight is {weight} kg, age is {age}, and my goal is to {goal}."
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Generate response for diet plan
            with st.spinner("Generating personalized diet plan..."):
                response = generate_response(user_input)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.diet_plan_generated = True  # Mark diet plan as generated
        else:
            st.error("Please fill in all the fields to generate the diet plan.")
else:
    # If the diet plan is generated, allow for further conversation
    prompt = st.chat_input(placeholder="Ask anything about your diet plan or goals:", key="user_input")
    
    # Trigger response generation right after user input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response to the user's query immediately after input
        with st.spinner("Assistant is thinking..."):
            response = generate_response(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Show the assistant's response if it hasn't been shown already
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            st.write(st.session_state.messages[-1]["content"])
