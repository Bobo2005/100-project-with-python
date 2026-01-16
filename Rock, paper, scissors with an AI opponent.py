import random
choices = ["rock","paper","scissors"]
history = []

def ai_move():
    if not history: return random.choice(choices)
    # Count player choices
    counts = {c: history.count(c) for c in choices}
    common = max(counts, key=counts.get)
    # Counter the player's most common move
    counter = {"rock":"paper","paper":"scissors","scissors":"rock"}
    return counter[common]

def winner(p, a):
    if p == a: return "draw"
    wins = {("rock","scissors"),("paper","rock"),("scissors","paper")}
    return "player" if (p,a) in wins else "ai"

if __name__ == "__main__":
    while True:
        p = input("rock/paper/scissors (or 'quit'): ").strip().lower()
        if p == "quit": break
        if p not in choices: print("Invalid"); continue
        a = ai_move()
        history.append(p)
        print(f"AI: {a} → {winner(p,a)}")

