# Import all necessary libraries
import numpy as np
from Proposition import Proposition

# Change all instance of an operation
def change_token(prop, tokenOld, tokenNew):
    tokenOld = Proposition(tokenOld)
    # Go deeper if a nested token exist
    if hasattr(prop, 'nestedToken'):
        for idx, token in list(prop.nestedToken.items()):
            prop.nestedToken[idx] = change_token(token, " ".join(tokenOld.order), tokenNew)
        prop.update_nestedToken()
    
    # Find the structure used for the old token
    sequence = []
    idxProp = 0
    while idxProp < len(prop.operations):
        if prop.operations[idxProp].upper() == tokenOld.operations[0].upper():
            idx0 = idxProp
            while idxProp < len(prop.operations) or idxProp - idx0 < len(tokenOld.operations):
                if prop.operations[idxProp].upper() == tokenOld.operations[idxProp - idx0].upper():
                    idxProp += 1
                else:
                    idxProp = idx0
                    break
            if idxProp - idx0 == len(tokenOld.operations):
                sequence.append(idx0)
                idxProp = idx0
        idxProp += 1

    # Get the part that should be changed
    if len(sequence) > 0:
        for seq in sequence:
            beforeProp = prop.order[0:2 * seq]
            seqProp = prop.order[2 * seq:2 * seq + 2 * len(tokenOld.operations) + 1]
            afterProp = prop.order[2 * seq + 1 + 2 * len(tokenOld.operations) + 1:-1]

        # Replace the tokens of the new structure with the tokens of the old structure
        token = Proposition(tokenNew)
        seq = Proposition(" ".join(seqProp))
        idx = 0
        for idxToken, val in enumerate(token.order):
            if val == token.tokens[idx]:
                token.order[idxToken] = seq.tokens[idx]
                idx += 1
        beforeStatement = " ".join(beforeProp) + " " if len(beforeProp) > 0 else ""
        seqStatement = " ".join(token.order)
        afterStatement = " ".join(afterProp) if len(afterProp) > 0 else ""
        statement = beforeStatement + seqStatement + afterStatement
        token = Proposition(statement)

        # Return the token
        return token
    
    # Return the token
    return prop

# Applying the De Morgan law (WIP)
def De_Morgan(prop, beforeNot = False):
    if hasattr(prop, 'nestedToken'):
        for idx, token in list(prop.nestedToken.items()):
            prop.nestedToken[idx] = De_Morgan(token, False)
        prop.update_nestedToken()

    if "NOT" in prop.operations.upper():
        idx = prop.operations.index("NOT")
        if hasattr(prop, 'nestedToken'):
            prop.nestedToken[idx] = De_Morgan(token, True)
            prop.update_nestedToken()
        
    if beforeNot and (prop.operations.upper() == "NOT" or prop.operations.upper() == "AND" or prop.operations.upper() == "OR"):
        if prop.operations.upper() == "NOT":
            pass
        elif prop.operations.upper() == "AND":
            pass
        elif prop.operations.upper() == "OR":
            pass
        token = Proposition(token)
        return token
            
    return prop
    
# Expanding the statement (WIP)
def expansion(prop):
    pass

# Get the CNF form of the proposition
# Gotten from https://personal.cis.strath.ac.uk/robert.atkey/cs208/converting-to-cnf.html
def convert_to_CNF(proposition):
    # Step 1: Convert all "if ... then ..." to negated or (P -> Q to not P or Q)
    proposition = change_token(proposition, "X if Y", "not X or Y")

    # Step 2: Convert to Negation Normal Form (NNF) by putting a negation in front of all premises (expand with De Morgan to simplify)
    

    # Step 3: Expand the ands and ors operators
    
    
    return proposition
    

# Give the resolution alghorithm
def resolution(CNF):
    pass

# Debugging
if __name__ == "__main__":
    logic = Proposition("(A and (A if B)) if C")
    print(logic)
    logic = change_token(logic, "X if Y", "not X or Y")
    print(logic)

    