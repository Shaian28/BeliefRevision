# Import all necessary libraries
import numpy as np
import Proposition

# Change all instance of an operation
def change_ops(opOld, opNew, addNot = None):
    pass
    ## Update embedded objects in the first premise
    #if hasattr(self, 'obj1'):
    #    self.obj1 = self.obj1.change_ops(opOld, opNew, addNot)
    #    self.p = f"({self.obj1})"
    ## Update embedded objects in the second premise
    #if hasattr(self, 'obj2'):
    #    self.obj2 = self.obj2.change_ops(opOld, opNew, addNot)
    #    self.q = f"({self.obj2})"
    ## Update the operation
    #if self.op.upper() == opOld.upper():
    #    self.op = opNew
    #    # Negate first premise
    #    if addNot.upper() == "RIGHT":
    #        self.p = str(Proposition(premise1 = self.obj1 if hasattr(self, 'obj1') else self.p, operation = "not"))
    #    # Negate second premise
    #    elif addNot.upper() == "LEFT":
    #        self.q = str(Proposition(premise2 = self.obj2 if hasattr(self, 'obj2') else self.q, operation = "not"))
    #    
    ## Return the object
    #return self

# Applying the De Morgan law (WIP)
def De_Morgan():
    pass
    ## Update embedded objects in the first premise
    #if hasattr(self, 'obj1'):
    #    self.obj1 = self.obj1.De_Morgan()
    #    self.p = f"({self.obj1})"
    ## Update embedded objects in the second premise
    #if hasattr(self, 'obj2'):
    #    self.obj2 = self.obj2.De_Morgan()
    #    self.q = f"({self.obj2})"
    ## Apply De Morgan's laws
    #if self.op.upper() == "NOT" and hasattr(self, 'obj1'):
    #    # When there is double negation
    #    if self.obj1.op.upper() == "NOT":
    #        self = self.obj1.obj1 if hasattr(self.obj1, 'obj1') else self.obj1.p
    #    # When there is and in negation
    #    elif self.obj1.op.upper() == "AND":
    #        self = Proposition(
    #            Proposition(premise1 = self.obj1.obj1 if hasattr(self.obj1, 'obj1') else self.obj1.p, operation = "not"),
    #            Proposition(premise1 = self.obj1.obj2 if hasattr(self.obj1, 'obj2') else self.obj1.q, operation = "not"),
    #            operation = "or"
    #        )
    #    # When there is or in negation
    #    elif self.obj1.op.upper() == "OR":
    #        self = Proposition(
    #            Proposition(premise1 = self.obj1.obj1 if hasattr(self.obj1, 'obj1') else self.obj1.p, operation = "not"),
    #            Proposition(premise1 = self.obj1.obj2 if hasattr(self.obj1, 'obj2') else self.obj1.q, operation = "not"),
    #            operation = "and"
    #        )
#
    ## Return the object
    #return self
    
# Expanding the statement
def expansion():
    pass
    ## Update embedded objects in the first premise
    #if hasattr(self, 'obj1'):
    #    self.obj1 = self.obj1.expansion()
    #    self.p = f"({self.obj1})"
    ## Update embedded objects in the second premise
    #if hasattr(self, 'obj2'):
    #    self.obj2 = self.obj2.expansion()
    #    self.q = f"({self.obj2})"
    ## Apply the expansion for single premise at right
    #if self.op.upper() == "OR" and not hasattr(self, 'obj1') and hasattr(self, 'obj2'):
    #    print(self)
    #    self = Proposition(
    #        Proposition(premise1 = self.p, premise2 = self.obj2.obj1 if hasattr(self.obj2, 'obj1') else self.obj2.p, operation = "or"),
    #        Proposition(premise1 = self.p, premise2 = self.obj2.obj2 if hasattr(self.obj2, 'obj2') else self.obj2.q, operation = "or"),
    #        operation = "and"
    #    )
    ## Apply the expansion for single premise at left
    #elif self.op.upper() == "OR" and hasattr(self, 'obj1') and not hasattr(self, 'obj2'):
    #    self = Proposition(
    #        Proposition(premise1 = self.obj1.obj1 if hasattr(self.obj1, 'obj1') else self.obj1.p, premise2 = self.q, operation = "or"),
    #        Proposition(premise1 = self.obj1.obj2 if hasattr(self.obj1, 'obj2') else self.obj1.q, premise2 = self.q, operation = "or"),
    #        operation = "and"
    #    )
    ## Apply the expansion for premises
    #elif self.op.upper() == "OR" and hasattr(self, 'obj1') and hasattr(self, 'obj2'):
    #    self = Proposition(
    #        Proposition(premise1 = self.obj1, premise2 = self.obj2.obj1 if hasattr(self.obj2, 'obj1') else self.obj2.p, operation = "or"),
    #        Proposition(premise1 = self.obj1, premise2 = self.obj2.obj2 if hasattr(self.obj2, 'obj2') else self.obj2.q, operation = "or"),
    #        operation = "and"
    #    )
    ## Return the object
    #return self

# Get the CNF form of the proposition
# Gotten from https://personal.cis.strath.ac.uk/robert.atkey/cs208/converting-to-cnf.html
def convert_to_CNF(proposition):
    # Step 1: Convert all "if ... then ..." to negated or (P -> Q to not P or Q)
    oldProp = ""
    while str(proposition) != str(oldProp):
        print(proposition)
        oldProp = proposition
        proposition = proposition.change_ops("if", "or", "right")
    # Step 2: Convert to Negation Normal Form (NNF) by putting a negation in front of all premises (expand with De Morgan to simplify)
    oldProp = ""
    while str(proposition) != str(oldProp):
        print(proposition)
        oldProp = proposition
        proposition = proposition.De_Morgan()
    # Step 3: Expand the ands and ors operators
    oldProp = ""
    while str(proposition) != str(oldProp):
        print(proposition)
        oldProp = proposition
        proposition = proposition.expansion()
    
    return proposition
    

# Give the resolution alghorithm
def resolution(CNF):
    pass

# Debugging
if __name__ == "__main__":
    prop1 = Proposition("a", "b", "if")
    prop2 = Proposition("a", prop1, "and")
    prop3 = Proposition(prop2, "c", "if")
    print(prop3)
    CNF = convert_to_CNF(prop3)
    print(CNF)
    