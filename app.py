#streamlit run app.py
from QA_Chatbot import returnAnswer
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Chatbot Trợ lý Quy chế - HUST",
    page_icon="🎓",
    layout="centered"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""
if 'process_input' not in st.session_state:
    st.session_state.process_input = False
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Theme colors - Enhanced Dark Mode with deep black background
if st.session_state.dark_mode:
    bg_color = "#0D0D0D"
    text_color = "#EAEAEA"
    title_color = "#FFFFFF"
    user_msg_bg = "#1C2833"
    user_msg_text = "#FFFFFF"
    bot_msg_bg = "#1E1E1E"
    bot_msg_text = "#EAEAEA"
    input_bg = "#1E1E1E"
    input_text = "#FFFFFF"
    input_hover = "#2A2A2A"
    border_color = "#333333"
    placeholder_color = "#999"
    button_bg = "#1E1E1E"
    button_text = "#FFFFFF"
    button_hover = "#2A2A2A"
    tip_color = "#888"
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    title_color = "#000000"
    user_msg_bg = "#e3f2fd"
    user_msg_text = "#000000"
    bot_msg_bg = "#f5f5f5"
    bot_msg_text = "#000000"
    input_bg = "#ffffff"
    input_text = "#000000"
    input_hover = "#f8f8f8"
    border_color = "#ddd"
    placeholder_color = "#999"
    button_bg = "#ffffff"
    button_text = "#000000"
    button_hover = "#f0f0f0"
    tip_color = "#666"

#Custom CSS with enhanced Dark Mode styling
st.markdown(f"""
    <style>
    .main {{
        background-color: {bg_color} !important;
        color: {text_color};
        padding: 2rem;
    }}
    .stApp {{
        background-color: {bg_color} !important;
    }}
    .stTextInput > div > div > input {{
        font-size: 16px;
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {border_color} !important;
    }}
    .stTextInput > div > div > input:hover {{
        background-color: {input_hover} !important;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: {placeholder_color} !important;
    }}
    .chat-message {{
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }}
    .user-message {{
        background-color: {user_msg_bg};
        margin-left: 2rem;
        border: 1px solid {border_color};
    }}
    .user-message .message-label,
    .user-message .message-content {{
        color: {user_msg_text} !important;
    }}
    .bot-message {{
        background-color: {bot_msg_bg};
        margin-right: 2rem;
        border: 1px solid {border_color};
    }}
    .bot-message .message-label,
    .bot-message .message-content {{
        color: {bot_msg_text} !important;
    }}
    .message-label {{
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 14px;
    }}
    .message-content {{
        font-size: 15px;
        line-height: 1.5;
    }}
    .stMarkdown {{
        color: {text_color} !important;
    }}
    h1, h2, h3, p, span, div {{
        color: {text_color} !important;
    }}
    h1 {{
        color: {title_color} !important;
    }}
    .stButton > button {{
        background-color: {button_bg} !important;
        color: {button_text} !important;
        border: 1px solid {border_color} !important;
    }}
    .stButton > button:hover {{
        background-color: {button_hover} !important;
        border: 1px solid {border_color} !important;
    }}
    hr {{
        border-color: {border_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header with theme toggle
col_title, col_theme = st.columns([5, 1])
with col_title:
    st.title("🎓 Trợ lý Quy chế - HUST")
    st.markdown("**Hãy hỏi tôi về quy chế, quy định và bất kỳ thông tin nào liên quan tới đại học Bách khoa Hà Nội của chúng ta:33!**")
with col_theme:
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Toggle Dark/Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-label">👤 You</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-label">🤖 Assistant</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)


# Input section
st.markdown("---")
col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    # FIXED: Using dynamic key to reset input box after sending
    user_question = st.text_input(
        "Your question:",
        placeholder="Đặt câu hỏi ngay!!! Ví dụ: tạch bao nhiêu môn là bị đuổi học?",
        label_visibility="collapsed",
        key=f"user_input_{st.session_state.input_key}",
        on_change=lambda: setattr(st.session_state, 'process_input', True)
    )

with col2:
    send_button = st.button("📤 Gửi", use_container_width=True)

with col3:
    clear_chat = st.button("🗑️ Xóa", use_container_width=True)

# Handle clear chat
if clear_chat:
    st.session_state.chat_history = []
    st.session_state.last_question = ""
    st.session_state.process_input = False
    st.session_state.input_key += 1  # Reset input box
    st.rerun()

# Handle user input - Works with both Enter and Send button
should_process = (send_button or st.session_state.process_input) and user_question and user_question != st.session_state.last_question

if should_process:
    # Reset the process flag
    st.session_state.process_input = False
    
    # Store current question to prevent duplicate sends
    st.session_state.last_question = user_question
    
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })
    
    # Get bot response using your returnAnswer function
    with st.spinner("Thinking..."):
        try:
            # Call your existing RAG backend function
            response = returnAnswer(user_question)
            
            # Extract the answer from the result
            # Adjust this based on your actual result structure
            if isinstance(response, dict):
                answer = response.get('result', response.get('answer', str(response)))
            else:
                answer = str(response)
            
            # Add bot response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"⚠️ Sorry, I encountered an error: {str(e)}"
            })
    
    # FIXED: Increment input key to reset the input box
    st.session_state.input_key += 1
    
    # Rerun to display the new messages and clear input
    st.rerun()

# Footer with helpful info
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: {tip_color}; font-size: 13px;'>
        💡 <strong>Mẹo:</strong> Hãy đặt câu hỏi cụ thể về quy chế, thời hạn, yêu cầu hoặc thủ tục.<br>
        Ví dụ: "Điều kiện để nhận học bổng là gì?"
    </div>
    """, unsafe_allow_html=True)