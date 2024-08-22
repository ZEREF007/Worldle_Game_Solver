Wordle Solver

Overview
This Python script solves Wordle puzzles using guesses and feedback from the Wordle API. It filters possible words using the NLTK corpus and iteratively refines guesses to find the correct word.

Method:
Step 1:
Iterate from a-z to find the initaial correct/present letters

Step2:
use NLTK library to filter the common words

Step3:
Use bruteforce until found

Instructions

1. Clone the repo:
   git clone https://github.com/ZEREF007/Worldle_Game_Solver.git

2. Install dependencies:
   pip install requests nltk
   
4. Run the script:
   python wordle_solver.py

Acknowledgments
- NLTK Library
- Votee Wordle API
