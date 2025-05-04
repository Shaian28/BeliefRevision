from Proposition import Proposition

class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def expand(self, new_sentence):
        """
        Adds a new belief (Proposition) to the belief base.
        This method does not check for consistency — pure expansion.
        """
        prop = Proposition(new_sentence)
        self.beliefs.append(prop)
        print(f"Expanded: added '{prop}' to the belief base.")
        return self  # Return the updated belief base

    def __str__(self):
        return "\n".join([f"{idx+1}: {str(b)}" for idx, b in enumerate(self.beliefs)])

# Example usage
if __name__ == "__main__":
    bb = BeliefBase()
    bb.expand("A and B")
    bb.expand("not C or A")
    print("\nCurrent belief base:")
    print(bb)
