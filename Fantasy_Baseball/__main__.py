import fantasy_baseball as fb

if __name__ == "__main__":

    #fb.loadCBScreds()
    html = fb.loadfantasy()
    h_stats, p_stats = fb.scrape(html)

    #handle duplicate columns
    h_stats, p_stats = fb.remove_FPTS(h_stats, p_stats)

    #Apply League Rules
    h_stats = fb.scoring_rules_hitting(h_stats)
    p_stats = fb.scoring_rules_pitching(p_stats)
    fb.plot_bar(h_stats, p_stats)