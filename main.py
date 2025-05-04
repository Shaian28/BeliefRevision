
# main.py
from BeliefBase import BeliefBase
from Proposition import Proposition
from BeliefContraction import contract_belief_base
import AGM

def test_agm_postulates(belief_base, new_prop):
    print("\n--- Testing AGM Postulates ---")

    # Success Postulate: After revision, the new belief is included
    print("Success Postulate:", new_prop in belief_base.formulas)

    # Inclusion Postulate: All previous beliefs not contradicting new belief should be retained
    print("Beliefs retained after revision:", [str(p) for p in belief_base.formulas if p != new_prop])

    # Vacuity Postulate: If the new belief is already in the belief base, no change needed
    print("Vacuity Postulate:", new_prop in belief_base.formulas)

    # Consistency: Belief base should remain consistent (mock check)
    # (Actual consistency checking would need entailment logic applied)
    print("Consistency: Not formally checked here.")

def print_belief_base(belief_base):
    print("Current Belief Base:")
    for i, b in enumerate(belief_base.formulas):
        print(f"  [{i+1}] {b}")

def main():
    print("=== Belief Revision Engine ===")
    belief_base = BeliefBase()
    belief_base.expand("A and B")
    belief_base.expand("C if A")

    while True:
        print("\nOptions:")
        print("1. Expand belief base with a proposition or add initial beliefs")
        print("2. Contract belief base with a proposition")
        print("3. View current belief base")
        print("4. Test with AGM postulates")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            belief = input("Enter proposition to expand with: ")
            belief_base.expand(belief)
            print("Belief base expanded.")
        elif choice == "2":
            belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(belief_base.beliefs)]
            belief = input("Enter proposition to contract with: ")
            prop = Proposition(belief)
            contract_belief = contract_belief_base(belief_base_with_priorities, prop)
            belief_base.beliefs = [Proposition(belief.premise) for belief, _ in contract_belief]
            print("Belief base contracted.")
        elif choice == "3":
            print(belief_base)
        elif choice == "4":
            belief = input("Enter proposition to test out: ")
            prop = Proposition(belief)
            test_agm_postulates(belief_base, prop)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
