#!/usr/bin/env python3
"""
Blackjack - A command line casino game
Author: nockpoterson
"""

import random
import os
import json
from typing import List, Tuple

# Card suits and ranks
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def value(self) -> int:
        """Return the value of the card"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Will handle as 1 or 11 in hand calculation
        else:
            return int(self.rank)

class Deck:
    def __init__(self, num_decks: int = 1):
        self.cards: List[Card] = []
        self.num_decks = num_decks
        self.reset()
    
    def reset(self):
        """Reset and shuffle the deck"""
        self.cards = []
        for _ in range(self.num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        """Deal a card from the deck"""
        if len(self.cards) < 10:
            print("Reshuffling deck...")
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
        self.bet = 0
    
    def add_card(self, card: Card):
        """Add a card to the hand"""
        self.cards.append(card)
    
    def calculate_value(self) -> int:
        """Calculate the total value of the hand"""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                value += 11
            else:
                value += card.value()
        
        # Adjust for aces
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self) -> bool:
        """Check if hand is a blackjack"""
        return len(self.cards) == 2 and self.calculate_value() == 21
    
    def is_busted(self) -> bool:
        """Check if hand is busted"""
        return self.calculate_value() > 21
    
    def __str__(self):
        cards_str = ' '.join([str(card) for card in self.cards])
        return f"{cards_str} (Value: {self.calculate_value()})"

class Player:
    def __init__(self, name: str = "Player", bankroll: int = 1000):
        self.name = name
        self.bankroll = bankroll
        self.hand = Hand()
        self.stats = {"wins": 0, "losses": 0, "pushes": 0, "blackjacks": 0}
    
    def place_bet(self, amount: int) -> bool:
        """Place a bet, returns True if successful"""
        if amount > self.bankroll:
            print(f"Insufficient funds! You have ${self.bankroll}")
            return False
        if amount <= 0:
            print("Bet must be positive!")
            return False
        self.hand.bet = amount
        self.bankroll -= amount
        return True
    
    def win(self, amount: int = None):
        """Player wins the hand"""
        if amount is None:
            amount = self.hand.bet * 2
        self.bankroll += amount
        self.stats["wins"] += 1
        if self.hand.is_blackjack():
            self.stats["blackjacks"] += 1
    
    def lose(self):
        """Player loses the hand"""
        self.stats["losses"] += 1
    
    def push(self):
        """Push - return the bet"""
        self.bankroll += self.hand.bet
        self.stats["pushes"] += 1
    
    def reset_hand(self):
        """Reset hand for new round"""
        self.hand = Hand()
    
    def display_stats(self):
        """Display player statistics"""
        total_games = sum(self.stats.values()) - self.stats["blackjacks"]
        if total_games > 0:
            win_rate = (self.stats["wins"] / total_games) * 100
        else:
            win_rate = 0
        
        print(f"\n{'='*40}")
        print(f"📊 {self.name}'s Statistics")
        print(f"{'='*40}")
        print(f"Bankroll: ${self.bankroll}")
        print(f"Wins: {self.stats['wins']}")
        print(f"Losses: {self.stats['losses']}")
        print(f"Pushes: {self.stats['pushes']}")
        print(f"Blackjacks: {self.stats['blackjacks']}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"{'='*40}\n")

class BlackjackGame:
    def __init__(self):
        self.deck = Deck(num_decks=2)
        self.player = Player()
        self.dealer_hand = Hand()
        self.load_stats()
    
    def load_stats(self):
        """Load player stats from file"""
        if os.path.exists('blackjack_stats.json'):
            try:
                with open('blackjack_stats.json', 'r') as f:
                    data = json.load(f)
                    self.player.stats = data.get('stats', self.player.stats)
                    self.player.bankroll = data.get('bankroll', 1000)
            except:
                pass
    
    def save_stats(self):
        """Save player stats to file"""
        data = {
            'stats': self.player.stats,
            'bankroll': self.player.bankroll
        }
        with open('blackjack_stats.json', 'w') as f:
            json.dump(data, f)
    
    def display_table(self, show_dealer_full: bool = False):
        """Display the current table state"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*50)
        print("🎰 BLACKJACK 🎰".center(50))
        print("="*50)
        
        print(f"\n💰 Your Bankroll: ${self.player.bankroll}")
        print(f"💵 Current Bet: ${self.player.hand.bet}")
        
        print(f"\n{'='*50}")
        print("DEALER'S HAND:")
        if show_dealer_full:
            print(f"  {self.dealer_hand}")
            if self.dealer_hand.is_blackjack():
                print("  🎲 BLACKJACK!")
        else:
            # Hide dealer's hole card
            print(f"  {self.dealer_hand.cards[0]} [?] (Value: ?)")
        
        print(f"\n{'='*50}")
        print("YOUR HAND:")
        print(f"  {self.player.hand}")
        if self.player.hand.is_blackjack():
            print("  🎲 BLACKJACK!")
        elif self.player.hand.is_busted():
            print("  💥 BUSTED!")
        
        print(f"{'='*50}\n")
    
    def get_bet(self) -> int:
        """Get bet amount from player"""
        while True:
            try:
                bet = input(f"Place your bet (1-{self.player.bankroll}, or 'q' to quit): $")
                if bet.lower() == 'q':
                    return -1
                bet = int(bet)
                if self.player.place_bet(bet):
                    return bet
            except ValueError:
                print("Please enter a valid number!")
    
    def player_turn(self) -> bool:
        """Player's turn, returns True if player hasn't busted"""
        while True:
            self.display_table()
            
            if self.player.hand.is_busted():
                return False
            
            if self.player.hand.calculate_value() == 21:
                return True
            
            print("Options:")
            print("  [h] Hit")
            print("  [s] Stand")
            if len(self.player.hand.cards) == 2 and self.player.bankroll >= self.player.hand.bet:
                print("  [d] Double Down")
            print("  [q] Quit")
            
            choice = input("\nYour choice: ").lower()
            
            if choice == 'h':
                card = self.deck.deal()
                self.player.hand.add_card(card)
                print(f"You drew: {card}")
            elif choice == 's':
                return True
            elif choice == 'd' and len(self.player.hand.cards) == 2 and self.player.bankroll >= self.player.hand.bet:
                # Double down
                self.player.bankroll -= self.player.hand.bet
                self.player.hand.bet *= 2
                card = self.deck.deal()
                self.player.hand.add_card(card)
                print(f"You doubled down and drew: {card}")
                return not self.player.hand.is_busted()
            elif choice == 'q':
                return -1
            else:
                print("Invalid choice!")
    
    def dealer_turn(self):
        """Dealer's turn - hits on 16, stands on 17"""
        print("\nDealer's turn...")
        input("Press Enter to continue...")
        
        while self.dealer_hand.calculate_value() < 17:
            card = self.deck.deal()
            self.dealer_hand.add_card(card)
            self.display_table(show_dealer_full=True)
            print(f"Dealer drew: {card}")
            input("Press Enter to continue...")
    
    def determine_winner(self):
        """Determine the winner and pay out"""
        player_value = self.player.hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()
        
        self.display_table(show_dealer_full=True)
        
        print("\n" + "="*50)
        
        # Check for blackjacks
        if self.player.hand.is_blackjack() and self.dealer_hand.is_blackjack():
            print("🤝 Both have Blackjack! PUSH!")
            self.player.push()
        elif self.player.hand.is_blackjack():
            blackjack_payout = int(self.player.hand.bet * 2.5)
            print(f"🎉 BLACKJACK! You win ${blackjack_payout - self.player.hand.bet}!")
            self.player.win(blackjack_payout)
        elif self.dealer_hand.is_blackjack():
            print("😞 Dealer has Blackjack! You lose!")
            self.player.lose()
        # Check for busts
        elif self.player.hand.is_busted():
            print("💥 You busted! Dealer wins!")
            self.player.lose()
        elif self.dealer_hand.is_busted():
            win_amount = self.player.hand.bet * 2
            print(f"🎉 Dealer busted! You win ${self.player.hand.bet}!")
            self.player.win(win_amount)
        # Compare hands
        elif player_value > dealer_value:
            win_amount = self.player.hand.bet * 2
            print(f"🎉 You win ${self.player.hand.bet}! ({player_value} vs {dealer_value})")
            self.player.win(win_amount)
        elif dealer_value > player_value:
            print(f"😞 Dealer wins! ({dealer_value} vs {player_value})")
            self.player.lose()
        else:
            print(f"🤝 Push! It's a tie at {player_value}")
            self.player.push()
        
        print("="*50 + "\n")
        input("Press Enter to continue...")
    
    def play_round(self) -> bool:
        """Play one round, returns False if player wants to quit"""
        # Reset hands
        self.player.reset_hand()
        self.dealer_hand = Hand()
        
        # Get bet
        bet = self.get_bet()
        if bet == -1:
            return False
        
        # Deal initial cards
        self.player.hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player.hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        # Check for immediate blackjacks
        if self.player.hand.is_blackjack() or self.dealer_hand.is_blackjack():
            self.determine_winner()
            return True
        
        # Player turn
        result = self.player_turn()
        if result == -1:
            return False
        if not result:  # Player busted
            self.determine_winner()
            return True
        
        # Dealer turn
        self.dealer_turn()
        
        # Determine winner
        self.determine_winner()
        
        return True
    
    def run(self):
        """Main game loop"""
        print("\n" + "="*50)
        print("Welcome to Blackjack!".center(50))
        print("="*50)
        print("\nRules:")
        print("- Try to get closer to 21 than the dealer")
        print("- Dealer hits on 16, stands on 17")
        print("- Blackjack pays 3:2")
        print("- Type 'q' to quit anytime\n")
        
        while self.player.bankroll > 0:
            if not self.play_round():
                break
            
            # Save stats after each round
            self.save_stats()
            
            if self.player.bankroll <= 0:
                print("\n💸 You're broke! Game over!")
                break
        
        # Show final stats
        self.player.display_stats()
        self.save_stats()
        print("\nThanks for playing! 👋\n")

if __name__ == "__main__":
    game = BlackjackGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Saving stats...")
        game.save_stats()
        game.player.display_stats()
