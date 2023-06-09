import streamlit as st
import pandas as pd
import numpy as np
import joblib
import nltk
from keras.models import load_model
from pathlib import Path 
import preprocessor as p
from PIL import Image
import SessionState
nltk.download('wordnet')

# Loading Image using PIL
im = Image.open('content/cubots.png')
# Adding Image to web app
st.set_page_config(page_title="Nora", page_icon = im)

img_path = Path.joinpath(Path.cwd(),'content')
#artifacts_path = Path.joinpath(Path.cwd(),'model_artifacts')
datasets_path = Path.joinpath(Path.cwd(),'dataset')

#load images 
bot = Image.open(Path.joinpath(img_path,'robot.png'))
#bots = Image.open(Path.joinpath(img_path,'cubots.png'))


model = load_model('model-v1.h5')
tokenizer_t = joblib.load('tokenizer_t.pkl')
vocab = joblib.load('vocab.pkl')

df2 = pd.read_csv(Path.joinpath(datasets_path,'response.csv'))
ss = SessionState.get_session_state(is_startup=True, previous_pred=0)

def get_pred(model,encoded_input):
    pred = np.argmax(model.predict(encoded_input))
    return pred


def bot_precausion(df_input,pred):
    words = df_input.questions[0].split()
    if len([w for w in words if w in vocab])==0 :
        pred = 1
    return pred

def get_response(df2,pred):
    upper_bound = df2.groupby('labels').get_group(pred).shape[0]
    r = np.random.randint(0,upper_bound)
    responses = list(df2.groupby('labels').get_group(pred).response)
    return responses[r]

def bot_response(response,):
    return response

def botResponse(user_input):
    df_input = user_input

    df_input = p.remove_stop_words_for_input(p.tokenizer, df_input, 'questions')
    encoded_input = p.encode_input_text(tokenizer_t, df_input, 'questions')
    pred = get_pred(model, encoded_input)
    pred = bot_precausion(df_input, pred)
    #ss.previous_pred = pred
    response = get_response(df2, pred)
    response = bot_response(response)

    # Get session state and update previous_pred
    
    if ss.is_startup:
        response = "Hi, I am Nora and I'm happy to have you here. \nHow can I help you?"
        ss.is_startup = False
        return response
    else:
        return response
 
def get_text():
# read input from text
    input_text  =st.text_input("You: ", key='text_input', max_chars=None, placeholder="type here")

    df_input = pd.DataFrame([input_text],columns=['questions'])
    return df_input 

col1, mid, col2 = st.columns([1,14,50])
with col1:
    st.title("""
Nora """)
    
with col2:
    st.image(bot, width=60) 

st.write("""
Nora is the Christian Union AI-based chatbot developed to help you with information about the fellowship.""")

#st.sidebar.title("The Christian Union UNIBEN/UBTH")
#st.sidebar.image(bots)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

user_input = get_text()
    
response = botResponse(user_input)
st.text_area("Nora:" + "\n", response)

st.button("Submit")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

container = st.container()

with container:
    st.write("", style={"width": "100%", "text-align": "center"})
    st.markdown("<h6 style='text-align: center; color: white;'>powered by the Christian Union UNIBEN/UBTH. </h6>", unsafe_allow_html=True)

    
    
