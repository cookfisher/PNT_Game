# PNT_Game
https://github.com/cookfisher/PNT_Game/ </br>
To implement the Alpha-Beta pruning algorithm to play a two-player game called PNT: pick numbered-tokens.  

pnt_game.py  
	1. Create the Node class and build tree.  
	2. Main algorithm. Implement Alpha-Beta pruning and make the evaluation via functions alpha_beta_search(node, depth, alpha, beta, maximizingPlayer) 
	and evaluation(isMaxTurn, node, last_move)  
	3. Help functions. a. find the prime, multiple factors.  
	4. Driver. Test different inputs and obtain the results  
	  
	  
PNT_Player.py  
	1. Read the input values from command line via function read_arg(). eg. python PNT_Player.py PNT_Player 7 2 3 6 0  
	2. Read the input values without player via function read_arg_without_player. eg. python PNT_Player.py 7 2 3 6 0  
	3. Help function to generate unused token list based on the number of token.  

Testcase10.txt  
	Provide ten test cases based on the requirement.  

Output_10_cases.txt  
	Return the outputs of ten test cases.  
