# Deployed Resume Summarizer (GenAI)

dBug Labs ML/GenAI Recruitment Task — 2nd Year, Task 2

## Objective

Build and deploy a tool that takes resume text as input and generates a concise
2-3 line summary highlighting key skills and experience, using a pretrained
GenAI model via API.

## Tech Stack

- **Language:** Python 3.9+
- **UI / Deployment:** Streamlit (Streamlit Community Cloud)
- **AI Model:** Hugging Face Inference API — `facebook/bart-large-cnn`
  (free tier, no cost)
- **PDF parsing:** pypdf
- **HTTP requests:** requests

## Implementation Details

1. The user either uploads a resume (PDF/TXT) or pastes resume text directly
   into the app.
2. If a PDF is uploaded, `pypdf` extracts the raw text from it.
3. The extracted/pasted text is sent to the Hugging Face Inference API
   (`facebook/bart-large-cnn`, a pretrained summarization transformer) with
   a max output length capped at ~80 tokens to keep the summary to 2-3 lines.
4. The API's summary is displayed back to the user in the Streamlit UI.
5. Input text is trimmed to the first 3000 characters to stay within the
   model's context limits.

## Setup & Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd resume-summarizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free Hugging Face API token
#    https://huggingface.co/settings/tokens -> "New token" (read access is enough)

# 4. Run the app
streamlit run app.py
```

Paste your Hugging Face token into the sidebar field when the app opens
in your browser.

## Deploying (Streamlit Community Cloud — free)

1. Push this repo to GitHub (public).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click "New app", select this repo and `app.py` as the entry point.
4. Deploy. Once live, enter your Hugging Face token in the sidebar to use it
   (or add it as a Streamlit "Secret" named `HF_TOKEN` for a fixed deployment).

## Testing

Tested on 3 sample resumes (included in `sample_resumes/`):
- `resume1.txt` — Software Engineer
- `resume2.txt` — Data Analyst
- `resume3.txt` — Machine Learning Enthusiast

Each produced a coherent 2-3 line summary capturing the candidate's role,
key skills, and experience highlights.

## Screenshots

_Add screenshots of the running app here (app UI, an example summary output,
and the deployed Streamlit Cloud URL) before submitting._

`screenshots/app-home.png`
`screenshots/summary-example.png`

## Notes

- The Hugging Face free Inference API can occasionally return a "model
  loading" response on the first request (cold start) — simply retry after
  ~20 seconds.
- For production-grade summaries tailored specifically to resumes
  (e.g., explicitly extracting skills/experience rather than general
  summarization), this could be swapped for an instruction-following model
  (e.g., `google/flan-t5-large`) with a custom prompt.
