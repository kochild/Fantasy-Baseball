import getpass
import lxml.html
import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import time

matplotlib.use
plt.style.use('ggplot')

"""
Make sure you set your environmental variables before running script
"""

# Let's check to see if we have any environment variables set
def loadCBScreds():
    "Load the League information from your environment variables over here"
    if 'league_name' in os.environ:
        league_name = os.environ['league_name'] # The Leagues Name | xxx.baseball.cbssports.com, where xxx is the league name. 
    else:
        league_name = input('Enter CBS Fantasy League name: ')
    if 'CBS_USERNAME' in os.environ:
        user_name = os.environ['CBS_USERNAME'] # CBS username 
    else:
        user_name = input('Enter username: ')
    if 'CBS_Password' in os.environ:
        password = os.environ['CBS_Password'] # Your CBS password. This better be a unique password 
    else:
        password = getpass.getpass()
    return league_name, user_name, password

def loadfantasy():
    """Login into CBS and let's get a database made of the site"""
    # Let's load up the login information and download the html page!
    league_name, user_name, password = loadCBScreds() 
    login_url = 'https://www.cbssports.com/login/'
    url = f"http://{league_name}.baseball.cbssports.com/stats/stats-main/teamtotals/ytd:f/scoring/stats" # F string format is really useful
    session = requests.session()
    login = session.get(login_url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath('//form//input')
    # <InputElement 116779bc0 name='userid' type='text'> These two are the boxes
    #<InputElement 116779cb0 name='password' type='password'> 
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs if x.attrib['type'] != 'checkbox'} # They shouldn't be checkboxes
    form['userid'] = user_name
    form['password'] = password
    session.post(login_url, data=form)
    response = session.get(url)
    return response.content

def scrape(html):
    """Use pandas read_html function to generate tables for hitting and pitching"""
    frame = pd.read_html(html)
    n = 1
    df = frame[0]
    df.drop(df.tail(n).index,
        inplace = True)
    h_stats = df
    h_stats = h_stats.pop('Year to Date Fantasy Scoring Categories')
    df2 = frame[1]
    df2.drop(df2.tail(n).index,
        inplace = True)
    p_stats = df2
    p_stats = p_stats.pop('Year to Date Fantasy Scoring Categories')
    return h_stats, p_stats

def remove_FPTS(h_stats, p_stats):
    """Drop FPTS from the dataframe and make the Team name the first frame"""
    h_stats = h_stats.drop(['FPTS'], axis=1)
    h_stats = h_stats.set_index('Team')
    p_stats = p_stats.drop(['FPTS'], axis=1)
    p_stats = p_stats.set_index('Team')
    return h_stats, p_stats

def df_column_uniquify(stats):
    """Not really needed when we split up the table, but let's keep it for the future https://stackoverflow.com/questions/24685012/pandas-dataframe-renaming-multiple-identically-named-columns"""
    df_columns = stats.columns
    new_columns = []
    for item in df_columns:
        counter = 0
        newitem = item
        while newitem in new_columns:
            counter += 1
            newitem = "{}_{}".format(item, counter)
        new_columns.append(newitem)
    stats.columns = new_columns
    return stats

def scoring_rules_hitting(h_stats):
    """Modify Values Here for your hittings stats"""
    cols=[i for i in h_stats.columns if i not in ["Team"]]
    for col in cols:
        h_stats[col]=pd.to_numeric(h_stats[col])
    h_stats["2B"] = h_stats["2B"] * 2
    h_stats["3B"] = h_stats["3B"] * 3
    h_stats["K"] = h_stats["K"] * -1
    h_stats["CS"] = h_stats["CS"] * -1
    h_stats["CSC"] = h_stats["CSC"] * 0
    h_stats["CYC"] = h_stats["CYC"] * 10
    h_stats["E"] = h_stats["E"] * -1
    h_stats["GDP"] = h_stats["GDP"] * -1
    h_stats["HR"] = h_stats["HR"] * 4
    h_stats["OFAST"] = h_stats["OFAST"] * 0
    return h_stats

