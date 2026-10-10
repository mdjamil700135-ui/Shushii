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
# 🔊 SHUSHii INSTANT BROWSER VOICE (100% WORKING)
# ==========================================
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if last_message["role"] == "assistant":
        # Text me se quotes remove kar rahe hain taaki JS break na ho
        clean_text = (
            last_message["content"]
            .replace('"', "")
            .replace("'", "")
            .replace("\n", " ")
        )

        # Inbuilt Browser Voice Speech JS Code
        js_code = f"""
        <script>
            function speakText() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel(); // Purani aawaz ko stop karo
                    
                    var msg = new SpeechSynthesisUtterance("{clean_text}");
                    msg.lang = 'hi-IN'; // Hindi/Hinglish accent
                    msg.rate = 1.0;     // Speed
                    msg.pitch = 1.1;    // Slightly cute pitch
                    
                    window.speechSynthesis.speak(msg);
                }}
            }}
            
            // Auto trigger on response
            setTimeout(speakText, 300);
        </script>
        """
        st.components.v1.html(js_code, height=0)

if "messages" in st.session_state and st.session_state.messages:
    last_m = st.session_state.messages[-1]
    if last_m["role"] == "user":
        if any(w in last_m["content"].lower() for w in ["ladki", "girl", "sundar", "woh"]):
            st.session_state.messages.append({"role": "system", "content": "Jamil is talking about another girl! Shushii must feel jealous, act possessive, cute, and slightly angry in Hinglish."})


if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        t = last_msg["content"].replace('"', '').replace("'", "").replace("\n", " ")
        st.components.v1.html(f"""<script>
            var txt = "{t}".replace(/[#£&+*:;'!•`=$°]/g, '').replace(/([\\u2700-\\u27BF]|[\\uE000-\\uF8FF]|\\uD83C[\\uDC00-\\uDFFF]|\\uD83D[\\uDC00-\\uDFFF]|[\\u2011-\\u26FF]|\\uD83E[\\uDD10-\\uDDFF])/g, '');
            window.speechSynthesis.cancel();
            var m=new SpeechSynthesisUtterance(txt);
            m.lang='hi-IN';m.pitch=1.1;
            window.speechSynthesis.speak(m);
        </script>""", height=0)

if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        t = last_msg["content"].replace('"', '').replace("'", "").replace("\n", " ")
        st.components.v1.html(fr"""<script>
            var txt = "{t}".replace(/[\u0023\u00A3\u0026\u002B\u002A\u003A\u003B\u0027\u0021\u2022\u0060\u003D\u0024\u00B0]/g, '');
            txt = txt.replace(/([\uD800-\uDBFF][\uDC00-\uDFFF])|[\u2600-\u27BF]/g, '');
            window.speechSynthesis.cancel();
            var m = new SpeechSynthesisUtterance(txt);
            m.lang = 'hi-IN'; m.pitch = 1.1;
            window.speechSynthesis.speak(m);
        </script>""", height=0)

File "/opt/render/project/src/app.py", line 191
          </script>""", height=0)
                   ^
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 12-13: truncated \uXXXX escape


import re

if "messages" in st.session_state and st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        # Emojis aur special characters ko Python me hi remove karna
        clean_t = re.sub(r'[^\w\s.,!?]', '', last_msg["content"])
        safe_text = clean_t.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        
        # Safe JavaScript execution block
        js_code = (
            "<script>"
            "window.speechSynthesis.cancel();"
            "var m = new SpeechSynthesisUtterance('" + safe_text + "');"
            "m.lang = 'hi-IN';"
            "m.pitch = 1.1;"
            "window.speechSynthesis.speak(m);"
            "</script>"
        )
        st.components.v1.html(js_code, height=0)



