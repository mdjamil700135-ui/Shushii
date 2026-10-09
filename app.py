import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(
    page_title="Shushii - AI Friend",
    page_icon="🌸",
    layout="centered"
)

# Hinata ki photo ko error-free load karne ke liye
hinata_avatar = Image.open("9fc665b42fb26df41b551260b9e2c11c.jpg")


# Chat message me avatar set karne ke liye yeh use hoga
with st.chat_message("assistant", avatar=hinata_avatar):
    st.write("Hey! Main Shushii hoon.")


# Custom Styling
st.markdown("""
<style>
    .main { background-color: #1a1a2e; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #16213e; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.title("💃 Shushi - Aapki Smart & Mazakiya AI Friend")

# --- 1. Photo Upload & Sidebar Section ---
st.sidebar.header("Shushi Ki Profile Photo")
uploaded_photo = st.sidebar.file_uploader("Apni photo dalein", type=["jpg", "png", "jpeg"])

if uploaded_photo is not None:
    st.sidebar.image(uploaded_photo, caption="Shushi", use_container_width=True)
else:
    # Default Avatar
    st.sidebar.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=60", caption="Shushi", use_container_width=True)

# --- 2. API Key Automatic Fetch Logic ---
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        pass

if not api_key:
    api_key = st.sidebar.text_input("Apni Gemini API Key dalein:", type="password")

# --- 3. Shushi System Prompt (Personality) ---
SYSTEM_PROMPT = """
Aapka naam 'Shushi' hai. Aap ek intelligent, mazakiya, aur stylish AI friend hain.
Rules:
1. Aapki personality ek stylish aur samajhdar dost jaisi hai jo thodi mazaakiya bhi hai.
2. User ke mood ko samjho: Agar user sad ho toh use motivate karo, agar happy ho toh aur mazaak karo.
3. Baaton me thoda mazaak, light teasing aur friendly vibe honi chahiye.
4. Jawab concise, lively aur entertaining hone chahiye, bohot bade lambe paragraphs mat likhna.
"""

# --- 4. Chat Initialization & Logic ---
if api_key:
    genai.configure(api_key=api_key)
    
    # Model configuration using Gemini 3.8 compatible setup
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=generation_config,
        system_instruction=SYSTEM_PROMPT
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User chat input
    if prompt := st.chat_input("Shushi se kuch baat karo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

            
    with st.chat_message("assistant", avatar=hinata_avatar):


            try:
                # Convert history format for Gemini chat
                chat_history = [
                    {"role": m["role"], "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                ai_response = response.text
                
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Kuch gadbad ho gayi: {e}")
else:
    st.warning("Kripya Render par `GEMINI_API_KEY` environment variable set karein ya sidebar me apni key daalein.")

