# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

# Input show title to find the imdb id

# Variables
show = 'Doctor Who'
url_search = 'https://www.imdb.com/find?q='

# Set up Dataframe to create Heatmap


# Put the search term in the url_search     example: imdb.com/find?q=breaking+bad
for word in show.split():
    if url_search[-1] == '=':
        url_search = url_search + word
    else:
        url_search = url_search + '+' + word
# url_search

# Parse the get request
get_search = requests.get(url_search)
soup_search = BeautifulSoup(get_search.text, 'html.parser')

# Get the imdb_id
find_search = soup_search.find('tr', attrs={'class': 'findResult odd'})
imdb_id = find_search.find('a')['href'].split('/')[2]
show = find_search.find_all('a')[1].text
print(show)
print(imdb_id)

# Use the imdb id to find the latest season available
get_home = requests.get('https://www.imdb.com/title/' + imdb_id)
soup_home = BeautifulSoup(get_home.text, 'html.parser')
# soup_home

# find the latest season available
find_home = soup_home.find('div', attrs={'class': 'seasons-and-year-nav'})
max_season = int(find_home.find('a').text)
max_season

# Find the ratings for episodes in each season
records = []
for current_season in range(1, max_season + 1):
    get_season = requests.get('https://www.imdb.com/title/' + imdb_id + '/episodes?season=' + str(current_season))
    soup_season = BeautifulSoup(get_season.text, 'html.parser')

    # List of ratings
    find_season = soup_season.find_all('span', attrs={'class': 'ipl-rating-star__rating'})[
                  ::23]  # ratings occur in every 23rd item

    episode = 1
    for rating in find_season:
        records.append((show, current_season, episode, float(rating.text)))
        episode += 1

# Add records to DataFrame
df = pd.DataFrame(records, columns=['show', 'season', 'episode', 'rating'])

# Num of season and episodes determine size of plot
max_season = df.season.max()
max_episode = df.episode.max()
print(df.episode.count())

# Pivot Table
df_pivot = df.pivot(index='season', columns='episode', values='rating')
df_pivot

# Plot
f, ax = plt.subplots(figsize=(max_episode, max_season))
ax = sns.heatmap(df_pivot, vmin=6, vmax=10, annot=True, linewidths=1, cmap='RdYlGn', linecolor='gray', cbar=False)
ax.set_title(show, fontsize=30)
ax.set_xlabel('Episode', fontsize=20, labelpad=15)
ax.set_ylabel('Season', fontsize=20, labelpad=15)
ax.tick_params(labelsize=15)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(show + '.png')
plt.show()