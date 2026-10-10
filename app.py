import os
import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(
    page_title="Shushii - AI Friend",
    page_icon="🌸",
    layout="centered",
)

# ==========================================
# "9fc665b42fb26df41b551260b9e2c11c.jpg"
# ==========================================
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
                    "Hey! Main Shushii hoon, aapki dost. Aaj kya baat"
                    " karni hai?"
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

    # Future Voice Integration Placeholder
    # TODO: Future me yahan voice input / audio recording ka code add kiya ja sakega.

    # User Input
    if prompt := st.chat_input("Shushi se kuch baat karo..."):
        # Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(
            "user", avatar="https://api.iconify.design/lucide:user.svg"
        ):
            st.markdown(prompt)

        # Generate Assistant response using Groq (Updated Model)
        with st.chat_message("assistant", avatar=SHUSHII_AVATAR):
            message_placeholder = st.empty()
            message_placeholder.markdown("Shushii soch rahi hai... 🤔")

            try:
                # System prompt to give Shushii her personality
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are Shushii, a smart, witty, and friendly AI"
                        " companion, inspired by anime characters. You speak"
                        " in a cool mix of Hindi and English (Hinglish),"
                        " friendly, casual, and sometimes humorous tone."
                    ),
                }

                # Format messages for Groq API
                formatted_messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # API Call to Groq with active model
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
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


