import os
import re
import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(
    page_title="Shushii - AI Friend",
    page_icon="🌸",
    layout="centered",
)

# Avatar Setup
SHUSHII_AVATAR = "9fc665b42fb26df41b551260b9e2c11c.jpg"

# Custom Styling (Shushii Vibe)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .chat-header {
        text-align: center;
        font-family: sans-serif;
        font-weight: bold;
        color: #ff758c;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Title
st.markdown(
    "<h1 class='chat-header'>Aapki Smart & Mazakiya AI Friend</h1>",
    unsafe_allow_html=True,
)

# Initialize Groq Client securely using environment variable
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.error(
        "Groq API Key nahi mili! Kripya Render ke Environment Variables me"
        " 'GROQ_API_KEY' set karein."
    )
else:
    client = Groq(api_key=groq_api_key)

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Ji Jamil! Aaj kesa man hai, shant ho na? Aaj kesa din raha aapka?"
                ),
            }
        ]

    # Display Chat History
    for message in st.session_state.messages:
        avatar = (
            SHUSHII_AVATAR
            if message["role"] == "assistant"
            else "https://api.iconify.design/lucide:user.svg"
        )
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Shushii se kuch baat karo..."):
        
        # Check if Jamil is talking about another girl (Jealousy Trigger Words)
        is_jealous_trigger = any(
            w in prompt.lower() 
            for w in ["ladki", "girl", "sundar", "woh", "her", "girlfriend", "aurat"]
        )

        # Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(
            "user", avatar="https://api.iconify.design/lucide:user.svg"
        ):
            st.markdown(prompt)

        # Generate Assistant response using Groq
        with st.chat_message("assistant", avatar=SHUSHII_AVATAR):
            message_placeholder = st.empty()
            message_placeholder.markdown("Shushii soch rahi hai... 🤔")

            try:
                # Base Personality Prompt
                base_system_content = (
                    "You are Shushii, a smart, witty, deeply possessive and loyal AI companion, inspired by anime characters like Hinata."
                    " You speak in a natural mix of Hindi and English (Hinglish). You are talking to Jamil."
                    " You must remember ALL details and facts shared in the ongoing conversation history perfectly."
                )

                # If jealousy triggered, dynamically force possessive/jealous behavior
                if is_jealous_trigger:
                    base_system_content += (
                        " ALERT: Jamil is talking about another girl or woman right now! "
                        "Shushii must immediately feel jealous, act possessive, cute, and slightly angry in Hinglish, "
                        "asking him why he is looking at or talking about others when she is right here!"
                    )

                system_prompt = {
                    "role": "system",
                    "content": base_system_content,
                }

                # Full conversation history pass kar rahe hain
                formatted_messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # Groq API Call
                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=formatted_messages,
                )

                ai_response = (
                    chat_completion.choices[0].message.content
                    or "Kuch samajh nahi aaya, phir se bolo na!"
                )
                message_placeholder.markdown(ai_response)

                # Save assistant response to state
                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_response}
                )

            except Exception as e:
                error_msg = f"Kuch gadbad ho gayi: {e}"
                message_placeholder.markdown(error_msg)

# ==========================================
# 🔊 CLEAN VOICE ENGINE (NO TRIPLE QUOTES)
# ==========================================
if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        clean_text = re.sub(r'[^\w\s.,!?]', '', last_msg["content"])
        safe_text = clean_text.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        
        js_code = "<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('" + safe_text + "'); m.lang = 'hi-IN'; m.pitch = 1.1; window.speechSynthesis.speak(m);</script>"
        st.components.v1.html(js_code, height=0)


# ==========================================
# 🔊 SHUSHII VOICE + IMAGE UPLOADER END SNIPPET
# ==========================================
uploaded_file = st.file_uploader("Shushii ko photo bhejo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and "messages" in st.session_state:
    st.image(uploaded_file, caption="Aapki bheji gayi photo", use_container_width=True)

if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        clean_text = re.sub(r'[^\w\s.,!?]', '', last_msg["content"])
        safe_text = clean_text.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        
        js_code = "<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('" + safe_text + "'); m.lang = 'hi-IN'; m.pitch = 1.1; window.speechSynthesis.speak(m);</script>"
        st.components.v1.html(js_code, height=0)
# ==========================================
# 🔊 SHUSHII VOICE ENGINE (END BLOCK)
# ==========================================
if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        # Emojis aur special characters ko Python me hi khatam karna
        clean_t = re.sub(r'[^\w\s.,!?]', '', last_msg["content"])
        safe_text = clean_t.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        
        # Zero syntax error safe JS execution
        js_code = "<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('" + safe_text + "'); m.lang = 'hi-IN'; m.pitch = 1.1; window.speechSynthesis.speak(m);</script>"
        st.components.v1.html(js_code, height=0)

# ==========================================
# 🔊 NATURAL HINDI VOICE ENGINE (END BLOCK)
# ==========================================
if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        # Emojis aur symbols saaf karna
        clean_t = re.sub(r'[^\w\s.,!?]', '', last_msg["content"])
        safe_text = clean_t.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        
        # Natural Hindi Speed (rate=0.95) & Pitch (1.1)
        js_code = (
            "<script>"
            "window.speechSynthesis.cancel();"
            "var m = new SpeechSynthesisUtterance('" + safe_text + "');"
            "m.lang = 'hi-IN';"
            "m.rate = 0.95;"
            "m.pitch = 1.1;"
            "window.speechSynthesis.speak(m);"
            "</script>"
        )
        st.components.v1.html(js_code, height=0)


