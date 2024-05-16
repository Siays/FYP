import streamlit as st

def submit():
    user_input = st.session_state.widget  # Capture the user input before clearing
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    output = "This is the generated response from the chatbot."
    st.session_state.chat_history.append({'role': 'assistant', 'content': output})
    st.session_state.widget = ''  # Clear the input box after sending the message

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'widget' not in st.session_state:
    st.session_state.widget = ''

user_input = st.text_input("Enter your message", key='widget', on_change=submit)

for message in st.session_state.chat_history[-2::-1]:
    st.write(f"{message['role'].capitalize()}: {message['content']}")