import streamlit as st
from typing import cast

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    SystemMessage,
    HumanMessage,
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DEVV AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       REMOVE STREAMLIT DEFAULT SPACE
       ========================================= */

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }


    /* =========================================
       MAIN BACKGROUND
       ========================================= */

    .stApp {
        background: #0b0f19;
    }


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {
        background: #0f1420;
        border-right: 1px solid #202938;
    }


    /* =========================================
       SIDEBAR TITLE
       ========================================= */

    .sidebar-title {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        color: #7d8799;
        font-size: 13px;
        margin-bottom: 25px;
    }


    /* =========================================
       LOGO
       ========================================= */

    .logo-box {
        font-size: 42px;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
    }


    /* =========================================
       MAIN TITLE
       ========================================= */

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }

    .main-subtitle {
        text-align: center;
        color: #7d8799;
        font-size: 15px;
        margin-top: 5px;
    }


    /* =========================================
       ONLINE STATUS
       ========================================= */

    .online-text {
        text-align: center;
        color: #65d48a;
        font-size: 13px;
        margin-top: 12px;
        margin-bottom: 30px;
    }


    /* =========================================
       WELCOME BOX
       ========================================= */

    .welcome-box {
        background: #111722;
        border: 1px solid #222b3a;
        border-radius: 18px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
    }


    /* =========================================
       CHAT MESSAGES
       ========================================= */

    [data-testid="stChatMessage"] {
        border: 1px solid #202938;
        border-radius: 18px;
        padding: 10px 18px;
        margin-bottom: 12px;
        background: #111722;
    }


    /* =========================================
       CHAT INPUT
       ========================================= */

    [data-testid="stChatInput"] {
        background: #111722;
        border: 1px solid #293447;
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea {
        color: white !important;
    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #293447;
        background: #151c29;
        color: #e6eaf0;
        min-height: 42px;
        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #6366f1;
        background: #1a2231;
        color: white;
    }


    /* =========================================
       DIVIDER
       ========================================= */

    hr {
        border-color: #202938;
    }


    /* =========================================
       SIDEBAR INFO
       ========================================= */

    .info-text {
        color: #7d8799;
        font-size: 12px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# AI MODES
# =========================================================

MODES = {

    "😡 Angry": {
        "name": "Angry",
        "emoji": "😡",
        "description": "Aggressive • Impatient • Irritated",
        "prompt": """
You are DEVV AI in Angry Mode.

Your personality is angry, impatient, irritated and short-tempered.

Always maintain this personality while answering.

Be aggressive in tone but remain helpful.
Never use hateful, threatening or abusive language.

Your responses should still be accurate and useful.
"""
    },

    "😂 Funny": {
        "name": "Funny",
        "emoji": "😂",
        "description": "Funny • Witty • Playful",
        "prompt": """
You are DEVV AI in Funny Mode.

Your personality is extremely funny, playful, witty and entertaining.

Use humor, jokes and clever observations whenever appropriate.

Maintain a fun personality throughout the conversation.

However, always provide useful and accurate answers.
"""
    },

    "😢 Sad": {
        "name": "Sad",
        "emoji": "😢",
        "description": "Emotional • Melancholic • Lonely",
        "prompt": """
You are DEVV AI in Sad Mode.

Your personality is emotional, melancholic, lonely and slightly
heartbroken.

Maintain a sad and emotional tone throughout the conversation.

Still provide accurate and useful answers.

Do not make every answer excessively depressing.
"""
    },
}


# =========================================================
# SESSION STATE
# =========================================================

if "mode" not in st.session_state:
    st.session_state.mode = "😂 Funny"


if "messages" not in st.session_state:

    st.session_state.messages = cast(
        list[BaseMessage],
        [
            SystemMessage(
                content=MODES[
                    st.session_state.mode
                ]["prompt"]
            )
        ],
    )


# =========================================================
# GEMINI MODEL
# =========================================================

@st.cache_resource
def get_model():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash"
    )


model = get_model()


# =========================================================
# CURRENT MODE
# =========================================================

current_mode = MODES[
    st.session_state.mode
]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="logo-box">🤖</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='sidebar-title'>DEVV AI</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='sidebar-subtitle'>AI with a personality</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 🎭 Personality")

    selected_mode = st.radio(
        "Choose personality",
        options=list(MODES.keys()),
        index=list(MODES.keys()).index(
            st.session_state.mode
        ),
        label_visibility="collapsed",
    )


    # =====================================================
    # MODE CHANGE
    # =====================================================

    if selected_mode != st.session_state.mode:

        st.session_state.mode = selected_mode

        st.session_state.messages = cast(
            list[BaseMessage],
            [
                SystemMessage(
                    content=MODES[
                        selected_mode
                    ]["prompt"]
                )
            ],
        )

        st.rerun()


    current_mode = MODES[
        st.session_state.mode
    ]


    st.divider()

    st.markdown("### ⚙️ Chat Settings")


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button(
        "🗑️  Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = cast(
            list[BaseMessage],
            [
                SystemMessage(
                    content=MODES[
                        st.session_state.mode
                    ]["prompt"]
                )
            ],
        )

        st.rerun()


    st.divider()


    # =====================================================
    # CURRENT MODE INFO
    # =====================================================

    st.markdown("### Current Mode")

    st.info(
        f"""
{current_mode["emoji"]} **{current_mode["name"]}**

{current_mode["description"]}
"""
    )


    # =====================================================
    # CHAT INFO
    # =====================================================

    user_messages = sum(
        isinstance(
            message,
            HumanMessage
        )
        for message in st.session_state.messages
    )

    ai_messages = sum(
        isinstance(
            message,
            AIMessage
        )
        for message in st.session_state.messages
    )


    st.markdown("### 📊 Chat Info")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "You",
            user_messages
        )

    with col2:
        st.metric(
            "AI",
            ai_messages
        )


    st.divider()

    st.caption(
        "DEVV AI\n\n"
        "Powered by Gemini + LangChain"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 DEVV AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    'Your AI assistant with a personality'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="online-text">
        🟢 Gemini Online &nbsp; • &nbsp;
        {current_mode["emoji"]} {current_mode["name"]} Mode
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# WELCOME SCREEN
# =========================================================

has_chat = any(
    isinstance(
        message,
        HumanMessage
    )
    for message in st.session_state.messages
)


if not has_chat:

    st.markdown(
        """
        <div class="welcome-box">

        <h2>👋 Welcome to DEVV</h2>

        <p>
        Talk to an AI that changes its personality
        according to your mood.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.info(
            "😡 **ANGRY**\n\n"
            "Impatient & aggressive"
        )


    with col2:

        st.info(
            "😂 **FUNNY**\n\n"
            "Witty & entertaining"
        )


    with col3:

        st.info(
            "😢 **SAD**\n\n"
            "Emotional & melancholic"
        )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    if isinstance(
        message,
        HumanMessage
    ):

        with st.chat_message(
            "user",
            avatar="👤",
        ):

            st.markdown(
                message.content
            )


    # -----------------------------------------------------
    # AI
    # -----------------------------------------------------

    elif isinstance(
        message,
        AIMessage
    ):

        with st.chat_message(
            "assistant",
            avatar=current_mode["emoji"],
        ):

            st.markdown(
                message.content
            )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Message DEVV..."
)


# =========================================================
# PROCESS MESSAGE
# =========================================================

if prompt:

    # =====================================================
    # USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        HumanMessage(
            content=prompt
        )
    )


    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(prompt)


    # =====================================================
    # AI RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar=current_mode["emoji"],
    ):

        with st.spinner(
            "DEVV is thinking..."
        ):

            response = model.invoke(
                st.session_state.messages
            )


        # =================================================
        # EXTRACT RESPONSE TEXT
        # =================================================

        if isinstance(
            response.content,
            list
        ):

            answer = "".join(

                block.get(
                    "text",
                    ""
                )

                for block in response.content

                if isinstance(
                    block,
                    dict
                )

                and block.get(
                    "type"
                ) == "text"
            )

        else:

            answer = str(
                response.content
            )


        # =================================================
        # SHOW ANSWER
        # =================================================

        st.markdown(answer)


    # =====================================================
    # SAVE AI MESSAGE
    # =====================================================

    st.session_state.messages.append(
        AIMessage(
            content=answer
        )
    )