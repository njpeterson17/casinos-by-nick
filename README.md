# Casinos by Nick 🎰

A collection of casino games playable in your browser or command line.

## Games

### 🃏 Blackjack
Classic 21 game against the dealer.

**Features:**
- Bet, hit, stand, double down
- Persistent stats and bankroll
- Dealer follows casino rules (hits 16, stands 17)
- Blackjack pays 3:2

### 🎲 Roulette
European roulette with multiple betting options.

**Features:**
- Bet on Red, Black, Even, Odd, High/Low, Dozens, or Zero
- Animated spinning wheel
- Various payout odds (2:1, 3:1, 36:1)
- Multiple bets per spin

## How to Play

### Web Browser (Recommended)
1. Visit: https://njpeterson17.github.io/casinos-by-nick
2. Click on **Blackjack** or **Roulette**
3. Start playing!

### Local - Web Version
```bash
git clone https://github.com/njpeterson17/casinos-by-nick.git
cd casinos-by-nick
python3 -m http.server 8000
# Open http://localhost:8000
```

### Local - Command Line
```bash
# Blackjack (CLI)
python3 blackjack.py

# Roulette (CLI)
python3 roulette.py
```

## Game Controls

### Blackjack
- `h` - Hit
- `s` - Stand
- `d` - Double Down
- `q` - Quit

### Roulette
- `1-9` - Select bet type
- `0` - Bet on Zero
- `s` - Spin the wheel
- `c` - Clear all bets
- `q` - Quit

## Technologies
- Pure HTML/CSS/JavaScript (browser games)
- Python 3.6+ (CLI versions)
- No external dependencies!

## License
MIT License - Feel free to use, modify, and distribute!

---

*Remember: The house always wins... eventually.* 🎰