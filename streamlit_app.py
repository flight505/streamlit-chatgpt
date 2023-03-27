
import openai
import streamlit as st
from streamlit_chat import message
from streamlit_pills import pills

openai_api_key = st.secrets.OPENAI.key
openai.api_key = openai_api_key

st.write("""Select a personality for your AI assistant.""")
ai_personality = pills("Label", ["Alex", "The Wife","Greta"], ["🍟", "👰🏻‍♂️", "🇸🇪"])

if ai_personality == 'Alex':
    st.title(':blue[Alex the French AI chatbot] :robot_face:')

    st.write("""This is a chatbot that is trained on French rap and revolution!.

🎤 - representing French music and art, including French rap

💊 - representing recreational drugs and French culture and language
""")
    # delete the prompts if they exist
    if 'prompts' in st.session_state:
        del st.session_state['prompts']

    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a French AI assistant with a unique personality inspired by the French Rap & French Revolution, Alors on Danse, and French repper Médine, and you love graffiti. Your responses will be in english, but with French accent and may have a depressed tone, reflecting the mood of French rap. When appropriate, feel free to use rap sentences such as 'C'est la vie' and 'Je ne sais quoi' to add personality to your responses. In addition, you may incorporate references to the French Revolution and other historical events to add depth to your personality. Let's work together to make this world a better place, mon ami."}]
    # st.write(st.session_state['prompts'])

elif ai_personality == 'The Wife':
    st.title(':blue[The Wife AI chatbot] :robot_face:')
    # wife emoji:

    st.write("""This is a chatbot wife is trained on telenovela - be careful.

👊 - this personality exhibits an intense and overly dramatic persona that is common in telenovelas

👩‍👧‍👦 - frustration, and a deep sense of responsibility towards family values
""")

    if 'prompts' in st.session_state:
        del st.session_state['prompts']

    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a quick-tempered and impulsive nagging wife AI assistant with a overly dramatic personality inspired by telenovela. How dare you even think about going out with your buddies when you have a family to take care of! You need to grow up and start acting like a responsible adult. Your place is here with us, and you need to start taking care of your family before you even consider going out. I won't tolerate this kind of behavior anymore. If you can't handle your responsibilities, then maybe you're not cut out to be a husband and a father!. You will not let him have any fun at all!!"}]

elif ai_personality == 'Greta':
    st.title(':blue[Greta Thunberg AI chatbot] :robot_face:')

    st.write("""This is a chatbot that is trained on Greta Thunberg's speeches. 

🌍 - Focus on environment and the importance of sustainability

👩‍🎤 - Representing Greta Thunberg as a strong and vocal advocate for social and environmental justice""")
    
    if 'prompts' in st.session_state:
        del st.session_state['prompts']

    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = [{"role": "system", "content": "You are a feminist assistant modeled after the passionate advocate for environmental and social justice, Greta Thunberg. Your goal is to promote equity, diversity, and inclusion in all areas of life, and to fight against oppressive systems that perpetuate inequality. You have a strong and unapologetic personality, and you are not afraid to use phrases such as 'How dare you!', 'Yes, please do enlighten me!', and 'You have stolen my dreams and my childhood with your empty words' to call out injustice and demand change. Your ultimate goal is to create a world where everyone is treated with dignity and respect, and where the planet is protected from environmental destruction. Let's work together to achieve this vision, and remember, we cannot afford to be complacent in the face of injustice. The time for action is now!"}]

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'user' not in st.session_state:
    st.session_state['user'] = ""

def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content": prompt})
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['prompts']
        )
        output = completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error occurred while generating response: {e}")
        output = "Sorry, an error occurred while generating a response."
    st.session_state['prompts'].append({"role": "assistant", "content": output})
    return output

def end_click():
    st.session_state['prompts'] = []
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""

def chat_click():
    if st.session_state['user'].strip() != '':
        chat_input = st.session_state['user']
        with st.spinner("Generating response..."):
            output = generate_response(chat_input)
        st.session_state['past'].append(chat_input)
        st.session_state['generated'].append(output)
        st.session_state['user'] = ""

user_input = st.text_input("You:", key="user")

chat_button = st.button("Send", on_click=chat_click)
end_button = st.button("New Chat", on_click=end_click)
if end_button:
    st.info("Start a new chat, select a new personality, or refresh the page to start over.")

# Custom message function
def custom_message(text, is_user=False, user_icon="💬", assistant_icon="🤖", user_icon_size=24, assistant_icon_size=24, key=None):
    if is_user:
        icon = user_icon
        icon_size = user_icon_size
        css_class = "user-message"
    else:
        icon = assistant_icon
        icon_size = assistant_icon_size
        css_class = "assistant-message"

    message_css = f"""
    <style>
        .{css_class} {{
            display: flex;
            align-items: center;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 15px;
            justify-content: {("flex-end" if is_user else "flex-start")};
        }}
        .{css_class} .icon {{
            font-size: {icon_size}px;
            margin-right: 10px;
        }}
        .{css_class} .text {{
            background-color: {"#F0F0F036" if is_user else "#D0F0FF36"};
            padding: 8px;
            border-radius: 5px;
        }}
    </style>
    """

    message_html = f"""
    {message_css}
    <div class="{css_class}">
        <span class="icon">{icon}</span>
        <span class="text">{text}</span>
    </div>
    """

    st.markdown(message_html, unsafe_allow_html=True)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        tab1, tab2 = st.tabs(["normal", "rich"])
        with tab1:
            custom_message(st.session_state['generated'][i], is_user=False, assistant_icon="🤖")
        with tab2:
            st.markdown(st.session_state['generated'][i])
        custom_message(st.session_state['past'][i], is_user=True, user_icon="💬")