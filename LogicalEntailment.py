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
def resolution(proposition, complement):
    # Convert to CNF
    CNF = convert_to_CNF(proposition)

    # Get the clauses from CNF
    clauses = (" ".join(CNF.order)).split(" and ")
    clauses.append(" ".join(complement.order))
    clauses = [Proposition(claus) for claus in clauses]
    newClauses = []

    # Logical statement for entailment
    entail = False
    notEntail = False

    # Go though the loop until entailment is certain
    while not entail and not notEntail:
        # Go through all the clauses
        for claus1 in clauses:
            claus1String = " ".join(claus1.order)
            for claus2 in clauses:
                claus2String = " ".join(claus2.order)
                # Compare the different clauses tokens
                for token in claus1.tokens:
                    for idx, order in enumerate(claus2.order):
                        if idx > 0 and claus1String != claus2String:
                            # Check if the two clauses are the same, but with a negation in one of te tokens
                            if token == order and claus2.order[idx - 1].upper() == "NOT":
                                # Reassemble the clause
                                claus1List = claus1String.split(" or ")
                                claus2List = claus2String.split(" or ")
                                idxList = []
                                # Find the complementary pair of the token
                                for idxElem, elem1 in enumerate(claus1List):
                                    for elem2 in claus2List:
                                        if elem1 in elem2 and not (elem1.upper().startswith("NOT ") == elem2.upper().startswith("NOT ")):
                                            idxList.append(idxElem)
                                # Delete the tokens with a complementary pair
                                for idxEl in reversed(idxList):
                                    del claus1List[idxEl]
                                # There is an entailment if the resulting clauses lead to an empty clause
                                if len(claus1List) == 0:
                                    entail = True
                                # Add the new clause
                                else:
                                    newClauses.append(Proposition(" and ".join(claus1List)))
        
        # Remember the clauses from before
        oldClausString = [" ".join(claus.order) for claus in clauses]
        # Go through all the new clauses
        for newClaus in newClauses:
            clausString = [" ".join(claus.order) for claus in clauses]
            # Add the new clause if it isn't present
            if " ".join(newClaus.order) not in clausString:
                clauses.append(newClaus)
        # Remember the clauses now
        newClausString = [" ".join(claus.order) for claus in clauses]
        # There is not an entailment if no clauses was added
        if oldClausString == newClausString:
            notEntail = True
            entail = False
    
    # Print the result
    result = " ".join(complement.order)
    result = result.upper().removeprefix("NOT ") if result.upper().startswith("NOT ") else result
    print(f"KB = {proposition}")
    print(f"φ = {result}")
    # There is entailment
    if entail:
        print(f"{proposition} ⊨ {result}")
        print("KB does entail the result")
    # There is no entailment
    else:
        print(f"{proposition} ⊭ {result}")
        print("KB does not entail the result")
                                


# Debugging
if __name__ == "__main__":
    logic = Proposition("R iff P or S")
    complement = Proposition("P")
    resolution(logic, complement)
    