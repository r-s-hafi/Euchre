import sqlite3
from sqlite3 import Connection
from models import Player, Bot
from typing import List, Union
from operator import attrgetter
import random
import time

def deal_cards(connection: Connection, players: List[Union[Player, Bot]])-> List[Union[Player, Bot]]:
    for player in players:
        for int in range(1, 3):
            with connection:

                cur = connection.cursor()
                cur.execute(
                    '''
                    SELECT *
                    FROM deck 
                    ORDER BY RANDOM()
                    LIMIT 1;
                    ''')
                card = cur.fetchone()
                player.hand.append(card)

                cur.execute(
                '''
                DELETE FROM deck
                WHERE id = ?
                AND suit = ?
                AND symbol = ?
                AND value = ?
                ''', card)

        for int in range(1, 4):
            with connection:

                cur = connection.cursor()
                cur.execute(
                    '''
                    SELECT *
                    FROM deck 
                    ORDER BY RANDOM()
                    LIMIT 1;
                    ''')
                card = cur.fetchone()
                player.hand.append(card)

                cur.execute(
                '''
                DELETE FROM deck
                WHERE id = ?
                AND suit = ?
                AND symbol = ?
                AND value = ?
                ''', card)

    for player in players:
        # Convert each card in hand from tuple to list
        for i in range(len(player.hand)):
            player.hand[i] = list(player.hand[i])

        if player.order == 1:
            print(f"\nIt is {player.name}'s deal.")

        if player.type == 'User':
            print(f"{player.name.capitalize()}'s hand is made up of the following cards: ")
            for index, card in enumerate(player.hand):
                print(f"Card {index + 1}: {card}")
    
    for player in players: #reset player order to left of the dealer is now order #1, dealer is now order #4
        if player.order == 1:
            player.order = 4
        
        else:
            player.order -= 1

    players = sorted(players, key=attrgetter('order')) #sort players into new order - ensures that they play in the correct order, moving the dealer each time
        
    return players

def top_deck(connection: Connection)-> list:
    with connection:
        cur = connection.cursor()
        cur.execute(
                    '''
                    SELECT *
                    FROM deck 
                    ORDER BY RANDOM()
                    LIMIT 1;
                    ''')
        card = cur.fetchone()
        card = list(card)
        print(f"\nThe top card is flipped and it is {card}.")
        return card
    













                    

                
                

        