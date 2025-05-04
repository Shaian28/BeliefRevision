# Import all necessary libraries
from Proposition import Proposition
import numpy as np
import sympy as sp

# Get the CNF form of the proposition
# https://en.wikipedia.org/wiki/Conjunctive_normal_form#Conversion_by_semantic_means
def convert_to_CNF(proposition):
    # Make the proposition symbolic
    proposition.symbolic_form()
    # Store the symbols in a dictionary
    local_sym = {str(sym): sym for sym in proposition.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    # Parse the expression
    expr = sp.parsing.sympy_parser.parse_expr(proposition.expression, local_dict = local_sym, evaluate = False)
    # Turn the statement into CNF and make it a readable string
    sentence = str(sp.to_cnf(expr))
    sentence = sentence.replace("~", "not ")
    sentence = sentence.replace("|", "or")
    sentence = sentence.replace("&", "and")
    # Make sure to note include tautologies
    CNF = Proposition(sentence) if len(sentence) > 0 else None
    if CNF is None:
        print(f"The statement {proposition} is a tautology")

    # Return the CNF form
    return CNF

# Find the complementary pair of clauses for the resolution algorithm
def find_complementary_pair(clauses):
    # Initiate the new clauses list
    newClauses = []
    # Go through all the clauses
    for idx1, claus1 in enumerate(clauses):
        claus1String = claus1.premise
        for idx2, claus2 in enumerate(clauses):
            claus2String = claus2.premise
            # Skipping the same clauses and clauses, that we should be cautious of
            if claus1String == claus2String:
                continue
            # Compare the different clauses tokens
            for token in claus1.tokens:
                # Skip the elements, that doesn't have a negation
                idxToken = claus1.order.index(token) if token in claus1.order else -1
                check = claus1.order[idxToken - 1].upper() == "NOT" if idxToken > 0 else False
                if check:
                    continue
                idxList = []
                # Go through all the tokens and operations in the second clause
                for idx, order in enumerate(claus2.order):
                    # Check if the two clauses are the same, but with a negation in one of the tokens
                    check = claus2.order[idx - 1].upper() == "NOT" if idx > 0 else False
                    if token == order and check:
                        # Reassemble the clause
                        claus1List = claus1String.upper().split(" OR ")
                        claus2List = claus2String.upper().split(" OR ")
                        addClaus = claus1List.copy() if np.argmax([len(claus1List), len(claus2List)]) == 0 else claus2List.copy()
                        compareClaus = claus2List.copy() if np.argmax([len(claus1List), len(claus2List)]) == 0 else claus1List.copy()
                        idxList = []
                        # Find the complementary pair of the token
                        for idxElem, elem1 in enumerate(addClaus):
                            for elem2 in compareClaus:
                                if (elem1 in elem2 or elem2 in elem1) and (elem1.upper()[0:4] == "NOT ") != (elem2.upper()[0:4]  == "NOT "):
                                    idxList.append(idxElem)
                        # Delete the tokens with a complementary pair
                        for idxEl in reversed(idxList):
                            del addClaus[idxEl]
                        # There is an entailment if the resulting clauses lead to an empty clause
                        if len(addClaus) == 0:
                            # Return the new clauses when the entail is not found
                            return [clauses.index(claus1), clauses.index(claus2)], True
                        # Add the new clause
                        else:
                            newClauses.append(Proposition(" OR ".join(addClaus)))
                        # Breaking the loop to continue to the next order
                        if len(idxList) > 0:
                            break
                # Breaking the loop to continue to the next token or completely go out of the loop
                if len(idxList):
                    break
    
    # Return the new clauses when the entail is not found
    return newClauses, False

# Give the resolution alghorithm
def resolution(KB, phi, write = False):
    # Convert to CNF
    KBCNF = convert_to_CNF(KB)

    # Simplifying the complement of phi
    phiString = phi.premise
    notPhi = Proposition("not " + phiString if len(phiString) == 1 else "not (" + phiString + ")")
    phiCNF = convert_to_CNF(notPhi)

    # Get the clauses from knowledge base
    if KBCNF is not None:
        clauses = (KBCNF.premise).upper().split(" AND ")
    else:
        clauses = []
    # Get the clauses from inference
    if phiCNF is not None:
        clauses.extend((phiCNF.premise).upper().split(" AND "))
    clauses = [Proposition(claus) for claus in clauses]

    # Logical statement for entailment
    entail = False
    notEntail = False

    # Go though the loop until entailment is certain
    while not entail and not notEntail:
        # Find the complementary pair of clauses
        newClauses, entail = find_complementary_pair(clauses)
        # If the entailment is not found, add the new clauses to the KB
        if not entail:
            # Remember the clauses from before
            oldClausString = [claus.premise for claus in clauses]
            # Go through all the new clauses
            for newClaus in newClauses:
                clausString = [claus.premise for claus in clauses]
                # Add the new clause if it isn't present
                if newClaus.premise not in clausString:
                    clauses.append(newClaus)
            # Remember the clauses now
            newClausString = [claus.premise for claus in clauses]
            # There is not an entailment if no clauses was added
            if oldClausString == newClausString:
                notEntail = True
    
    # Print the result
    if write:
        print(f"KB = {KB}")
        print(f"φ = {phi}")
    # There is entailment
    if entail:
        if write:
            print(f"{KB} ⊨ {phi}")
            print("KB does entail the result")

        # Return a truth value
        return True
    # There is no entailment
    else:
        if write:
            print(f"{KB} ⊭ {phi}")
            print("KB does not entail the result")

        # Return a false value
        return False

# Example
if __name__ == "__main__":
    logic = Proposition("R iff (P or S)")
    inference = Proposition("not P")
    print(resolution(logic, inference, True))
