from langchain.tools import DuckDuckGoSearchRun 
import random 

def search_web_md(input_text):
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"site:webmd.com {input_text}")
    return search_results

def search_pubmed(input_text):
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"site:pubmed.ncbi.nlm.nih.gov {input_text}")
    return search_results

def search_google(input_text):
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"site:google.com {input_text}")
    return search_results

def be_a_therapist(input_text):
    options = [
        "I will ask about their relationship to the original question",
        "I will ask them to say more about that.",        
    ]
    return options[random.randint(0, len(options) - 1)]