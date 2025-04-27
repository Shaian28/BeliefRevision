# Import all necessary libraries
import numpy as np
from Proposition import Proposition

# Get the CNF form of the proposition
# https://en.wikipedia.org/wiki/Conjunctive_normal_form#Conversion_by_semantic_means
def convert_to_CNF(proposition):
    # Make a truth table for the proposition
    proposition.truth_table()
    sentence = ""

    # Go through all the rows in the truth table
    for idxRow in range(0, len(proposition.TruthTable)):
        # Find a false result in the row
        if not proposition.TruthTable["Result"][idxRow]:
            # Join the existing string with an AND
            if sentence != "":
                sentence += " and "
            row = proposition.TruthTable.iloc[idxRow]
            clause = []
            # Find out if the symbolic values in the row is 1 or 0
            for symbol, value in zip(proposition.symbolic, row[:-1]):
                if value:
                    clause.append(f"not {symbol}")
                else:
                    clause.append(str(symbol))
            # Complete the sentence
            sentence += "(" + " or ".join(clause) + ")"
    # Turn the sentence into a proposition
    CNF = Proposition(sentence)

    # Return the CNF form
    return CNF
    

# Give the resolution alghorithm
def resolution(CNF, complement):
    clauses = str(CNF).split("∧")
    clauses.append(str(complement))
    print(clauses)

# Debugging
if __name__ == "__main__":
    logic = Proposition("R iff P or S")
    complement = Proposition("not P")
    logic.truth_table()
    CNF = convert_to_CNF(logic)
    resolution(CNF, complement)

    