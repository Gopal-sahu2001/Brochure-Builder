import streamlit as st
import ollama
from main import brochure_system_prompt, get_brochure_user_prompt

st.set_page_config(
    page_title="Company Brochure Generator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Company Brochure Generator")
st.write("Generate an AI-powered company brochure from a company name and website.")

company_name = st.text_input("Company Name")
website_url = st.text_input("Company Website URL")

if st.button("Generate Brochure"):

    if not company_name or not website_url:
        st.warning("Please enter both the company name and website URL.")
    else:

        with st.spinner("Generating brochure..."):

            try:
                user_prompt = get_brochure_user_prompt(company_name, website_url)

                stream = ollama.chat(
                    model="qwen3:8b",
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
                output = st.empty()

                for chunk in stream:
                    response += chunk["message"]["content"]
                    output.markdown(response)

            except Exception as e:
                st.error(f"Error: {e}")
