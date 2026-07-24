# Brochure-Builder
Generates company brochure if given a company name and url.

You can use the link below and deploy and play with it on render:
https://brochure-builder-c0fz.onrender.com/

                           +----------------------+
                           |      User Input      |
                           |----------------------|
                           | Company Name         |
                           | Company Website URL  |
                           +----------+-----------+
                                      |
                                      |
                                      v
                        +----------------------------+
                        |     Streamlit Frontend     |
                        | (Collects user inputs)     |
                        +-------------+--------------+
                                      |
                                      |
                                      v
                    +------------------------------------+
                    | get_brochure_user_prompt()         |
                    +----------------+-------------------+
                                     |
                                     |
                                     v
                +----------------------------------------------+
                | fetch_page_contents_and_links()              |
                +----------------------+-----------------------+
                                       |
             +-------------------------+-------------------------+
             |                                                   |
             |                                                   |
             v                                                   v
+-----------------------------+                   +------------------------------+
| fetch_website_contents()    |                   | get_relevant_links()         |
|                             |                   |                              |
| Scrapes Landing Page        |                   | Uses Groq LLM               |
|                             |                   | to identify important links |
+--------------+--------------+                   +--------------+---------------+
               |                                                |
               |                                                |
               |                                    fetch_website_links()
               |                                                |
               |                                                |
               +-------------------------+----------------------+
                                         |
                                         v
                      +-------------------------------------+
                      | Relevant Links JSON                 |
                      |-------------------------------------|
                      | About                              |
                      | Careers                            |
                      | Products                           |
                      | Blog                               |
                      | Social Media                       |
                      +----------------+--------------------+
                                       |
                                       |
                                       v
                     +---------------------------------------+
                     | Scrape every relevant webpage         |
                     | using fetch_website_contents()        |
                     +----------------+----------------------+
                                      |
                                      |
                                      v
                    +---------------------------------------+
                    | Combine all webpage contents into one |
                    | structured prompt                     |
                    +----------------+----------------------+
                                     |
                                     |
                                     v
                     +--------------------------------------+
                     |     Groq Llama 3.1 8B Instant        |
                     |--------------------------------------|
                     | Generates brochure in Markdown       |
                     | Streams response token-by-token      |
                     +----------------+---------------------+
                                      |
                                      |
                                      v
                      +--------------------------------+
                      | Streamlit Live Interface       |
                      |--------------------------------|
                      | Display streamed brochure      |
                      | Download as Markdown           |
                      +--------------------------------+
