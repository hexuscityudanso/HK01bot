import requests
import re
from bs4 import BeautifulSoup

def extract_content(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract content from <meta name="title">
    title_meta = soup.find("meta", attrs={"name": "title"})
    title = strip_content(str(title_meta))

    # Extract content from <meta name="description">
    #description_meta = soup.find("meta", attrs={"name": "description"})
    #desc = strip_content(str(description_meta))

    #content = []
    # Extract content from <p class="-ml-3 md:ml-0">
    #paragraphs = soup.find_all("p", class_="-ml-3 md:ml-0")
    #for paragraph in paragraphs:
        #content.append(remove_bracket_content(str(paragraph)))

    #paragraphs = soup.find_all("p", class_="break-words")
    #for paragraph in paragraphs:
        #content.append(remove_bracket_content(str(paragraph)))

    return title

def strip_content(string):
    first_quote_index = string.find('"')
    if first_quote_index == -1:
        return None

    second_quote_index = string.find('"', first_quote_index+1)
    if second_quote_index == -1:
        return None

    content = string[first_quote_index+1:second_quote_index]
    return content

def remove_bracket_content(string):
    pattern = r'<[^>]*>'  # Regular expression pattern to match content within brackets
    result = re.sub(pattern, '', string)
    return result

def extract(url):
    #url = "https://www.hk01.com/%E7%A4%BE%E6%9C%83%E6%96%B0%E8%81%9E/901052/19%E6%AD%B2%E6%95%91%E7%94%9F%E5%93%A1%E6%B6%89%E9%9D%9E%E7%A6%AE%E5%85%AB%E6%97%AC%E6%99%A8%E9%81%8B%E5%A9%A6-%E4%BA%8B%E4%B8%BB%E5%81%9A%E9%81%8B%E5%8B%95%E9%81%AD%E5%BE%9E%E5%BE%8C%E6%96%BD%E6%B7%AB-%E9%A9%9A%E5%88%B0%E9%9C%87%E9%9C%87%E8%B2%A2"
    return extract_content(url)
