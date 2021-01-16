import time
import random

from nba_api.stats.endpoints import playergamelog, commonplayerinfo

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.patches as mpatches
import matplotlib.table as table
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import nba_api.stats.static.teams as teams
from nba_api.stats.endpoints import commonteamroster

def violin_swarm_box_scores(fig, ax, violin_data, swarm_data, stat_header, orientation):
    # points subplot
    if orientation == 'h':
        ax.set_title(stat_header, y=1.0, pad=-14)
        ax.tick_params(direction = 'in')
        if len(violin_data) > 0:
            sns.violinplot(fig = fig,
                        ax = ax,
                        data = violin_data[stat_header],
                        orient = 'h',
                        width = 0.5,
                        legend = False,
                        scale = 'area',
                        inner = None, 
                        cut = 0,
                        bw = 0.5)
        plt.setp(ax.collections, alpha = 0.1)
        plt.scatter(swarm_data[stat_header][0], 0, 
                    marker='o', 
                    s=55, 
                    c = 'blue')
        ax.annotate(swarm_data[stat_header][0], 
                    (swarm_data[stat_header][0], 0), 
                    textcoords = 'offset pixels', xytext = (0, 7), 
                    fontsize = 10, 
                    horizontalalignment='center')
        sns.swarmplot(swarm_data[stat_header][1:], 
                      np.zeros(len(swarm_data[stat_header]) - 1), 
                      ax = ax, orient = 'h', 
                      color = 'blue', 
                      alpha = 0.2, 
                      size = 6)
        ax.get_yaxis().set_visible(False)
        ax.set_xlim(left = 0)
        ax.set_ylim(bottom = -0.35, top = 0.45)
        ax.axes.get_xaxis().get_label().set_visible(False)
    else:
        ax.set_title(stat_header, y=1.0, pad=-14)
        ax.tick_params(direction = 'in')
        if len(violin_data) > 0:
            sns.violinplot(fig = fig,
                        ax = ax,
                        data = violin_data[stat_header],
                        orient = 'v',
                        width = 0.5,
                        legend = False,
                        scale = 'area',
                        inner = None, 
                        cut = 0,
                        bw = 0.5)
        plt.setp(ax.collections, alpha = 0.1)
        plt.scatter(0, swarm_data[stat_header][0],
                    marker='o', 
                    s=55, 
                    c = 'blue')
        ax.annotate(swarm_data[stat_header][0], 
                    (0, swarm_data[stat_header][0]), 
                    textcoords = 'offset pixels', xytext = (13, -5), 
                    fontsize = 10, 
                    horizontalalignment='center')
        sns.swarmplot(np.zeros(len(swarm_data[stat_header]) - 1), 
                      swarm_data[stat_header][1:], 
                      ax = ax, orient = 'v', 
                      color = 'blue', 
                      alpha = 0.2, 
                      size = 6)
        ax.get_xaxis().set_visible(False)
        ax.set_ylim(bottom = 0, top = swarm_data[stat_header].max()*1.15)
        ax.axes.get_yaxis().get_label().set_visible(False)
        
def generate_box_score_figure(player_id, this_season, savedir = 'C:\\Users\\besid\\Desktop\\'):

    nba_cooldown = random.gammavariate(alpha=9, beta=0.4)

    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_id).get_data_frames()[0]
    time.sleep(nba_cooldown)
    box_scores_this_season = playergamelog.PlayerGameLog(player_id = player_id, season = this_season).get_data_frames()[0]
    time.sleep(nba_cooldown)
    box_scores_last_season = playergamelog.PlayerGameLog(player_id = player_id, season = this_season - 1).get_data_frames()[0]
    time.sleep(nba_cooldown)

    sns.color_palette("coolwarm", as_cmap=True)

    fig = plt.figure(figsize=(6,8), constrained_layout = False, dpi = 80)

    # create subplots
    gs = fig.add_gridspec(11, 4)

    ax0 = fig.add_subplot(gs[0:2, 0:4])
    ax0.axis('off')
    table.table(ax = ax0, cellText = [['Player:', player_info['DISPLAY_FIRST_LAST'][0]],
                                    ['Team:', player_info['TEAM_CITY'][0]],
                                    ['Position:', player_info['POSITION'][0]],
                                    ['Height:', player_info['HEIGHT'][0]],
                                    ['Last Game:', box_scores_this_season['GAME_DATE'][0]]], 
                                    cellLoc = 'left',
                                    edges = 'open', 
                                    loc = 'center')
    
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=box_scores_this_season['GAME_DATE'][0],
                              markerfacecolor='blue', markersize=9),
                       Line2D([0], [0], marker='o', color='w', label=str(this_season) + ' season',
                              markerfacecolor='blue', markersize=8, alpha = 0.3),
                       Patch(facecolor='gray', label=str(this_season-1) + ' season', alpha = 0.4)]
    ax0.legend(handles = legend_elements, loc = 'lower center', bbox_to_anchor = (0, -0.35, 1, 1), mode = 'expand', ncol = 3, frameon = False)

    ax1 = fig.add_subplot(gs[2:4, 0:])
    violin_swarm_box_scores(fig, ax1, box_scores_last_season, box_scores_this_season, 'PTS', orientation = 'h')

    ax2 = fig.add_subplot(gs[4:6, 0:2])
    violin_swarm_box_scores(fig, ax2, box_scores_last_season, box_scores_this_season, 'FG_PCT', orientation = 'h')

    ax3 = fig.add_subplot(gs[4:6, 2:4])
    violin_swarm_box_scores(fig, ax3, box_scores_last_season, box_scores_this_season, 'FT_PCT', orientation = 'h')

    ax4 = fig.add_subplot(gs[6:11, 0])
    violin_swarm_box_scores(fig, ax4, box_scores_last_season, box_scores_this_season, 'REB', orientation = 'v')

    ax5 = fig.add_subplot(gs[6:11, 1])
    violin_swarm_box_scores(fig, ax5, box_scores_last_season, box_scores_this_season, 'AST', orientation = 'v')

    ax6 = fig.add_subplot(gs[6:11, 2])
    violin_swarm_box_scores(fig, ax6, box_scores_last_season, box_scores_this_season, 'STL', orientation = 'v')

    ax7 = fig.add_subplot(gs[6:11, 3])
    violin_swarm_box_scores(fig, ax7, box_scores_last_season, box_scores_this_season, 'BLK', orientation = 'v')

    plt.subplots_adjust(hspace = 0.8, wspace = 0.4)
    plt.savefig(savedir + str(player_id) + '.jpg', bbox_inches="tight")
    
def get_team_roster(abbreviation = 'okc'):
    # get team id by team abbreviation
    team_info = teams.find_team_by_abbreviation(abbreviation)
    team_id = team_info['id']

    # use team id to get roster
    team_roster = commonteamroster.CommonTeamRoster(team_id = team_id).get_data_frames()
    team_roster = team_roster[0][['PLAYER', 'PLAYER_ID']]
    
    return team_roster