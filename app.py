
import streamlit as st
import time
import json
from datetime import datetime

from pipeline import run_research_pipeline


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #0B1020;
    color: #F8FAFC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #253047;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

.hero {
    text-align: center;
    padding: 35px 10px 30px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(
        90deg, #818CF8, #C084FC, #38BDF8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 17px;
    margin-top: 12px;
}

.agent-card {
    background: #151E31;
    border: 1px solid #29354B;
    padding: 22px 12px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 15px;
}

.agent-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.agent-title {
    color: #E2E8F0;
    font-weight: 700;
    font-size: 15px;
}

.agent-description {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 6px;
}

.result-card {
    background: #151E31;
    border: 1px solid #29354B;
    padding: 22px;
    border-radius: 15px;
    margin: 15px 0;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg, #6366F1, #9333EA
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
}

div.stButton > button[kind="primary"]:hover {
    background: #7C3AED;
    color: white;
}

[data-testid="stMetric"] {
    background: #151E31;
    padding: 16px;
    border: 1px solid #29354B;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}

.stTabs [data-baseweb="tab"] {
    background: #151E31;
    border-radius: 9px;
    padding: 12px 18px;
}

.stTextArea textarea {
    background: #151E31 !important;
    color: #F8FAFC !important;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def format_output(value):
    """Convert chain output to readable text."""

    if isinstance(value, str):
        return value

    if hasattr(value, "content"):
        content = value.content
        if isinstance(content, str):
            return content
        return str(content)

    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    return str(value)


def agent_card(icon, title, description):
    st.markdown(
        f"""
        <div class="agent-card">
            <div class="agent-icon">{icon}</div>
            <div class="agent-title">{title}</div>
            <div class="agent-description">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🧠 ResearchAI")
    st.caption("Intelligent Multi-Agent Platform")

    st.divider()

    st.markdown("### ⚙️ System Overview")

    st.success("● Application Ready")

    st.markdown("""
    **Active AI Agents**

    - 🔎 Search Agent
    - 📖 Reader Agent
    - ✍️ Writer Agent
    - 🛡️ Critic Agent
    """)

    st.divider()

    st.markdown("### 📚 Research History")

    if st.session_state.research_history:

        for item in reversed(
            st.session_state.research_history
        ):
            st.markdown(
                f"📄 {item['topic']}"
            )

    else:
        st.caption("No research completed yet.")

    st.divider()

    st.caption("Powered by LangChain & Streamlit")


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            AI Research Intelligence
        </div>

        <div class="hero-subtitle">
            Transform any topic into comprehensive
            research using four specialized AI agents.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# AGENT WORKFLOW
# --------------------------------------------------

st.markdown("### 🤖 Your AI Research Team")

col1, col2, col3, col4 = st.columns(4)

with col1:
    agent_card(
        "🔎",
        "Search Agent",
        "Finds reliable information"
    )

with col2:
    agent_card(
        "📖",
        "Reader Agent",
        "Extracts source content"
    )

with col3:
    agent_card(
        "✍️",
        "Writer Agent",
        "Generates research reports"
    )

with col4:
    agent_card(
        "🛡️",
        "Critic Agent",
        "Reviews report quality"
    )


# --------------------------------------------------
# RESEARCH INPUT
# --------------------------------------------------

st.markdown("### 🚀 Start New Research")

topic = st.text_area(
    "What would you like to research?",
    placeholder=(
        "Example: Impact of Generative AI "
        "on the future of software engineering..."
    ),
    height=110
)

start_button = st.button(
    "✨ Generate Research Report",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# EXECUTE RESEARCH PIPELINE
# --------------------------------------------------

if start_button:

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:

        st.session_state.research_result = None

        st.markdown("### ⚡ Research Execution")

        progress = st.progress(0)

        status = st.empty()

        start_time = time.time()

        try:

            status.info(
                "🚀 Running Search → Reader → "
                "Writer → Critic pipeline..."
            )

            progress.progress(10)

            # CALL YOUR EXISTING PIPELINE
            result = run_research_pipeline(
                topic.strip()
            )

            progress.progress(100)

            elapsed = round(
                time.time() - start_time,
                2
            )

            st.session_state.research_result = result
            st.session_state.current_topic = topic.strip()

            st.session_state.research_history.append({
                "topic": topic.strip(),
                "date": datetime.now().strftime(
                    "%d %b %Y, %I:%M %p"
                ),
                "duration": elapsed
            })

            status.success(
                "✅ All four agents completed successfully!"
            )

            st.success(
                f"Research completed in {elapsed} seconds."
            )

        except Exception as e:

            progress.empty()

            status.error(
                "❌ Research pipeline failed."
            )

            st.error(str(e))


# --------------------------------------------------
# RESEARCH RESULTS
# --------------------------------------------------

if st.session_state.research_result is not None:

    result = st.session_state.research_result

    report = format_output(
        result.get("report", "")
    )

    search_results = format_output(
        result.get("search_results", "")
    )

    scraped_content = format_output(
        result.get("scraped_content", "")
    )

    feedback = format_output(
        result.get("feedback", "")
    )

    st.divider()

    st.markdown("## 📊 Research Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "AI Agents",
            "4"
        )

    with metric2:
        st.metric(
            "Report Words",
            len(report.split())
        )

    with metric3:
        st.metric(
            "Research Status",
            "Completed"
        )

    with metric4:
        st.metric(
            "Pipeline Steps",
            "4 / 4"
        )

    st.markdown(
        f"### 📌 {st.session_state.current_topic}"
    )

    # ----------------------------------------------
    # RESULT TABS
    # ----------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Final Report",
        "🔎 Search Results",
        "📖 Scraped Content",
        "🛡️ Critic Feedback"
    ])

    with tab1:

        st.markdown("### ✍️ AI Generated Research Report")

        st.markdown(report)

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    with tab2:

        st.markdown("### 🔎 Search Agent Output")

        st.markdown(search_results)

    with tab3:

        st.markdown("### 📖 Reader Agent Output")

        st.markdown(scraped_content)

    with tab4:

        st.markdown("### 🛡️ Critic Agent Review")

        st.markdown(feedback)

    # ----------------------------------------------
    # EXPORT COMPLETE RESULTS
    # ----------------------------------------------

    st.divider()

    st.markdown("### 📦 Export Complete Research")

    export_data = {
        "topic": st.session_state.current_topic,
        "search_results": search_results,
        "scraped_content": scraped_content,
        "report": report,
        "feedback": feedback
    }

    st.download_button(
        label="⬇️ Download Complete Research (JSON)",
        data=json.dumps(
            export_data,
            indent=4,
            ensure_ascii=False
        ),
        file_name="complete_research.json",
        mime="application/json",
        use_container_width=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        padding:15px;
        font-size:13px;
    ">
        ResearchAI • Multi-Agent Research Platform
        <br>
        Built with Python, LangChain and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
