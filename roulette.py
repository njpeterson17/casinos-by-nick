#!/usr/bin/env python3
"""
Roulette - A command line casino game
Author: nockpoterson
"""

import random
import os
import json
from typing import List, Dict, Tuple

class RouletteGame:
    def __init__(self):
        self.bankroll = 1000
        self.wheel_numbers = [
            0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
        ]
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.current_bets: List[Dict] = []
        self.load_stats()
    
    def get_number_color(self, num: int) -> str:
        """Get the color of a number"""
        if num == 0:
            return "green"
        return "red" if num in self.red_numbers else "black"
    
    def load_stats(self):
        """Load player stats from file"""
        if os.path.exists('roulette_stats.json'):
            try:
                with open('roulette_stats.json', 'r') as f:
                    data = json.load(f)
                    self.bankroll = data.get('bankroll', 1000)
            except:
                pass
    
    def save_stats(self):
        """Save player stats to file"""
        data = {'bankroll': self.bankroll}
        with open('roulette_stats.json', 'w') as f:
            json.dump(data, f)
    
    def display_table(self):
        """Display the roulette table"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*60)
        print("🎰 ROULETTE 🎲".center(60))
        print("="*60)
        print(f"\n💰 Bankroll: ${self.bankroll}")
        
        total_bet = sum(bet['amount'] for bet in self.current_bets)
        print(f"💵 Current Bets: ${total_bet}")
        
        if self.current_bets:
            print(f"\n{'='*60}")
            print("YOUR BETS:")
            for i, bet in enumerate(self.current_bets, 1):
                print(f"  {i}. ${bet['amount']} on {bet['type'].upper()}")
        
        print(f"\n{'='*60}")
        print("BETTING OPTIONS:")
        print("  [1] Red         (2:1)    [2] Black       (2:1)")
        print("  [3] Even        (2:1)    [4] Odd         (2:1)")
        print("  [5] High (19-36) (2:1)   [6] Low (1-18)  (2:1)")
        print("  [7] 1st Dozen   (3:1)    [8] 2nd Dozen   (3:1)")
        print("  [9] 3rd Dozen   (3:1)    [0] Zero        (36:1)")
        print(f"{'='*60}\n")
    
    def get_bet_type(self, choice: str) -> str:
        """Convert menu choice to bet type"""
        bet_types = {
            '1': 'red',
            '2': 'black',
            '3': 'even',
            '4': 'odd',
            '5': 'high',
            '6': 'low',
            '7': '1-12',
            '8': '13-24',
            '9': '25-36',
            '0': 'zero'
        }
        return bet_types.get(choice)
    
    def place_bet(self) -> bool:
        """Place a bet"""
        print("\nSelect bet type (0-9) or 's' to spin, 'c' to clear bets:")
        choice = input("> ").lower()
        
        if choice == 's':
            return False  # Ready to spin
        
        if choice == 'c':
            # Clear all bets
            for bet in self.current_bets:
                self.bankroll += bet['amount']
            self.current_bets = []
            print("Bets cleared!")
            input("Press Enter to continue...")
            return True
        
        bet_type = self.get_bet_type(choice)
        if not bet_type:
            print("Invalid choice!")
            input("Press Enter to continue...")
            return True
        
        try:
            amount = int(input(f"Bet amount (max ${self.bankroll}): $"))
            if amount > self.bankroll:
                print("Insufficient funds!")
                input("Press Enter to continue...")
                return True
            if amount < 1:
                print("Minimum bet is $1!")
                input("Press Enter to continue...")
                return True
            
            self.bankroll -= amount
            self.current_bets.append({'type': bet_type, 'amount': amount})
            print(f"Bet ${amount} on {bet_type.upper()}")
            input("Press Enter to continue...")
        except ValueError:
            print("Invalid amount!")
            input("Press Enter to continue...")
        
        return True
    
    def check_win(self, number: int, bet: Dict) -> int:
        """Check if a bet wins and return payout multiplier"""
        bet_type = bet['type']
        color = self.get_number_color(number)
        
        if bet_type == 'red':
            return 2 if color == 'red' else 0
        elif bet_type == 'black':
            return 2 if color == 'black' else 0
        elif bet_type == 'zero':
            return 36 if number == 0 else 0
        elif bet_type == 'even':
            return 2 if number != 0 and number % 2 == 0 else 0
        elif bet_type == 'odd':
            return 2 if number % 2 == 1 else 0
        elif bet_type == 'high':
            return 2 if number >= 19 else 0
        elif bet_type == 'low':
            return 2 if 1 <= number <= 18 else 0
        elif bet_type == '1-12':
            return 3 if 1 <= number <= 12 else 0
        elif bet_type == '13-24':
            return 3 if 13 <= number <= 24 else 0
        elif bet_type == '25-36':
            return 3 if 25 <= number <= 36 else 0
        
        return 0
    
    def spin(self):
        """Spin the wheel"""
        if not self.current_bets:
            print("No bets placed!")
            input("Press Enter to continue...")
            return
        
        self.display_table()
        print("\n🎲 Spinning the wheel...")
        input("Press Enter to spin...")
        
        # Simulate spinning
        for _ in range(3):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "="*60)
            print("🎰 ROULETTE 🎲".center(60))
            print("="*60)
            print("\n🎲 Spinning...")
            temp_num = random.choice(self.wheel_numbers)
            print(f"  -> {temp_num} {self.get_number_color(temp_num).upper()}")
            import time
            time.sleep(0.3)
        
        # Final result
        result = random.choice(self.wheel_numbers)
        color = self.get_number_color(result)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*60)
        print("🎰 ROULETTE 🎲".center(60))
        print("="*60)
        print(f"\n🎯 RESULT: {result} {color.upper()}!")
        print(f"{'='*60}")
        
        # Calculate winnings
        total_win = 0
        win_details = []
        
        for bet in self.current_bets:
            multiplier = self.check_win(result, bet)
            if multiplier > 0:
                win_amount = bet['amount'] * multiplier
                total_win += win_amount
                win_details.append(f"  ✓ ${bet['amount']} on {bet['type'].upper()} → ${win_amount}")
        
        if total_win > 0:
            print("\n🎉 WINNING BETS:")
            for detail in win_details:
                print(detail)
            print(f"\n💰 Total Win: ${total_win}")
            self.bankroll += total_win
        else:
            print("\n😞 No winning bets this round.")
        
        print(f"{'='*60}")
        print(f"New Bankroll: ${self.bankroll}")
        
        # Reset bets
        self.current_bets = []
        self.save_stats()
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main game loop"""
        print("\n" + "="*60)
        print("Welcome to Roulette!".center(60))
        print("="*60)
        print("\nRules:")
        print("- Place bets on Red, Black, Even, Odd, High/Low, Dozens")
        print("- Red/Black/Even/Odd/High/Low pay 2:1")
        print("- Dozens pay 3:1")
        print("- Zero pays 36:1")
        print("\nType 's' to spin, 'c' to clear bets, 'q' to quit\n")
        input("Press Enter to start...")
        
        while self.bankroll > 0:
            self.display_table()
            
            if not self.place_bet():
                # User chose to spin
                self.spin()
            
            if self.bankroll <= 0:
                print("\n💸 You're broke! Game over!")
                input("Press Enter to exit...")
                break
        
        print(f"\nFinal Bankroll: ${self.bankroll}")
        self.save_stats()
        print("\nThanks for playing! 👋\n")

if __name__ == "__main__":
    game = RouletteGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Saving stats...")
        game.save_stats()
        print(f"Final Bankroll: ${game.bankroll}")