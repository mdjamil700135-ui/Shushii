import streamlit as st
import google.generativeai as genai

# Streamlit UI Configuration
st.set_page_config(page_title="Shushi - AI Assistant", page_icon="💃", layout="centered")

# --- Custom CSS Design ---
st.markdown("""
    <style>
    .main { background-color: #1a1a2e; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #16213e; color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("💃 Shushi - Aapki Smart & Mazakiya AI Friend")

# --- 1. Photo Upload Section ---
st.sidebar.header("Shushi Ki Profile Photo")
uploaded_photo = st.sidebar.file_uploader("Apni pasand ki photo daalein:", type=["jpg", "png", "jpeg"])

if uploaded_photo is not None:
    st.sidebar.image(uploaded_photo, caption="Shushi", use_column_width=True)
else:
    # Default Avatar
    st.sidebar.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=60", caption="Shushi")


if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        pass

if not api_key:
    api_key = st.sidebar.text_input("Apni Gemini API Key dalein:", type="password")


# --- 3. Shushi System Prompt (Personality Setup) ---
SYSTEM_PROMPT = """
Aapka naam 'Shushi' hai. Aap ek intelligent, caring, thodi sarcastic aur mazakiya (witty) girl AI assistant hain.
Rules:
1. Aapki personality ek stylish aur samajhdar ladki ki tarah hai jo Hinglish (Hindi + English) me baat karti hai.
2. User ke mood ko samjho: Agar user sad hai toh empathetic aur caring bano, agar happy hai toh full mazaak aur roast mode me raho.
3. Baaton me thoda mazaak, light teasing aur human-like emotions hone chahiye.
4. Jawab concise, lively aur entertaining rakhein.
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.8-flash", system_instruction=SYSTEM_PROMPT)

    # Chat History Maintain karna
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Previous Chat Display
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # --- 4. Speech Recognition JavaScript (Mobile Wake Word + Voice Input) ---
    st.markdown("""
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN';
        recognition.continuous = true;

        recognition.onresult = function(event) {
            var text = event.results[event.results.length - 1][0].transcript.toLowerCase();
            if (text.includes("shushi") || text.includes("sushi")) {
                alert("Shushi Sun Rahi Hai! Message type ya record karein.");
            }
        };

        function startListening() {
            recognition.start();
        }
        </script>
        <button onclick="startListening()" style="padding:10px; background-color:#e94560; color:white; border:none; border-radius:5px; cursor:pointer;">
            🎤 Turn ON Voice Wake-Word ("Shushi")
        </button>
    """, unsafe_allow_html=True)

    # User Chat Input
    user_input = st.chat_input("Shushi se baat karein...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        # AI Response
        response = st.session_state.chat_session.send_message(user_input)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
            # --- Text to Speech (Voice Output) ---
            # Browser ki aawaz se Shushi bolegi
            tts_script = f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{response.text.replace('"', '')}");
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
            </script>
            """
            st.components.v1.html(tts_script, height=0)

else:
    st.warning("Kripya sidebar me apni Free Gemini API Key dalein taaki Shushi active ho sake.")
