# Brochure-Builder
Generates company brochure if given a company name and url.

You can use the link below and deploy and play with it on render:
https://brochure-builder-c0fz.onrender.com/

# Project Workflow

```text
                         DEVELOPMENT PHASE
                         =================

        ┌──────────────────────────────────────────┐
        │             Python Source Code           │
        │------------------------------------------│
        │ app.py                                   │
        │ main.py                                  │
        │ scraper.py                               │
        │ requirements.txt                         │
        │ README.md                                │
        └──────────────────────┬───────────────────┘
                               │
                               │ Git Commit
                               ▼
                    ┌───────────────────────┐
                    │       GitHub          │
                    │ Source Code Repository│
                    └───────────┬───────────┘
                                │
                                │ Auto Deployment
                                ▼
                     ┌────────────────────────┐
                     │        Render          │
                     │ Python Web Service     │
                     └───────────┬────────────┘
                                 │
                                 │
                     Installs Dependencies
                                 │
                                 ▼
                    requirements.txt
                                 │
                                 ▼
                       Launches Streamlit
                                 │
                                 ▼
                         app.py starts
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     Streamlit UI       │
                    └───────────┬────────────┘
                                │
                                │ User enters
                                │ Company Name
                                │ Company URL
                                ▼
                  get_brochure_user_prompt()
                                │
                                ▼
             fetch_page_contents_and_links()
                                │
             ┌──────────────────┴───────────────────┐
             ▼                                      ▼
 fetch_website_contents()                 get_relevant_links()
             │                                      │
             │                                      │
             ▼                                      ▼
 Landing Page Text                    Groq API (Llama 3.1)
                                              │
                                              ▼
                                 Select Relevant Website Links
                                              │
                                              ▼
                          JSON containing About, Careers,
                          Products, Blog, Social Media, etc.
                                              │
                                              ▼
                     Scrape all selected webpages
                                              │
                                              ▼
                      Combine all webpage contents
                                              │
                                              ▼
                     Create Final Prompt for LLM
                                              │
                                              ▼
                               Groq API
                       (Llama 3.1 8B Instant)
                                              │
                                     Streaming Response
                                              │
                                              ▼
                             Streamlit Frontend
                                              │
                                              ▼
                           Display AI Brochure
                                              │
                                              ▼
                       Download Markdown Brochure
```

## Deployment Flow

```
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Render Web Service
    │
    ▼
Installs Python Dependencies
    │
    ▼
Runs Streamlit Application
    │
    ▼
Public URL
```

## AI Pipeline

```
Website URL
     │
     ▼
Landing Page Scraper
     │
     ▼
Extract Hyperlinks
     │
     ▼
Groq LLM selects relevant links
     │
     ▼
Scrape selected pages
     │
     ▼
Build final prompt
     │
     ▼
Groq Llama 3.1 8B Instant
     │
     ▼
Generate brochure
     │
     ▼
Stream response to user
```

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM Provider:** Groq
- **Model:** Llama 3.1 8B Instant
- **Web Scraping:** Requests + BeautifulSoup
- **HTML Parsing:** lxml
- **Deployment:** Render
- **Version Control:** Git & GitHub
- **Output:** Markdown brochure
