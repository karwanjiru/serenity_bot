import streamlit as st
import openai
import os

# App title
st.set_page_config(page_title="SerenityBot 🌸")

# OpenAI Credentials
with st.sidebar:
    st.title('SerenityBot 🌸')
    st.write('Your friendly mental health companion here to support you :)')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter OpenAI API key:', type='password')
        if not openai_api_key:
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['OPENAI_API_KEY'] = openai_api_key

    st.markdown('Talk to a 👩‍⚕️[qualified personnel](link to website here) today😊')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
# Button to clear chat history
if st.sidebar.button('Clear Chat History', on_click=clear_chat_history):
    pass  # Placeholder, action handled in clear_chat_history function

# Button to start a new chat
if st.sidebar.button('New Chat'):
    st.session_state.messages = [{"role": "assistant", "content": "Hello. How may I assist you today?"}]

# Function for generating OpenAI response
def generate_openai_response(prompt_input):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only answers questions related to mental health and general health. If a user asks a question outside of these topics, respond politely by explaining that you are only able to assist with mental health and general health inquiries."}
        ] + st.session_state.messages + [{"role": "user", "content": prompt_input}]
    )
    return response['choices'][0]['message']['content']

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if the last message is not from the assistant
    if st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("..."):
                response = generate_openai_response(prompt)
                st.write(response)  # Display the response
                st.session_state.messages.append({"role": "assistant", "content": response})

