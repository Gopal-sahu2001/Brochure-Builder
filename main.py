import json
from openai import OpenAI
import os
from scraper import fetch_website_contents,fetch_website_links


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
#The variables to be given as prompts to the LLM for Brochure generation

#This is the link system prompt for the input given to fetch all the links in the given website url at '' function

link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

#Here is the brochure system prompt that is neccessary for the creation of the company brochure at the '' function

brochure_system_prompt = """
You are an assistant that analyzes the contents of several company web pages and creates
a professional brochure in Markdown.

Use the information from the provided pages to describe the company.

IMPORTANT:
- Every page in the input contains its corresponding URL.
- Whenever you mention a company page (Website, About, Careers, Products, Blog, LinkedIn, YouTube, etc.), include the ACTUAL URL as a Markdown hyperlink.
- Never output placeholder text such as:
  [Link to company website]
  [Company Website]
  [Link to YouTube]
- Use the URLs exactly as provided in the input.

Example:

Website: [https://company.com](https://company.com)

About: [https://company.com/about](https://company.com/about)

Careers: [https://company.com/careers](https://company.com/careers)

Respond only in Markdown.
"""

#The function that gets us the links from the webpage and this function is a prompt itself in the get_relevant_links function
def get_links_from_url(url):
    user_prompt = f"""
    Here is the list of links on the website {url} -
    Please decide which of these are relevant web links for a brochure about the company, 
    respond with the full https URL in JSON format.
    Do not include Terms of Service, Privacy, email links.

    Links (some might be relative links):

    """
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

#This function filters out the relevant links from the whole collection of found links where, 
#the type of links desired is requested using link_system_prompt,and the actual links are fetched using get_links_from_url(url)function

def get_relevant_links(url):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_from_url(url)}
        ],
        response_format={"type": "json_object"}
    )

    #result = response.choices[0].message.content
    #links = json.loads(result)
    result = response.choices[0].message.content
    print(result)
    
    links = json.loads(result)
    print(links)
    return links

#Now fetch all the relevant links and the page contents then use this as a prompt to create a brochure
def fetch_page_contents_and_links(url):
    contents = fetch_website_contents(url)
    relevant_links = get_relevant_links(url)

    result = f"# Landing Page\n"
    result += f"URL: {url}\n\n"
    result += contents

    result += "\n\n# Relevant Pages\n"

    for link in relevant_links["links"]:
        print(type(link), link)

        if isinstance(link, dict):
            link_type = link.get("type", "Relevant Page")
            link_url = link.get("url", "").strip().strip('"').strip("'")
        else:
            link_type = "Relevant Page"
            link_url = str(link).strip().strip('"').strip("'")

        result += f"\n\n## {link_type}\n"
        result += f"URL: {link_url}\n\n"

        try:
            page_content = fetch_website_contents(link_url)
            result += page_content
        except Exception:
            result += "Content could not be retrieved.\n"

    return result

# Now have all the user prompt finalized and ready for the last prompt of the creating the brochure 
def get_brochure_user_prompt(company_name,url):
    user_prompt = f"""
    You are looking at a company called: {company_name}
    Here are the contents of its landing page and other relevant pages;
    use this information to build a short brochure of the company in markdown without code blocks.\n\n
    """
    user_prompt += fetch_page_contents_and_links(url)
    user_prompt = user_prompt[:5000]

    return user_prompt
