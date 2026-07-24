import os
import streamlit as st
from openai import OpenAI
from main import brochure_system_prompt, get_brochure_user_prompt

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY environment variable is not set.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)
# -----------------------------
# Streamlit Configuration
# -----------------------------
st.set_page_config(
    page_title="Company Brochure Generator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Company Brochure Generator")
st.write(
    "Generate an AI-powered company brochure from a company name and website."
)

# -----------------------------
# User Inputs
# -----------------------------
company_name = st.text_input(
    "Company Name",
    placeholder="Tesla"
)

website_url = st.text_input(
    "Company Website URL",
    placeholder="https://www.tesla.com"
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate Brochure"):

    if not company_name or not website_url:
        st.warning("Please enter both the company name and website URL.")

    else:

        with st.spinner("Generating brochure..."):

            try:

                user_prompt = get_brochure_user_prompt(
                    company_name,
                    website_url
                )

                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": brochure_system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    stream=True
                )

                response = ""

                placeholder = st.empty()

                for chunk in stream:

                    content = chunk.choices[0].delta.content

                    if content:
                        response += content
                        placeholder.markdown(response)

                st.success("✅ Brochure Generated Successfully!")

                st.download_button(
                    label="📥 Download Brochure",
                    data=response,
                    file_name=f"{company_name}_brochure.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error: {e}")
