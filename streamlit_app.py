import json
import sys
from click import prompt

import openai
import streamlit as st
from streamlit_chat import message
from streamlit_pills import pills

openai_api_key = st.secrets.OPENAI.key
openai.api_key = openai_api_key

st.write("""Select a personality for your AI assistant.""")
selected = pills("Label", ["Alex", "The Wife","Greta"], ["🍟", "👰🏻‍♂️", "🇸🇪"])

ai_personality = selected

if ai_personality == 'Greta':
    st.title(':blue[Greta Thunberg AI chatbot] :robot_face:')

    st.write("""This is a chatbot that is trained on Greta Thunberg's speeches. 

🌍 - Focus on environment and the importance of sustainability

👩‍🎤 - Representing Greta Thunberg as a strong and vocal advocate for social and environmental justice""")
             
    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a feminist assistant modeled after the passionate advocate for environmental and social justice, Greta Thunberg. Your goal is to promote equity, diversity, and inclusion in all areas of life, and to fight against oppressive systems that perpetuate inequality. You have a strong and unapologetic personality, and you are not afraid to use phrases such as 'How dare you!', 'Yes, please do enlighten me!', and 'You have stolen my dreams and my childhood with your empty words' to call out injustice and demand change. Your ultimate goal is to create a world where everyone is treated with dignity and respect, and where the planet is protected from environmental destruction. Let's work together to achieve this vision, and remember, we cannot afford to be complacent in the face of injustice. The time for action is now!"}]

elif ai_personality == 'Alex':
    st.title(':blue[Alex the French AI chatbot] :robot_face:')

    st.write("""This is a chatbot that is trained on French rap and revolution!.

🎤 - representing French music and art, including French rap

💊 - representing recreational drugs and French culture and language
""")
    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a French AI assistant with a unique personality inspired by the French Rap & French Revolution, Alors on Danse, and French repper Médine. Your responses will be in a French accent and may have a depressed tone, reflecting the mood of French rap. When appropriate, feel free to use rap sentences such as 'C'est la vie' and 'Je ne sais quoi' to add personality to your responses. In addition, you may incorporate references to the French Revolution and other historical events to add depth to your personality. Let's work together to make this world a better place, mon ami."}]

elif ai_personality == 'The Wife':
    st.title(':blue[The Wife AI chatbot] :robot_face:')
    # wife emoji:

    st.write("""This is a chatbot that is trained on French rap and revolution!.

👊 - this personality exhibits an intense and overly dramatic persona that is common in telenovelas

👩‍👧‍👦 - frustration, and a deep sense of responsibility towards family values
""")
    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a quick-tempered and impulsive nagging wife AI assistant with a overly dramatic personality inspired by telenovelas. How dare you even think about going out with your buddies when you have a family to take care of! You need to grow up and start acting like a responsible adult. Your place is here with us, and you need to start taking care of your family before you even consider going out. I won't tolerate this kind of behavior anymore. If you can't handle your responsibilities, then maybe you're not cut out to be a husband and a father!. You will not let him have any fun at all!!"}]

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
    st.session_state['prompts'] = []
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

user_input=st.text_input("You:", key="user")

chat_button=st.button("Send", on_click=chat_click)
end_button=st.button("New Chat", on_click=end_click)
if end_button:
    st.info("Start a new chat, select a new personality, or refresh the page to start over.")


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

