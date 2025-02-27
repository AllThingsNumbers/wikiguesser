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
    normalised_title = title
    title = title.replace(' ', '_')
    article_url = f'https://en.wikipedia.org/wiki/{title}'
    
    response = req.get(article_url)
    if response.status_code != 200:
        st.write(f'Failed to fetch {article_url}, status code: {response.status_code}')
        return None, None
    
    article_content = BeautifulSoup(response.text, 'html.parser')
    all_pars = article_content.find_all('p')
    
    sentences = []
    for par in all_pars:
        par_text = par.get_text(separator=' ', strip=True)
        sentences.extend(par_text.split('. '))
    
    title_words = set(normalised_title.lower().split())
    valid_sentences = [s for s in sentences if not any(word in s.lower() for word in title_words)]
    
    #if len(valid_sentences) < 2:
    #    return None, None
    
    return valid_sentences[0], random.choice(valid_sentences[1:])

# Streamlit UI
st.title("Wikipedia Guesser Game")


# Session state setup
if "game_state" not in st.session_state:
    st.session_state.game_state = "not_started"
if "drawn_titles" not in st.session_state:
    st.session_state.drawn_titles = []
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "rand_sent" not in st.session_state:
    st.session_state.rand_sent = ""
if "first_sent" not in st.session_state:
    st.session_state.first_sent = ""
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

# Start the game when button is clicked
if st.button('(Re)Start Game'):
    st.write('Welcome to Wiki Guesser.\nGuess the correct Wikipedia article based on the provided sample.\n\nPlease wait, as the game is being prepared.')
    st.session_state.game_state = "playing"

    while True:  # Keep trying until a valid sentence is found
        st.session_state.drawn_titles = get_4_titles()
        st.session_state.correct_answer = random.randint(0, 3)
        chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]

        first_sent, rand_sent = get_rand_sentence(chosen_title)

        if first_sent and rand_sent:
            st.session_state.first_sent = first_sent
            st.session_state.rand_sent = rand_sent
            break  # Exit loop when valid sentences are found

    # st.session_state.drawn_titles = get_4_titles()
    # st.session_state.correct_answer = random.randint(0, 3)
    # chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]
    
    # first_sent, rand_sent = get_rand_sentence(chosen_title)
    
    # if not first_sent or not rand_sent:
    #     st.error("Could not retrieve a valid sentence. Try again.")
    #     st.session_state.game_state = "not_started"
    # else:
    #     st.session_state.first_sent = first_sent
    #     st.session_state.rand_sent = rand_sent

# Game UI
if st.session_state.game_state == "playing":
    st.subheader("Which article is this sentence from?")
    st.write(st.session_state.rand_sent)
    
    # Radio button (stores answer in session state)
    st.session_state.selected_answer = st.radio(
        "Choose an article:",
        [title.replace('_', ' ') for title in st.session_state.drawn_titles],
        #st.session_state.drawn_titles,
        index=None,
        #key="selected_answer"
    )

    # Submit answer button
    if st.button('Submit Answer'):
        if st.session_state.selected_answer:  # Ensure an answer is selected
            chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]
            if st.session_state.selected_answer.replace(' ', '_') == chosen_title:
                st.success(f"Correct! The article was: {chosen_title.replace('_', ' ')}")
            else:
                st.error(f"Wrong! The correct article was: {chosen_title.replace('_', ' ')}")
            st.info(f"First sentence of the article: {st.session_state.first_sent} \n\nPress (Re)Start Game above to play again.")
            
            # Reset the game state
            st.session_state.game_state = "not_started"
            st.session_state.selected_answer = None
        else:
            st.warning("Please select an answer before submitting.")