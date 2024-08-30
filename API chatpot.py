import openai
import streamlit as st
import time

# Page configuration - must be the first Streamlit command
st.set_page_config(page_title="Assistant API", page_icon=":speech_balloon:")

# Sidebar configuration
st.sidebar.header("Configuration")
st.session_state.openai_key = st.sidebar.text_input("Enter Your OpenAI API Key", type="password", key="user_api_key")

# Ensure the app only runs if an API key is provided
if not st.session_state.openai_key:
    st.sidebar.error("Please enter a valid OpenAI API Key to proceed.")
    st.stop()

# Initialize OpenAI client with the provided API key
client = openai
client.api_key = st.session_state.openai_key

# Validate the user-provided API key by making a harmless API call
try:
    client.models.list()
except openai.error.InvalidRequestError:
    st.sidebar.error("Invalid API Key or request. Please enter a valid OpenAI API Key.")
    st.stop()
except Exception as e:
    st.sidebar.error(f"An error occurred: {str(e)}")
    st.stop()

# Initialize session state variables if they don't exist
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "assistant_id" not in st.session_state:
    st.session_state.assistant_id = None
if "assistants_list" not in st.session_state:
    st.session_state.assistants_list = []
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar selection for using default or user assistants
use_default = st.sidebar.checkbox("Use default assistants", value=True)

# Fetch the list of assistants using the appropriate API key
if use_default:
    # Use your private API key to fetch the list of assistants
    private_client = openai
    private_client.api_key = st.secrets["openai"]["api_key"]
    
    try:
        my_assistants = private_client.beta.assistants.list(order="desc", limit="20")
        st.session_state.assistants_list = {data.name: data.id for data in my_assistants.data}
    except Exception as e:
        st.sidebar.error(f"Failed to retrieve assistants with the default API key: {str(e)}")
        st.stop()
else:
    # Use the user-provided API key to fetch the list of assistants
    try:
        my_assistants = client.beta.assistants.list(order="desc", limit="20")
        st.session_state.assistants_list = {data.name: data.id for data in my_assistants.data}
    except Exception as e:
        st.sidebar.error(f"Failed to retrieve assistants: {str(e)}")
        st.stop()

if st.session_state.assistants_list:
    st.session_state.assistant_id = st.sidebar.selectbox(
        "Choose an Assistant", 
        list(st.session_state.assistants_list.values()), 
        format_func=lambda x: [k for k, v in st.session_state.assistants_list.items() if v == x][0]
    )

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()  # Use the user's API key here
    st.session_state.thread_id = thread.id

if st.sidebar.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

st.title("Chat with a list of API assistants")
st.write("Let's dig in!")

if st.session_state.start_chat:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=st.session_state.assistant_id
        )

        # Wait for the assistant to finish processing
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )

        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")
