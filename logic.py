from models import Player, User, Bot
import random
import time
from typing import List, Union
from operator import attrgetter
import sqlite3

def initialize_db()->None:
    connection = sqlite3.connect('euchre.db')
    with open('migrations/cards.sql', 'r', encoding='utf-8') as sql_file:
        sql = sql_file.read()
        connection.executescript(sql)

def initialize_players()->List[Union[User, Bot]]:
    username = input("Please select a username: \n")
    user = User(username)
    bot1 = Bot('bot1')
    bot2 = Bot('bot2')
    bot3 = Bot('bot3')

    order_list = list(range(1, 5))
    players = [user, bot1, bot2, bot3]

    for player in players:
        player.order = random.choice(order_list)
        order_list.remove(player.order)
        if player.order % 2 == 1:
            player.team = 1
        else:
            player.team = 2
        player.is_turn = player.order == 1

    random.choice(players).is_turn = True
    
    players = sorted(players, key=attrgetter('order'))

    return players

def get_trump(card: tuple, players: List[Union[Player, Bot]])-> str:
    #1st round of picks
    trump_selected = False
    trump = str()
    pick = 0

    while not trump_selected and pick < 4: #first round to determine trump - dealer picks card

        for player in players:
            print(f"\nIt is {player.name}'s turn. {player.name} is on team {player.team}")
            pick += 1
            if player.type == 'User': #if the player is the user
                decision = input(f"\nDoes {player.name} want to accept {card[1].lower()[:-1]} as trump? Y/N: ")
                if decision == 'Y':
                    trump = card[1]
                    trump_selected = True
                    player.is_maker = True
                    break

                elif decision == 'N':
                    print(f"\n{player.name} has passed on the card.") #save exception handling for front end (either click button or dont)
                    continue

                else:
                    print("Please enter valid input")

            else: #if the player is a bot
                rand_list = ['N', 'Y', 'Y', 'Y']
                decision = rand_list[random.randint(0, 3)]
             #   time.sleep(2)
                if decision == 'Y':
                    trump = card[1]
                    trump_selected = True
                    player.is_maker = True
                    print(f"\n{player.name} has chosen {trump} as trump.")
                    break
            
                else:
                    print(f"\n{player.name} has passed on the card.")
                    continue
                
    for player in players:
        #2nd round of picks
        if trump_selected and player.order == 4:
            print(f"\nBecause {player.name} is dealer, they will pick it up.")

            if player.type == "User": #if the player is the dealer they must pick up the card
                burn_num = int(input(f"\nPlease select a card to remove from your hand (1-5): "))

            else:
                burn_num = random.randint(0, 4)

            print(f"\n{player.hand[burn_num - 1]} has been removed from {player.name}'s hand.")
            player.hand.pop(burn_num - 1)
            player.hand.append(card)
            print(f"\n{player.name} has picked up the card. Trump is set to {trump}.")
            return trump.capitalize(), players
        
    pick = 0
    print("\nNobody picked up the card. It is discarded and players can now choose trump.")
    suits = ['pass', 'pass', 'pass', 'pass', 'spades', 'clubs', 'hearts', 'diamonds'] #FIX THIS LASER
    while not trump_selected and pick < 3:

        for player in players:
            
            pick += 1
            if pick == 4:
                break
            
            print(f"\nIt is {player.name}'s turn to choose trump.")

            if player.type == 'User': #if player is user
                decision = input(f"\nPlease select a suit or pass: (spades/clubs/diamonds/hearts/pass): ")
                if decision in suits and decision != 'pass':
                    trump = decision
                    trump_selected = True
                    player.is_maker = True
                    print(f"\n{player.name} has chosen {trump} as trump.")
                    return trump.capitalize(), players
                
                else:
                    print(f"\n{player.name} has passed.")
                    continue

            else: #if player is a bot
                decision = suits[random.randint(0, 7)]
               # time.sleep(2)
                if decision == 'pass':
                    print(f"\n{player.name} has passed.")
                    continue

                else:
                    trump = decision
                    trump_selected = True
                    player.is_maker = True
                    print(f"\n{player.name} has chosen {trump} as trump.")
                    return trump.capitalize(), players
        
        for player in players:
            if player.order == 4:
                trump_selected = True
                if player.type == 'User':
                    trump = input(f"\n{player.name} must pick trump (suits: spades/clubs/diamonds/hearts): ")
                    print(f"\n{player.name} has chosen {trump} as trump.")
                    return trump.capitalize(), players
                else:
                    print(f"\n{player.name} must pick trump (suits: spades/clubs/diamonds/hearts): ")
                    trump = suits[random.randint(4, 7)]
                    print(f"\n{player.name} has chosen {trump} as trump.")
                    return trump.capitalize(), players
            
def update_bowers(trump: str, players: List[Union[Player, Bot]])-> List[Union[User, Bot]]:
    
    black = ['Spades', 'Clubs']
    red = ['Hearts', 'Diamonds']
    
    for player in players:
        for card in player.hand: #loop through all cards in all players' hands

            if card[0] == 'J': #if the card is a jack
                if trump in black and card[1] in black: #if trump AND the card are black
                    if card[1] == trump: #right bower
                        card[3] = 16

                    else: #left bower - makes the other jack the same suit as trump
                        card[1] = trump
                        card[3] = 15

                if trump in red and card[1] in red:
                    if card[1] == trump:
                        card[3] = 16
                        print(f"{card} has been assigned the value of 16")

                    else:
                        card[1] = trump
                        card[3] = 15
                        print(f"{card} has been assigned the value of 15 and is now considered a {card[1].lower()[:-1]}")

            else:
                continue

    return players

