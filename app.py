import streamlit as st
import requests
from pypdf import PdfReader
import io

st.set_page_config(page_title="Resume Summarizer", page_icon="📄", layout="centered")

st.title("📄 Resume Summarizer (GenAI)")
st.write(
    "Upload a resume (PDF or TXT) or paste the text below, and get a "
    "2-3 line AI-generated summary highlighting key skills and experience."
)

# --- Sidebar: API key input ---
st.sidebar.header("Settings")
hf_token = st.sidebar.text_input(
    "Hugging Face API Token",
    type="password",
    help="Get a free token at https://huggingface.co/settings/tokens",
)
st.sidebar.markdown(
    "This app uses the free Hugging Face Inference API "
    "(model: `facebook/bart-large-cnn`) to generate summaries."
)

HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract raw text from an uploaded PDF file."""
    reader = PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def summarize_resume(resume_text: str, token: str) -> str:
    """Call the Hugging Face Inference API to summarize resume text."""
    headers = {"Authorization": f"Bearer {token}"}

    # Keep input within a reasonable length for the model
    trimmed_text = resume_text[:3000]

    payload = {
        "inputs": trimmed_text,
        "parameters": {
            "max_length": 80,
            "min_length": 20,
            "do_sample": False,
        },
    }

    response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"API Error ({response.status_code}): {response.text}")

    result = response.json()

    if isinstance(result, list) and "summary_text" in result[0]:
        return result[0]["summary_text"]
    elif isinstance(result, dict) and "error" in result:
        raise RuntimeError(result["error"])
    else:
        raise RuntimeError(f"Unexpected response format: {result}")


# --- Main input area ---
input_method = st.radio("Choose input method:", ["Upload file", "Paste text"])

resume_text = ""

if input_method == "Upload file":
    uploaded_file = st.file_uploader("Upload resume (PDF or TXT)", type=["pdf", "txt"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
        if resume_text:
            with st.expander("Preview extracted text"):
                st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
else:
    resume_text = st.text_area("Paste resume text here:", height=250)

# --- Summarize button ---
if st.button("Summarize Resume", type="primary"):
    if not hf_token:
        st.error("Please enter your Hugging Face API token in the sidebar.")
    elif not resume_text.strip():
        st.error("Please upload a file or paste resume text first.")
    else:
        with st.spinner("Generating summary..."):
            try:
                summary = summarize_resume(resume_text, hf_token)
                st.success("Summary generated!")
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()
st.caption(
    "Built for dBug Labs ML/GenAI recruitment task — "
    "Task 2 (2nd Year): Deployed Resume Summarizer."
)
