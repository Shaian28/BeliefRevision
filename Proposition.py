# Import all necessary libraries
import sympy as sp
import pandas as pd

# Class for proposition
class Proposition:
    # Initialise the object
    def __init__(self, premise):
        # Getting all the tokens
        self.tokens = premise.split(" ")
        # Removing the unnecessary paranthesis at the start and end of the premise
        while self.tokens[0][0] == "(" and self.tokens[-1][-1] == ")":
            parantheses = 0
            # Going through the premise to check if the paranthesis are necessary
            for idx, char in enumerate(premise):
                # Count the paranthesis
                if char == "(":
                    parantheses += 1
                elif char == ")":
                    parantheses -= 1
                # When the paranthesis has reached 0
                if parantheses == 0:
                    # Break out of the loop
                    if idx < len(premise) - 1:
                        break
                    # Remove the paranthesis
                    else:
                        self.tokens[0] = self.tokens[0][1:]
                        self.tokens[-1] = self.tokens[-1][:-1]
            # Break out of the loop
            if idx < len(premise) - 1:
                break
        
        # Initialisation for tokens given as a statement
        idx = 0
        combinedToken = ""
        parantheses = 0
        paranthesesLoop = False
        self.nestedToken = []
        # Go through the elements to find statements in tokens
        while idx < len(self.tokens):
            # Look for open paranthesis
            if "(" in self.tokens[idx] and ")" not in self.tokens[idx]:
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
            elif "(" in self.tokens[idx] and ")" in self.tokens[idx]:
                # Remove the paranthesis in the token
                self.tokens[idx] = self.tokens[idx].replace("(", "").replace(")", "")
            # Iterate through the loop
            idx += 1
        
        # Saving the order of te tokens
        self.order = self.tokens.copy()

        # Getting all the operations and removing them from the token
        operations = ["AND", "OR", "NOT", "IF", "IFF"]
        self.operations = [oper for oper in self.tokens if oper.upper() in operations]
        for idx, operation in enumerate(self.operations):
            self.tokens.remove(operation)
        
        # Rewrite the premise as string
        self.premise = " ".join(self.order)
    
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
                    addMessage = addMessage.upper().replace("IFF", "↔")
                    addMessage = addMessage.upper().replace("IF", "→")
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

    # Get the symbolic expression that can be used for sympy
    def symbolic_form(self, depth = 0):
        depth += 1
        # Go deeper if a nested token exist and gather the variables
        allVariable = []
        if len(self.nestedToken) > 0:
            for idx, _ in enumerate(self.nestedToken):
                variable = self.nestedToken[idx].symbolic_form(depth)
                for var in variable:
                    if var not in allVariable:
                        allVariable.append(var)
        # Gather the vaiables when there is no nested tokens
        for token in self.tokens:
            if token not in allVariable and token.count("(") == 0:
                allVariable.append(token)
        
        # Turn variable to symbols when going back to the top token
        if depth == 1:
            self.symbolic = sp.symbols(" ".join(allVariable).upper())
            self.symbolic = list(self.symbolic) if type(self.symbolic) == tuple else [self.symbolic]
            expression = " ".join(self.order)

            # Turn operations into there equivalent sympy operation
            expression = expression.upper().replace("AND", "&")
            expression = expression.upper().replace("OR", "|")
            expression = expression.upper().replace("NOT", "~")
            expression = expression.upper().replace("IFF", "==")
            expression = expression.upper().replace("IF", ">>")
            
            # Save the symbolic expression
            self.expression = expression

        # Retutn alle non-repeating variables in the token
        return allVariable
    
    # Make a truth table of the expression
    def truth_table(self):
        # Make sure that the object has a symbolic form
        if not hasattr(self, "symbolic"):
            self.symbolic_form()
        # Generate a truth table
        variables = list(self.symbolic)
        num_rows = 2 ** len(variables)
        truth_values = [[(i >> j) & 1 for j in range(len(variables) - 1, -1, -1)] for i in range(num_rows)]
        self.TruthTable = pd.DataFrame(truth_values, columns=[str(var) for var in variables])
        
        # Evaluate the expression for each row in the truth table
        def truth_calc(row):
            expr = sp.parsing.sympy_parser.parse_expr(self.expression, local_dict = {str(sym): sym for sym in self.symbolic}, evaluate = False)
            exprLam = sp.lambdify(self.symbolic, expr)
            return exprLam(*row)
        
        # Add the final results in the truth table
        self.TruthTable['Result'] = self.TruthTable.apply(truth_calc, axis = 1)

# Debugging
if __name__ == "__main__":
    logic = Proposition("A and (not B or (C and A)) and (D or B)")
    print(logic)
    logic.truth_table()
    print(logic.TruthTable)