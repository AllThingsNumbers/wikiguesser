# Wiki Guesser Game, for Streamlit

# Streamlit adaptation of Wikipedia Guesser

import streamlit as st
import requests as req
import random
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/api/rest_v1/'
headers = {'User-Agent': 'komputerowiec21w@o2.pl', 'Accept': 'application/json'}

# Function to fetch 4 random article titles
def get_4_titles():
    titles = []
    titles_url = f'{url}page/random/title'
    for i in range(4):
        response = req.get(titles_url, headers=headers)
        items = response.json().get('items', [])
        titles.append(items[0]['title'])
    return titles

# Function to get a random sentence from a Wiki article
def get_rand_sentence(title):
    title = title.replace(' ', '_')
    article_url = f'https://en.wikipedia.org/wiki/{title}'
    
    response = req.get(article_url)
    if response.status_code != 200:
        return None, None
    
    article_content = BeautifulSoup(response.text, 'html.parser')
    all_pars = article_content.find_all('p')
    
    sentences = []
    for par in all_pars:
        par_text = par.get_text(separator=' ', strip=True)
        sentences.extend(par_text.split('. '))
    
    title_words = set(title.lower().split())
    valid_sentences = [s for s in sentences if not any(word in s.lower() for word in title_words)]
    
    if len(valid_sentences) < 2:
        return None, None
    
    return valid_sentences[0], random.choice(valid_sentences[1:])

# Streamlit UI
st.title("Wikipedia Guesser Game")
if st.button('Start Game'):
    drawn_titles = get_4_titles()
    correct_answer = random.randint(0, 3)
    chosen_title = drawn_titles[correct_answer]
    first_sent, rand_sent = get_rand_sentence(chosen_title)
    
    if not first_sent:
        st.error("Could not retrieve a valid sentence. Try again.")
    else:
        st.subheader("Which article is this sentence from?")
        st.write(rand_sent)
        
        answer = st.radio("Choose an article:", drawn_titles)
        if st.button('Submit Answer'):
            if answer == chosen_title:
                st.success(f"Correct! The article was: {chosen_title}")
            else:
                st.error(f"Wrong! The correct article was: {chosen_title}")
            st.info(f"First sentence of the article: {first_sent}")
        
    if st.button('Play Again'):
        st.experimental_rerun()
