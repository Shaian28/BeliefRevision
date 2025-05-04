# Belief Revision
This project is about making a belief revision agent. To run the game, open bash terminal, go to the directory with `cd` and type the following line:\
`python3 main.py`

The bash terminal will then give you 5 options. Press `1` to expand the belief base, type `2` to contract the belief base, type `3` to view the beliefs currently in the belief base, type `4` to test the belief base with the AGM postulates success, inclusion, vacuity, consistency and extensionality, and type `5` to exit the code.\
The belief base is empty by default, so as first commando, go to `1` and expand the belief base.

If you typed either `1` or `2`, then you will end up in a line, where you are requested to enter a proposition. The proposition should be written with the variables as uppercase letters (preferably singular) and the operation should be given in lowercase letter, with either `and`, `or`, `not`, `if` or `iff`. The operations/variables should be seperated with a space and set the paranthesis in the right spot.\
Example of a valid proposition in the code:\
`A or (not C and (B or A)) iff C`

If you typed `1` from the first menu, then the next line will prompt with given the proposition a priority. The priority is given as a value between 1 and 10, with 1 being untrustworty and 10 being completely trustworthy. If you don't know the priority, then give it a priority of 5.

If you typed `4` from the first menu, then the next line will prompt you to enter a proposition to test the postulates. Give with the same syntax as before. This prompt will appear twice, the second time for the extensionality postulate, which requires two arguments.
