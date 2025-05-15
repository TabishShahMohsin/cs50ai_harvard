from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a Knave."
knowledge0 = And(
    Or(
        And(And(AKnight, AKnave), AKnight),
        And(Not(And(AKnight, AKnave)), AKnave)
    ),
    Or(
        And(AKnight, Not(AKnave)),
        And(AKnave, Not(AKnight))
    )
)

# Puzzle 1
# A says "We are both Knave."
# B says nothing.
knowledge1 = And(
    Or(
        And(And(AKnave, BKnave), AKnight),
        And(Not(And(AKnave, BKnave)), AKnave)
    ),
    Or(
        And(AKnight, Not(AKnave)),
        And(AKnave, Not(AKnight))
    ),
    Or(
        And(BKnight, Not(BKnave)),
        And(BKnave, Not(BKnight))
    )
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(
        And(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
        And(Not(Or(And(AKnave, BKnave), And(AKnight, BKnight))), AKnave)
    ),
    Or(
        And(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight),
        And(Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))), BKnave)
    ),
    Or(
        And(AKnight, Not(AKnave)),
        And(AKnave, Not(AKnight))
    ),
    Or(
        And(BKnight, Not(BKnave)),
        And(BKnave, Not(BKnight))
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a Knave.", but you don't know which.
# B says "A said 'I am a Knave'."
# B says "C is a Knave."
# C says "A is a knight."
knowledge3 = And(
    Or(
        And(Or(AKnight, AKnave), AKnight),
        And(Not(Or(AKnave, AKnight)), AKnave)
    ),
    Or(
        And(Or(And(AKnave, AKnight), And(AKnight, AKnave)), BKnight),
        And(Not(Or(And(AKnave, AKnight), And(AKnight, AKnave))), BKnave)
    ),
    Or(
        And(CKnave, BKnight),
        And(Not(CKnave), BKnave)
    ),
    Or(
        And(AKnight, CKnight),
        And(Not(AKnight), CKnave)
    ),
    Or(
        And(AKnight, Not(AKnave)),
        And(AKnave, Not(AKnight))
    ),
    Or(
        And(BKnight, Not(BKnave)),
        And(BKnave, Not(BKnight))
    ),
    Or(
        And(CKnight, Not(CKnave)),
        And(AKnave, Not(AKnight))
    ),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