def play_trick(players: List[Union[Player, Bot]])-> List[List]:

    trick = []
    follow_suit = ''

    for player in players:
        print(f"\nIt is {player.name}'s turn.")
        #player selects a card
        if player.type == 'User':
            print(f"\nHere is {player.name}'s hand: ")

            for index, card in enumerate(player.hand):
                print(f"Card {index + 1}: {card}")

            play_card = int(input((f"\nWhich card would you like to play? (1-{len(player.hand)}): ")))
            trick.append(player.hand[play_card - 1])
            player.hand.pop(play_card - 1)
            print(f"\nThe trick is now {trick}")

            if player.order == 1:
                follow_suit = trick[0][1]

        #making the bots not stupid
        else:
           # time.sleep(2)

            if follow_suit == '': #if this is the first card played
                play_card = random.choice(player.hand) 
                print(f"\n{player.name} plays {play_card}.")  
                trick.append(play_card)
                player.hand.remove(play_card)
                print(f"\nHere is the current trick: {trick}")
                follow_suit = trick[0][1]

            else: #if there is a suit to follow
                
                can_follow = []

                #checks if they player has any of the follow suit
                for card in player.hand:
                    if card[1] == follow_suit:
                        can_follow.append(card)
                
                if can_follow:
                    play_card = random.choice(can_follow)
                else:
                    play_card = random.choice(player.hand)

                print(f"\n{player.name} plays {play_card}.")
                trick.append(play_card)
                player.hand.remove(play_card)
                print(f"\nHere is the current trick: {trick}")

    return trick, players, follow_suit

def score_trick(trump: str, follow_suit: str, trick: list, players: List[Union[Player, Bot]], team1_round_score: int, team2_round_score: int) -> int:
    #check trump cards
    trump_cards = []
    suited_cards = []
    winning_card = ['X', 'X', 'X', 0]
    winning_index = 0

    for card in trick: #add cards to two lists depending on if they followed suit or were trump
        if card[1] == trump:
            trump_cards.append(card)
        elif card[1] == follow_suit:
            suited_cards.append(card)
    
    if len(trump_cards) != 0: #if even 1 trump card was played, set as the winning card if higher than current winning card
        for card in trump_cards:
            if card[3] > winning_card[3]:
                winning_card = card
    else:
        for card in suited_cards: #if no trump cards were played, set follow suit cards as the winning cards
            if card[3] > winning_card[3]:
                winning_card = card
    
    winning_index = trick.index(winning_card)
    winning_player = players[winning_index]
    
    print(f"\n{winning_player.name} wins the trick for team {winning_player.team} with the card: {winning_card}.")
        
    if winning_player.team == 1:
        team1_round_score += 1
    else:
        team2_round_score += 1

    return team1_round_score, team2_round_score, winning_player

def rotate_players(players: List[Union[Player, Bot]], winning_player: Player)-> List[Union[User, Bot]]:
    

    players = sorted(players, key=attrgetter('order'))

    winning_index = players.index(winning_player)
    players = players[winning_index:] + players[:winning_index]

    for i, player in enumerate(players):
        player.order = i + 1

    players = sorted(players, key=attrgetter('order'))

    return players

def score_round(team1_round_score: int, team2_round_score: int, players: List[Union[Player, Bot]], team1_game_score: int, team2_game_score: int)-> List[int]:
    for player in players:
        if player.is_maker:
            maker_team = player.team
            player.is_maker = False

    if maker_team == 1:
        if 2 < team1_round_score < 5:
            team1_game_score += 1
            print(f"Team {maker_team} wins the round and receives 1 point. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")
        elif team1_round_score == 5:
            team1_game_score += 2
            print(f"Team {maker_team} wins the round and receives 2 points. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")
        else:
            team2_game_score += 2
            print(f"Team {maker_team} gets euchred. Team 2 receives 2 points. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")
    else:
        if 2 < team2_round_score < 5:
            team2_game_score += 1
            print(f"Team {maker_team} wins the round and receives 1 point. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")
        elif team2_round_score == 5:
            team2_game_score += 2
            print(f"Team {maker_team} wins the round and receives 2 points. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")
        else:
            team1_game_score += 2
            print(f"Team {maker_team} gets euchred. Team 1 receives 2 points. The score is now Team 1: {team1_game_score}, Team 2: {team2_game_score}.")

    return team1_game_score, team2_game_score

def end_game(team1_game_score: int, players: List[Union[Player, Bot]])->None:
    if team1_game_score >= 10:
        print(f"\n\nTeam 1 wins the game. The following players were on team 1: ")
        for player in players:
            if player.team == 1:
                print(f"{player.name}")
    else:
        print(f"\n\nTeam 2 wins the game. The following players were on team 2: ")
        for player in players:
            if player.team == 2:
                print(f"\n{player.name}")

    restart = input("\nWould the player like to play again (Y/N)?: ")
    if restart == 'Y':
        print("\nRestarting game....\n\n\n")
        return 'Y'

    elif restart == 'N':
        print(f"\nThanks for playing!")
        return('N')

    

    #for player in players:
    #if player.name == winning_player:

    #team1_round_score, team2_round_score, team1_game_score, team2_game_score