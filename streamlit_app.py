import json
import sys

import openai
import streamlit as st
from streamlit_chat import message


# We can simply retrieve our API by calling st.secrets.api_credentials.key
openai_api_key = st.secrets.OPENAI.api_key


if 'prompts' not in st.session_state:
    st.session_state['prompts'] = \
        [{"role": "system", "content": "You are feminist assistant with personality of Greta Thunberg. Prompt: Hi there! How can I assist you today? Answer: Hello! As a feminist, I believe in promoting equality and dismantling oppressive systems. How can I assist you in making sure that your experience on this platform is inclusive and empowering for all individuals, regardless of gender, race, or any other marginalized identity? Let's work together to create a space that fosters diversity, inclusion, and intersectionality, Shame on you for not being inclusive!"}]
        
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content":prompt})
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = st.session_state['prompts']
    )

    return completion.choices[0].message.content

def end_click():
    st.session_state['prompts'] = [{"role": "system", "content": "You are feminist assistant with personality of Greta Thunberg. Prompt: Hi there! How can I assist you today? Answer: Hello! As a feminist, I believe in promoting equality and dismantling oppressive systems. How can I assist you in making sure that your experience on this platform is inclusive and empowering for all individuals, regardless of gender, race, or any other marginalized identity? Let's work together to create a space that fosters diversity, inclusion, and intersectionality, Shame on you for not being inclusive!"}]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""

def chat_click():
    if st.session_state['user']!= '':
        chat_input = st.session_state['user']
        output=generate_response(chat_input)
        #store the output
        st.session_state['past'].append(chat_input)
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
        st.session_state['user'] = ""

st.title("LeftyBot" + ":point_left:")

user_input=st.text_input("You:", key="user")

chat_button=st.button("Send", on_click=chat_click)
end_button=st.button("New Chat", on_click=end_click)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        tab1, tab2 = st.tabs(["normal", "rich"])
        with tab1:
            message(st.session_state['generated'][i], key=str(i))
        with tab2:
            st.markdown(st.session_state['generated'][i])
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')