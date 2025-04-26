# Class for proposition
class Proposition:
    # Initialise the object
    def __init__(self, premise):
        # Getting all the tokens
        self.tokens = premise.split(" ")
        if self.tokens[0][0] == "(" and self.tokens[-1][-1] == ")":
            self.tokens[0] = self.tokens[0][1:]
            self.tokens[-1] = self.tokens[-1][:-1]
        # Initialisation for tokens given as a statement
        idx = 0
        combinedToken = ""
        parantheses = 0
        paranthesesLoop = False
        self.nestedToken = []
        # Go through the elements to find statements in tokens
        while idx < len(self.tokens):
            # Look for open paranthesis
            if "(" in self.tokens[idx]:
                paranthesesLoop = True
                idx0 = idx
                combinedToken = ""
                # Find the correponding close paranthesis
                while paranthesesLoop:
                    # Count open paranthesis in statement
                    if "(" in self.tokens[idx]:
                        parantheses += self.tokens[idx].count("(")
                    # Count close paranthesis in statement
                    elif ")" in self.tokens[idx]:
                        parantheses -= self.tokens[idx].count(")")
                    # Combine the tokens before finding the corresponding close paranthesis
                    combinedToken += self.tokens[idx] if idx == idx0 else " " + self.tokens[idx]
                    # Iterate through the tokens if the closed paranthesis hasn't been found 
                    if parantheses != 0:
                        idx += 1
                    else:
                        paranthesesLoop = False
                # Write the statement as a seperate token, and initialise it as a proposition
                self.tokens[idx] = combinedToken
                del self.tokens[idx0:idx]
                self.nestedToken.append(Proposition(combinedToken))
                idx = idx0
            # Iterate through the loop
            idx += 1
        
        # Saving the order of te tokens
        self.order = self.tokens.copy()

        # Getting all the operations and removing them from the token
        operations = ["AND", "OR", "NOT", "IF", "IFF"]
        self.operations = [oper for oper in self.tokens if oper.upper() in operations]
        for idx, operation in enumerate(self.operations):
            self.tokens.remove(operation)
    
    # Print the premise symbolically
    def __str__(self):
        # Define the message and index
        message = ""
        idx, idxToken, idxOperation = 0, 0, 0
        # Go through all the tokens and operations
        while  idx < len(self.tokens) + len(self.operations):
            # Add the tokens to the message
            if self.order[idx] == self.tokens[idxToken]:
                addMessage = self.tokens[idxToken]
                # Replace the operations in statements
                if "(" in self.tokens[idxToken]:
                    addMessage = addMessage.upper().replace("AND", "∧")
                    addMessage = addMessage.upper().replace("OR", "∨")
                    addMessage = addMessage.upper().replace("NOT", "¬")
                    addMessage = addMessage.upper().replace("IF", "→")
                    addMessage = addMessage.upper().replace("IFF", "↔")
                    addMessage = addMessage.replace(" ", "")
                message += addMessage
                idxToken += 1
            # Add the operation to the message
            elif self.order[idx] == self.operations[idxOperation]:
                operation = self.operations[idxOperation].upper()
                addMessage = "∧" if operation == "AND" else "∨" if operation == "OR" else "¬" if operation == "NOT" else "→" if operation == "IF" else "↔" if operation == "IFF" else ""
                message += addMessage
                idxOperation += 1
            # Iterate through the order
            idx += 1
        
        # Return the message
        return message
            

# Debugging
if __name__ == "__main__":
    logic = Proposition("A and (not B or (C and A)) and (D or B)")
    print(logic)
    print(logic.nestedToken[0])
    print(logic.nestedToken[0].nestedToken[0])
    print(logic.nestedToken[1])