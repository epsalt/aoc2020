from copy import deepcopy
from itertools import count, groupby
import sys

with open("input.txt") as f:
    lines = f.read().splitlines()
    players = [list(group) for k, group in groupby(lines, bool) if k]

    decks = {}
    for player in players:
        name = player.pop(0)
        deck = [int(n) for n in player]
        decks[name] = deck


def combat(decks):
    if not all(decks.values()):
        for player, deck in decks.items():
            if deck:
                return player, deck

    player1, player2 = decks.keys()
    card1 = decks[player1].pop(0)
    card2 = decks[player2].pop(0)

    if card1 > card2:
        decks[player1] += [card1, card2]
    else:
        decks[player2] += [card2, card1]

    return combat(decks)


def recursive_combat(decks, mem=None):
    player1, player2 = decks.keys()

    if mem is None:
        mem = []

    if str(decks) in mem:
        return player1, decks[player1]
    else:
        mem.append(str(decks))

    if not all(decks.values()):
        for player, deck in decks.items():
            if deck:
                return player, deck

    card1 = decks[player1].pop(0)
    card2 = decks[player2].pop(0)
    winner = player1 if card1 > card2 else player2

    if card1 <= len(decks[player1]) and card2 <= len(decks[player2]):
        subdecks = {
            player: decks[player][:card]
            for player, card in ((player1, card1), (player2, card2))
        }
        winner, _ = recursive_combat(subdecks)

    if winner == player1:
        decks[player1] += [card1, card2]
    else:
        decks[player2] += [card2, card1]

    return recursive_combat(decks, mem)


def score(deck):
    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def part1(decks):
    _decks = deepcopy(decks)
    winner, deck = combat(_decks)
    return score(deck)


def part2(decks):
    sys.setrecursionlimit(10**6)
    _decks = deepcopy(decks)
    winner, deck = recursive_combat(_decks)
    return score(deck)

