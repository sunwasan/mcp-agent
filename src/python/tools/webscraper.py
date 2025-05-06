from duckduckgo_search import DDGS
from python.tools.craw4ai import *
from nest_asyncio import apply
apply()
import asyncio
import asyncio
import nest_asyncio
import platform

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    nest_asyncio.apply()
    
import requests
from bs4 import BeautifulSoup

def web_grounding(query:str):
    """
    Perform a web search using DuckDuckGo and return the top results.
    
    Args:
        query (str): The search query.
        num_results (int): The number of search results to return.
        
    Returns:
        list: A list of dictionaries containing the title and URL of each result.
    """
    results = DDGS().text(query, 10)
    
    return results