def scoring_rules_pitching(p_stats):
    """Points for our pitching stats. Change if needed"""
    cols=[i for i in p_stats.columns if i not in ["Team"]]
    for col in cols:
        p_stats[col]=pd.to_numeric(p_stats[col])
    p_stats["BB"] = p_stats["BB"] * -1
    p_stats["B"] = p_stats["B"] * -1
    p_stats["BS"] = p_stats["BS"] * -5
    p_stats["CG"] = p_stats["CG"] * 5
    p_stats["ER"] = p_stats["ER"] * -1
    p_stats["H"] = p_stats["H"] * -1
    p_stats["HB"] = p_stats["HB"] * -1
    p_stats["INN"] = p_stats["INN"] * 3
    p_stats["L"] = p_stats["L"] * -5
    p_stats["NH"] = p_stats["NH"] * 10
    p_stats["PG"] = p_stats["PG"] * 10
    p_stats["QS"] = p_stats["QS"] * 5
    p_stats["S"] = p_stats["S"] * 10
    p_stats["SO"] = p_stats["SO"] * 10
    p_stats["W"] = p_stats["W"] * 5
    p_stats["WP"] = p_stats["WP"] * -1
    return p_stats

def plot_bar(h_stats, p_stats):
    league_name, _, _ = loadCBScreds() 
    league_name = league_name.upper()
    """Make charts and save csv"""
    color = 'ocean' #Any color under matplotlib will work
    h_stats = h_stats.reindex(h_stats.mean().sort_values().index, axis=1)
    p_stats = p_stats.reindex(p_stats.mean().sort_values().index, axis=1)
    h_stats.plot.barh(stacked=True, colormap = color, figsize=(8, 10))
    plt.title(league_name +' Hitting Stats as of ' + time.strftime("%m-%d-%Y"))
    plt.xlabel('FTPS')
    plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon = False)
    plt.savefig('League/hitting_stats_' + time.strftime("%Y-%m-%d") + '.png',
                bbox_inches='tight')
    plt.clf()
    p_stats.plot.barh(stacked=True, colormap = color, figsize=(8, 10))
    plt.title(league_name +' Pitching Stats as of ' + time.strftime("%m-%d-%Y"))
    plt.xlabel('FTPS')
    plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon = False)
    plt.savefig('League/Pitching_stats_' + time.strftime("%Y-%m-%d") + '.png',
                bbox_inches='tight')
    h_stats.to_csv('csv/hittings_stats_as_of ' + time.strftime("%m-%d-%Y") + '.csv')
    p_stats.to_csv('csv/pitching_stats_as_of '+ time.strftime("%m-%d-%Y") + '.csv')

def plot_scoring_bar(h_stats, p_stats):
    league_name, _, _ = loadCBScreds() 
    league_name = league_name.upper()
    """Make charts and save csv"""
    color = 'hot' #Any color under matplotlib will work
    h_stats = h_stats.reindex(h_stats.mean().sort_values().index, axis=1)
    h_stats = h_stats.drop(['CS', 'E','GDP', 'HP', '3B', 'CSC'], axis=1)
    p_stats = p_stats.drop(['B','CG', 'BS', 'H', 'HB', 'WP', 'PKO', 'NH', 'PG'], axis=1)
    h_stats.plot.barh(stacked=True, colormap = color, figsize=(8, 10))
    plt.title(league_name +' Hitting Scoring Stats as of ' + time.strftime("%m-%d-%Y"))
    plt.xlabel('FTPS')
    plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon = False)
    plt.savefig('League/hitting_stats_scoring_' + time.strftime("%Y-%m-%d") + '.png',
                bbox_inches='tight')
    plt.clf()
    p_stats.plot.barh(stacked=True, colormap = color, figsize=(8, 10))
    plt.title(league_name +' Pitching Scoring Stats as of ' + time.strftime("%m-%d-%Y"))
    plt.xlabel('FTPS')
    plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon = False)
    plt.savefig('League/Pitching_stats_scoring_' + time.strftime("%Y-%m-%d") + '.png',
                bbox_inches='tight')
    h_stats.to_csv('csv/hittings_scoring_stats_as_of ' + time.strftime("%m-%d-%Y") + '.csv')
    p_stats.to_csv('csv/pitching_scoring_stats_as_of '+ time.strftime("%m-%d-%Y") + '.csv')