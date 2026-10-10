import os
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

    # Initialize Chat History with Updated Welcome Message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Ji Jamil! Aaj kesa man hai, shant ho na? Aaj kesa din raha aapka?"
                ),
            }
        ]

    # Display Chat History with Hinata Avatar
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
                # System prompt for personality & full context memory
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are Shushii, a smart, witty, and friendly AI companion, inspired by anime characters like Hinata."
                        " You speak in a natural mix of Hindi and English (Hinglish). You are talking to Jamil."
                        " You must remember ALL details and facts shared in the ongoing conversation history perfectly."
                    ),
                }

                # Full conversation history pass kar rahe hain (Zero memory loss)
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
# 🔊 SHUSHII VOICE PLAYER (Add at the very bottom)
# ==========================================
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if last_message["role"] == "assistant":
        try:
            from gtts import gTTS
            import io
            
            # Convert last Shushii response to speech
            tts = gTTS(text=last_message["content"], lang="hi")
            sound_file = io.BytesIO()
            tts.write_to_fp(sound_file)
            
            # Show audio player at the bottom
            st.audio(sound_file, format="audio/mp3")
        except Exception as e:
            pass





