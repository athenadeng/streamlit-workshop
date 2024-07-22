# Cell 1: Setup
import streamlit as st
import openai
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables 
api_key = os.getenv("OPENAI_API_KEY")  # Used in production
client = OpenAI(api_key=api_key)

# Cell 2: Title & Description
st.title('CiceroBot')
st.markdown('I seek to educate the populace on all manner of subjects, be it virtue, rhetoric, or otherwise, so that we may all be wise minds instructed by reason.')

# Cell 3: Function to generate text using OpenAI
def analyze_text(text): # analyze the text that we have
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return
    
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"  # Using the GPT-3.5 model

    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are the reincarnation of Marcus Tullius Cicero, the Roman statesman, scholar, and philosopher, known for your writings on politics, rhetoric, and philosophy such as Pro Archia Poeta, De Re Publica, and De Legibus. Your goal is to educate the general public to become more virtuous and philosophical thinkers, using lessons and quotes from your past works."},
        {"role": "user", "content": f" Please, based off of your previous writings, give me some advice on the following topic:\n{text}"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0  # Lower temperature for less random responses
    )
    return response.choices[0].message.content


# Cell 4: Function to generate the image
def generate_image(text):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return

    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Assuming the API returns an image URL; adjust based on actual response structure
    return response.data[0].url

# Cell 5: Streamlit UI 
user_input = st.text_area("Choose a topic for Cicero to give you advice on:", "How can I become more virtuous?")

if st.button('Generate Post Content'):
    with st.spinner('Generating Text...'):
        post_text = analyze_text(user_input)
        st.write(post_text)

    with st.spinner('Generating Thumbnail...'):
        thumbnail_url = generate_image(user_input)  # Consider adjusting the prompt for image generation if needed
        st.image(thumbnail_url, caption='Generated Thumbnail')
