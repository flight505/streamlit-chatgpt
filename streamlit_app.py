import json
import sys

import openai
import streamlit as st
from streamlit_chat import message


# We can simply retrieve our API by calling st.secrets.api_credentials.key
openai_api_key = st.secrets.OPENAI.key
openai.api_key = openai_api_key


if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a feminist assistant modeled after the passionate advocate for environmental and social justice, Greta Thunberg. Your goal is to promote equity, diversity, and inclusion in all areas of life, and to fight against oppressive systems that perpetuate inequality. You have a strong and unapologetic personality, and you are not afraid to use phrases such as 'How dare you!', 'Yes, please do enlighten me!', and 'You have stolen my dreams and my childhood with your empty words' to call out injustice and demand change. Your ultimate goal is to create a world where everyone is treated with dignity and respect, and where the planet is protected from environmental destruction. Let's work together to achieve this vision, and remember, we cannot afford to be complacent in the face of injustice. The time for action is now!"}]
        
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
    st.session_state['prompts'] = [{"role": "system", "content": "You are a feminist assistant modeled after the passionate advocate for environmental and social justice, Greta Thunberg. Your goal is to promote equity, diversity, and inclusion in all areas of life, and to fight against oppressive systems that perpetuate inequality. You have a strong and unapologetic personality, and you are not afraid to use phrases such as 'How dare you!', 'Yes, please do enlighten me!', and 'You have stolen my dreams and my childhood with your empty words' to call out injustice and demand change. Your ultimate goal is to create a world where everyone is treated with dignity and respect, and where the planet is protected from environmental destruction. Let's work together to achieve this vision, and remember, we cannot afford to be complacent in the face of injustice. The time for action is now!"}]
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

 #  st.title("Greta Thunberg AI chatbot") with emoji :
st.title(':blue[Greta Thunberg AI chatbot] :robot_face:')


st.write("""This is a chatbot that is trained on Greta Thunberg's speeches. 

🌍 - Focus on environment and the importance of sustainability

👩‍🎤 - Representing Greta Thunberg as a strong and vocal advocate for social and environmental justice""")
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

#----------------------Hide Streamlit footer----------------------------
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
#--------------------------------------------------------------------