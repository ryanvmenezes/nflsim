from __future__ import division
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys

RAMS = pd.read_csv('teams_ram__team_index.csv', skiprows=2)
rams = RAMS[['Year','Tm','W','L','T','MoV','SoS','SRS','OSRS','DSRS']]

def game_sim(homeyear, awayyear, p=True):
    '''
    Takes a home and away year, simulates a game and spits out a result
    '''
    homerow = rams[rams['Year'] == homeyear]
    awayrow = rams[rams['Year'] == awayyear]
    try:
        srshome = float(homerow['SRS'])
    except TypeError:
        print "No home team for {}".format(homeyear)
        return None
    
    try:
        srsaway = float(awayrow['SRS'])
    except TypeError:
        print "No away team for {}".format(awayyear)
        return None
    
    pointdiff = srshome - srsaway
    result = np.random.normal(pointdiff, 13.45)

    if p:
        print "SIMULATING ONE GAME ..."
        print "Matchup:"
        print "Home team: {} ({}-{}-{}) SRS {}".format(
            int(homerow['Year']),
            int(homerow['W']),
            int(homerow['L']),
            int(homerow['T']),
            srshome
        )
        print "Away team: {} ({}-{}-{}) SRS {}".format(
            int(awayrow['Year']),
            int(awayrow['W']),
            int(awayrow['L']),
            int(awayrow['T']),
            srsaway
        )
        print ('Home team' if pointdiff > 0 else 'Away team') + ' favored by {}'.format(int(abs(round(pointdiff))))
        print "Game result:"
        print ('Home team' if result > 0 else 'Away team') + ' won by {}'.format(int(abs(round(result))))

        return None

    return result

if __name__ == '__main__':
    game_sim(int(sys.argv[1]), int(sys.argv[2]))

    print "---"

    print "SIMULATING 1,000 GAMES ..."

    sims = [ game_sim(int(sys.argv[1]), int(sys.argv[2]), False) for _ in range(0,1000) ]

    homewins = sum(s > 0 for s in sims)
    awaywins = sum(s < 0 for s in sims)
    ties = sum(s == 0 for s in sims)

    print "Over 1,000 simulations, {} home wins, {} away wins and {} ties".format(homewins, awaywins, ties)

