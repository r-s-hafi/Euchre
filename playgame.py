from logic import initialize_players, initialize_db, get_trump, update_bowers, play_trick, score_trick, rotate_players, score_round, end_game
from database import deal_cards, top_deck
import sqlite3

def main():
    while True:
        connection = sqlite3.connect('euchre.db')
        players = initialize_players()

        team1_game_score = 0
        team2_game_score = 0

        while team1_game_score < 10 and team2_game_score < 10:

            initialize_db()
            players = deal_cards(connection, players)
            top_card = top_deck(connection)
            trump, players = get_trump(top_card, players)
            players = update_bowers(trump, players)

            team1_round_score = 0
            team2_round_score = 0

            while (team1_round_score + team2_round_score < 5):
                trick, players, follow_suit = play_trick(players) #make sure dealer can get stuck with picking trump edge case
                team1_round_score, team2_round_score, winning_player = score_trick(trump, follow_suit, trick, players, team1_round_score, team2_round_score)
                players = rotate_players(players, winning_player)

            team1_game_score, team2_game_score = score_round(team1_round_score, team2_round_score, players, team1_game_score, team2_game_score)
        
        restart_choice =end_game(team1_game_score, players)
        if restart_choice != 'Y':
            break


    #make landing page
    #make playing page
    #incorporate score in front end
    #thats like it

if __name__ == '__main__':
    main()


