# Fantasy-Baseball
Analyzing CBS fantasy baseball stats

This is currently a work in progress, but the project scrapes data from the league's scoring stats page to plot potentially interesting data with matplotlib. 

# How to use

You just need to create a python environment from the requirements.txt file. I'm using python 3.10, but any python version that installs from the requirement file should work.


To execute the script, just type the following in the root directory of this repository in your terminal:
```
python Fantasy_Baseball
```

It will prompt you to type your league name, your username, and password. After that, it should load your league information and create graphs of your team's scoring page. This is currently specific to my league's scoring rules, so you'll want to match them with your league's scoring system. Edit scoring_rules_h_stats and p_stats to match your rules, or add to them if things don't match. 

As usual, you should look over the script to be sure that your information is safe and not being hijacked by me or anyone else. 

If you want, you can also set variables in your environment so you don't have to keep typing in league name, username, and passwords.
Please only add a password variable of your account if it is unique and not used for anything else. Storing passwords as plain text in your .*profile* isn't the safest idea, so make sure it's unique. 

```
league_name = your league name xxx.baseball.cbssports.com, where xxx is league name
CBS_USERNAME = your email address for your CBS fantasy account
CBS_Password = your password for your CBS fantasy account.
```


# Metrics of Each Team

![pitching](League/Pitching_stats_2022-08-18.png)
![hitting](League/hitting_stats_2022-08-18.png)

# Metrics of League

![pitching_league](League/Average_pitching_scores_2022-08-18.png)

So from this graph, we can tell most points in my league come from innings pitched and strickouts, a little bit from saves. Biggest loss of points are from hits.

![hitting_league](League/Average_hitting_scores_2022-08-18.png)

So from this graph, we can tell that singles, home runs, runs, RBIs, doubles, and BB are huge for points gained. Strikouts are the leading cause of losing points. 

## If anyone wants to help make this better, feel free to contribute :) 