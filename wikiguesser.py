# This is a simple quiz game called "Wikipedia Guesser"
# The game takes a random sentence from a random Wikipedia article.
# The player must then guess which of the 4 provided article titles contains the sentence.

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
        #print(response)
        items = response.json().get('items', [])
        #print(items)
        titles.append(items[0]['title'])
    return titles

# Function to get a random sentence from given Wiki article title
def get_rand_sentence(title):
    normalised_title = title
    title = title.replace(' ', '_')
    article_url = f'https://en.wikipedia.org/wiki/{title}'

    # We initialise the sentence variable with the title - this will make sense later
    chosen_sentence = normalised_title

    response = req.get(article_url)

    if response.status_code != 200:
        print(f'Failed to fetch {article_url}, status code: {response.status_code}')
        return

    article_content = BeautifulSoup(response.text, 'html.parser')
    all_pars = article_content.find_all('p')
    #print(f'Article {title} has {len(all_pars)} paragraphs')

    # Initialise list of sentences in each paragraph
    sentences = []

    # Convert our paragraphs to text:
    #all_pars = all_pars.get_text

    for par in all_pars:
        par_text = par.get_text(separator=' ', strip = True)
        sentences.extend(par_text.split('. '))

    #first_sentence = sentences[0]

    title_words = set(normalised_title.lower().split())

    valid_sentences = [s for s in sentences if not any(word in s.lower() for word in title_words)]
    first_sentence = valid_sentences[0]

    #while any(title_words) in chosen_sentence.lower() or not chosen_sentence:
    chosen_sentence = random.choice(valid_sentences)    

    #print('\n\nThis is a random sentence from this article:\n\n', chosen_sentence)    
    return first_sentence, chosen_sentence



#print('Generating 4 random wiki titles:')
#print(get_4_titles())


# MAIN GAME CODE BELOW:

print('\n\nWelcome to Marcin\'s Wikipedia Guesser Game!')
      
while True:
    print('\n\nPlease wait, as the game is being prepared.')

    drawn_titles = get_4_titles()
    correct_answer = random.randint(0, 3)
    chosen_title = drawn_titles[correct_answer]
    chosen_url = f'https://en.wikipedia.org/wiki/{chosen_title}'

    indices = ['a)', 'b)', 'c)', 'd)']


    print('\n\nI have chosen 4 Wikipedia articles at random:')
    for i in range(4):
        print(indices[i], drawn_titles[i].replace('_', ' '))

    #print('From these 4, the chosen one is: ', chosen_title.replace('_', ' '))
    #print('\n\nHere is a random sentence from the chosen article:')
    first_sent, rand_sent = get_rand_sentence(chosen_title)

    print('\n\nThis is a random sentence from this article:\n\n', rand_sent)   

    drawn_titles[correct_answer] = drawn_titles[correct_answer].replace('_',  ' ')

    print('\n\nWhich of the above articles does it come from?\n\nYour answer:')
    answer = input().strip().lower()

    while f'{answer.lower()})' not in indices:
        print('Please type a valid answer: a, b, c or d')
        answer = input().strip().lower()

    if f'{answer.lower()})' == indices[correct_answer]:
        print(f'\nYes! You got it right! Correct answer is {indices[correct_answer]} {drawn_titles[correct_answer]}')
    else: print(f'Unfortunately, that is not right. Correct answer is {indices[correct_answer]} {drawn_titles[correct_answer]}')

    print('\n\n', first_sent)

    play_again = input('\n\nDo you want to play again? (Y/N)').strip().lower()

    if play_again != 'y':
        print('\nThanks for playing! See you next time!')
        break