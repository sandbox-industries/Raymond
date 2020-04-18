# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

# Generate a heatmap of a tv series episodes


# Input show title to find the imdb id

# Variables
show = 'Doctor Who'
url_search = 'https://www.imdb.com/find?q='

# Set up Dataframe to create Heatmap
df = pd.DataFrame(columns=['show', 'season', 'episode', 'rating'])
df = df.astype({'show': 'str', 'season': 'int', 'episode': 'int', 'rating': 'float'})

# Put the search term in the url_search     example: imdb.com/find?q=breaking+bad
for word in show.split():
    if url_search[-1] == '=':
        url_search = url_search + word
    else:
        url_search = url_search + '+' + word

# Parse the get request
r_search = requests.get(url_search)
soup_search = BeautifulSoup(r_search.text, 'html.parser')

# Get the imdb id
content_search = soup_search.find('tr', attrs={'class': 'findResult odd'})
imdb_id = content_search.find('a')['href'].split('/')[2]
show = content_search.find_all('a')[1].text
print('title:' + show)
print('imdb_id:' + imdb_id)

# Use the imdb id to find the latest season available

# Parse the get request
r_home = requests.get('https://www.imdb.com/title/' + imdb_id)
soup_home = BeautifulSoup(r_home.text, 'html.parser')

# find the latest season available
content_home = soup_home.find('div', attrs={'class': 'seasons-and-year-nav'})
max_season = int(content_home.find('a').text)
print('seasons:' + str(max_season))

# Find the ratings for episodes in each season
for current_season in range(1, max_season + 1):
    r_season = requests.get('https://www.imdb.com/title/' + imdb_id + '/episodes?season=' + str(current_season))
    soup_season = BeautifulSoup(r_season.text, 'html.parser')
    # soup_season
    episode = 1
    results = soup_season.find_all('span', attrs={'class': 'ipl-rating-star__rating'})[
              ::23]  # ratings occur in every 23rd item
    for rating in results:
        # print(current_season,episode,rating.text)
        df = df.append({'show': show, 'season': current_season, 'episode': episode, 'rating': float(rating.text)},
                       ignore_index=True)
        episode += 1

# Num of season and episodes determine size of plot
max_season = df.season.max()
max_episode = df.episode.max()

# Pivot Table
df_pivot = df.pivot(index='season', columns='episode', values='rating')

# Plot
f, ax = plt.subplots(figsize=(max_episode, max_season))
ax = sns.heatmap(df_pivot,vmin=6,vmax=10, annot=True,linewidths=1, cmap='RdYlGn', linecolor='gray', cbar=False)
ax.set_title(show,fontsize=30)
ax.set_xlabel('Episode',fontsize=20,labelpad=15)
ax.set_ylabel('Season',fontsize=20,labelpad=15)
ax.tick_params(labelsize=15)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(show+'.png')
