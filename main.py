import json
import subprocess
import ollama
from scraper import fetch_website_contents,fetch_website_links


process = subprocess.Popen(['ollama', 'serve'])
print("The llama server us working in the background")
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
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
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
    response = ollama.chat(
        model = "qwen3:8b",
        messages = [
            {"role" : "system", "content":link_system_prompt},
            {"role" : "user", "content":get_links_from_url(url)}
        ],
        format = "json"
    )
    result = response.message.content
    links = json.loads(result)
    return links

#Now fetch all the relevant links and the page contents then use this as a prompt to create a brochure

def fetch_page_contents_and_links(url):
    contents = fetch_website_contents(url)
    relevant_links = get_relevant_links(url)
    result =  f"## Landing page:\n\n {contents}\n ##Relevant links:\n"
    for link in relevant_links["links"]:
       result += f"\n\n ###{link['type']}\n"
       result += fetch_website_contents(link['url'])
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
