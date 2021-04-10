# CS Seminar Quarter Project: A Game of UNO
# Author: Sreyansh Mamidi
# Date: 3/14/2021

import random

# Allows the user to play UNO with the computer -- through the terminal!
class Uno:
    user_turn = True
    user_cards = []
    comp_cards = []
    discard_pile = []
    turns = 0
    current_card = list()
    user_won = False
    comp_won = False

    # Constructor for the Uno class
    def __init__(self, num_cards):
        self.cards_per_player = num_cards
    
    def __str__(self):
        intro = "Welcome to UNO in Python!\nDesigned by Sreyansh Mamidi\nHere, you can play UNO with your computer as long as you like! Enjoy!\n"
        return(intro)
    
    # Chooses a random color to be used by the computer
    def choose_random_color(self):
        colors = ["red ", "green", "blue", "yellow"]
        color = random.choice(colors)
        return(color)
    
    # Uses the standard numbers from 0 to 9
    # Considers a few special cards: reverse = "R", skip = "S", and +2 = "+2"
    # References some wild cards: wild = "W" and +4 = "+4"
    def draw_a_card(self):
        cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "R", "S", "+2", "W", "+4"]
        wild_cards = ["W", "+4"]

        card = random.choice(cards)
        color = self.choose_random_color()

        if card in wild_cards:
            return(card, "special")
        else:
            return(card, color)
    
    # Generates a set of random cards for each player
    def generate_cards(self):
        print("Generating cards...")

        for i in range(self.cards_per_player):
            self.user_cards.append(list(self.draw_a_card()))
            self.comp_cards.append(list(self.draw_a_card()))
        
        self.display_user_cards()
    
    # Begins the game, ensures that the game doesn't begin with a wild
    def begin_game(self):
        while True:
            first_card = list(self.draw_a_card())
            if first_card[0] not in ["S", "R", "+2", "W", "+4"]:
                self.current_card = first_card
                break

        print("Deciding who gets to play first...")
        user_input = input("Choose either the number 0 or 1: ")
        rand = random.randrange(0, 2)

        if int(user_input) == rand:
            print("Yay! You chose the right number!\nYou get to play first!")
        else:
            print("Unfortunately, you chose the wrong number\nThe computer plays first!")
            self.user_turn = False

        print("Let the game begin!")
    
    # Checks if a card is the same as the current card
    def check_if_cards_are_equal(self, card):
        are_equal = False

        if card[0] == self.current_card[0]:
            are_equal = True
        elif card[1] in self.current_card[1]:
            are_equal = True
        elif card[0] == "W" or card[0] == "+4":
            are_equal = True
        
        return(are_equal)
    
    # Outputs the user's cards to the terminal
    def display_user_cards(self):
        print("You have the following cards:")
        counter = 1

        for card in self.user_cards:
            output = "(" + str(counter) + ") " + str(card[1]) + "\t" + str(card[0])
            print(output)
            counter += 1
    
    # Allows a user to draw a card and displays a corresponding message
    def draw_user_card(self):
        new_card = list(self.draw_a_card())
        self.user_cards.append(new_card)
        print(f'You got a {new_card[1]} {new_card[0]} from the deck')
    
    # Defines the actions that occur when a user plays a card
    def place_card(self, card):
        self.current_card = card
        self.discard_pile.append(card)

        if self.user_turn:
            self.user_cards.remove(card)
        else:
            self.comp_cards.remove(card)
    
    # Represents the functionality for a reverse and skip card
    # In a 2 player game, reverse just keeps the same turn
    def play_reverse_or_skip(self, card):
        is_reverse_or_skip = False
        if card[0] == "R" or card[0] == "S":
            if self.user_turn and card[0] == "R":
                print("You have put a reverse, so it's your turn again!")

            elif not self.user_turn and card[0] == "R":
                print("The computer has put a reverse, so it's the computer's turn again!")

            elif self.user_turn and card[0] == "S":
                print("You have put a skip, so it's your turn again!")
            else:
                print("The computer has put a skip, so it's the computer's turn again!")
            
            is_reverse_or_skip = True           
        
        return(is_reverse_or_skip)
    
    # Defines the functionality for a +2 card
    def play_plus_two(self, card):
        is_plus_two = False

        if card[0] == "+2":
            if self.user_turn:
                print("You have put a +2, so the computer takes two cards!\nDrawing cards...")
                self.comp_cards.append(self.draw_a_card())
                self.comp_cards.append(self.draw_a_card())
            else:
                print("The computer has put a +2, so you take two cards!")
                self.draw_user_card()
                self.draw_user_card()
                self.display_user_cards()

            is_plus_two = True

        return(is_plus_two)

    # Represents the functionality for a WILD card
    def play_wild_card(self, card):
        is_wild = False

        if card[0] == "W":
            if self.user_turn:
                print("You have put a wild card, so you can change the needed color!")

                color = input("Which color would you like to choose? (red/blue/green/yellow) ")
                print(f'The computer must put a {color} card...')
                self.current_card[1] = color
            else:
                print("The computer has put a wild card, so it can change the needed color!")

                color = self.choose_random_color()
                print(f'You must put a {color} card...')
                self.current_card[1] = color
            
            is_wild = True
        
        return(is_wild)
    
    # Defines the functionality for a +4 card
    def play_plus_four(self, card):
        is_plus_four = False

        if card[0] == "+4":
            if self.user_turn:
                print("You have put a +4 card, so the computer draws four cards!\nDrawing cards...")
                for i in range(4):
                    self.comp_cards.append(list(self.draw_a_card()))

                color = input("Now, choose a color! (red/blue/green/yellow) ")
                print("Because you placed a +4, it's your turn once again!")
                self.current_card[1] = color
            else:
                print("The computer has put a +4 card, so you have to draw four cards!")
                for i in range(4):
                    self.draw_user_card()
 
                color = self.choose_random_color()
                self.current_card[1] = color

                print(f'Now, the computer would like to change the color to {color}')
                print("Because it's a +4 card, your turn is skipped :(")

                self.display_user_cards()
            
            is_plus_four = True
        
        return(is_plus_four)
    
    # Evaluates the effects of the special cards on the game's turns
    # Based on the computer's functionality
    def check_power_cards(self):
        reverse_skip = self.play_reverse_or_skip(self.current_card)
        plus_two = self.play_plus_two(self.current_card)

        wild_card = self.play_wild_card(self.current_card)
        plus_four = self.play_plus_four(self.current_card)

        if reverse_skip or plus_two:
            return(False)
        elif wild_card:
            return(True)
        elif plus_four:
            return(False)
        else:
            return(True)

    # Defines the set of actions performed during the computer's turn
    def play_turn_computer(self):
        self.turns += 1      
        equal = False

        for card in self.comp_cards:
            equal = self.check_if_cards_are_equal(card)
            if equal:
                print(f'The computer has put a {card[1]} {card[0]}')

                self.place_card(card)
                self.user_turn = self.check_power_cards()
                if len(self.comp_cards) == 0:
                    self.comp_won = True

                return(self.user_turn)
    
        if not equal:
            print("The computer decided to pass its turn.")
            self.comp_cards.append(list(self.draw_a_card()))
        
        if len(self.comp_cards) == 0:
            self.comp_won = True
        
        self.user_turn = True
        return(self.user_turn)

    # Defines the set of actions performed during the user's turn
    def play_turn_user(self):
        self.turns += 1
        self.display_user_cards()

        choice = input("Would you like to (1) play a card or (2) draw another card? Answer (1/2): ")
        if choice == "1":
            which_card = input("Using the numbers from 1 to " + str(len(self.user_cards)) + " choose which card you would like to play: ")
            chosen_card = self.user_cards[int(which_card) - 1]

            if self.check_if_cards_are_equal(chosen_card) == False:
                b = True
                while (b):
                    which_card = input("It wasn't a match! Please choose a different card, or type 0 to draw another card: ")
                    if which_card == "0":
                        self.draw_user_card()
                        b = False
                    else:
                        chosen_card = self.user_cards[int(which_card) - 1]
                        if self.check_if_cards_are_equal(chosen_card):
                            b = False
            
            print(f'You have put a {chosen_card[1]} {chosen_card[0]}')
            self.place_card(chosen_card)

            self.user_turn = not self.check_power_cards()
            if len(self.user_cards) == 0:
                self.user_won = True
            return(self.user_turn)

        else:
            self.draw_user_card()
           
        if len(self.user_cards) == 0:
            self.user_won = True
        
        self.user_turn = False
        return(self.user_turn)

    # Documents the process of playing the game
    def play_game(self):
        b = True

        while b:
            if self.turns == 0:
                self.begin_game()

            if self.user_won or self.comp_won:
                break
            
            if self.current_card[0] not in ["W", "+4"]:
                print(f'The current card is a {self.current_card[1]} {self.current_card[0]}')
            else:
                print(f'The current color is {self.current_card[1]}')
           
            if self.user_turn:
                a = self.play_turn_user()
            else:
                print("Now, it's the computer's turn!")
                a = self.play_turn_computer()
                       
        print("However, the game is actually over!")
        print(f'This fierce battle consisted of {self.turns} turn(s), causing {len(self.discard_pile)} card(s) to enter the discard pile')
        if self.user_won:
            print("But, at the end of the day...\nYou won! Congrats!")
        else:
            print("But, at the end of the day...\nThe computer won! Better luck next time :)")
        
        print("Thank you for playing!")

def main():
    # Creates an UNO game with 7 cards, this can be changed!
    uno = Uno(7)
    print(uno)
    uno.generate_cards()
    uno.play_game()

if __name__ == "__main__":
    main()
