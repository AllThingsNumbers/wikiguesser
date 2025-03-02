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
    #valid_sentences = [s for s in sentences if not any(word in s.lower() for word in title_words)]

    valid_sentences = [
    s for s in sentences
    if not (
        any(word in s.lower() for word in title_words)  # Exclude sentences containing title words
        or any(word in s.lower() for word in ["stub", "expanding"])  # Exclude "stub" or "expanding"
        or len(s) < 20  # Exclude short sentences
    )
    ]
    
    # for valid_sent in valid_sentences:
    #     for word in valid_sent:
    #         if word in title_words:
    #             word = "XXXXX"

    #if len(valid_sentences) < 2:
    #    return None, None
    
    return sentences[0], random.choice(valid_sentences)

# Streamlit UI
st.title("Wikipedia Guesser Game")
st.write('Welcome to Wiki Guesser.\n\nGuess the correct Wikipedia article based on the provided sample.')

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
if "chosen_html" not in st.session_state:
    st.session_state.chosen_html = ""

# Start the game when button is clicked
if st.session_state.game_state == "not_started":
    #st.write('Welcome to Wiki Guesser.\n\nGuess the correct Wikipedia article based on the provided sample.\n\nPlease wait, as the game is being prepared.')
    st.session_state.game_state = "playing"

if st.button('Pick a random article', key="draw_article"):

    st.session_state.game_state = "playing"
    st.write('Choosing 4 articles at random, please wait.')
    while True:  # Keep trying until a valid sentence is found
        st.session_state.drawn_titles = get_4_titles()
        st.session_state.correct_answer = random.randint(0, 3)
        chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]
        chosen_url = f'https://en.wikipedia.org/wiki/{chosen_title}'
        st.session_state.chosen_html = f'<a href="{chosen_url}" target="_blank" rel="noopener noreferrer">{chosen_title.replace("_", " ")}</a>'

        first_sent, rand_sent = get_rand_sentence(chosen_title)

        if first_sent and rand_sent:
            st.session_state.first_sent = first_sent
            st.session_state.rand_sent = rand_sent
            break  # Exit loop when valid sentences are found

    # st.session_state.drawn_titles = get_4_titles()
    # st.session_state.correct_answer = random.randint(0, 3)
    # chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]
    st.session_state.game_state = "drawn"
    # first_sent, rand_sent = get_rand_sentence(chosen_title)
    
    # if not first_sent or not rand_sent:
    #     st.error("Could not retrieve a valid sentence. Try again.")
    #     st.session_state.game_state = "not_started"
    # else:
    #     st.session_state.first_sent = first_sent
    #     st.session_state.rand_sent = rand_sent

# Game UI
if st.session_state.game_state == "drawn":
    st.subheader("Which article is this sentence from?")
    st.write(st.session_state.rand_sent)
    
    # Radio button (stores answer in session state)
    st.session_state.selected_answer = st.radio(
        "Choose an article:",
        [title.replace('_', ' ') for title in st.session_state.drawn_titles],
        #st.session_state.drawn_titles,
        index=None,
        key=st.session_state.get("radio_key", "radio_default")
    )

    # Submit answer button
    if st.button('Submit Answer'):
        if st.session_state.selected_answer:  # Ensure an answer is selected
            chosen_title = st.session_state.drawn_titles[st.session_state.correct_answer]
            if st.session_state.selected_answer.replace(' ', '_') == chosen_title:
                st.success(f"Correct! The article was: {chosen_title.replace('_', ' ')}")
            else:
                st.error(f"Wrong! The correct article was: {chosen_title.replace('_', ' ')}")
            st.info(f"First sentence of the article: {st.session_state.first_sent}")

            st.write("Click the link to open the article and learn more about it: ") 
            st.html(st.session_state.chosen_html)
            st.write("\nor press the button at the top to play again.")
            
            # Reset the game state
            # st.session_state.game_state = "not_started"
            # st.session_state.selected_answer = None
            # if st.button('Play again', key="restart_after_answer"):
            #     st.session_state.game_state = "not_started"
            #     st.session_state.selected_answer = None  # Clear selection
            #     st.session_state.radio_key = str(random.randint(0, 100000))  # Change key to reset radio
            #     st.rerun()  # Force Streamlit to refresh the app
        else:
            st.warning("Please select an answer before submitting.")
