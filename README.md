# Fantasy-Baseball
Analyzing CBS fantasy baseball stats

This is currently a work in progress, but the project scrapes data from the league's scoring stats page to plot potentially interesting data with matplotlib. 

# How to use

You just need to create a python environment from the requirements.txt file. 

To execute the script, just type the following in the root directory of this repository:
```
python Fantasy_Baseball
```

Set the following variables in your environment. You can do this for ease, but please only add the password variable to your account if it is unique and not used for anything else. Storing passwords as plain text in your .*profile* isn't the safest idea. 

```
league_name = your league name xxx.baseball.cbssports.com, where xxx is league name
CBS_USERNAME = your email address for your CBS fantasy account
CBS_Password = your password for your CBS fantasy account.
```

![pitching](League/Pitching_stats_2022-08-15.png)
![hitting](hitting_stats_2022-08-15.png)
