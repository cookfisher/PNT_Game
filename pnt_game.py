import copy
import math

from numpy import inf
# Initial value of alpha be Double.NEGATIVE_INFINITY (which is in JAVA, not python, here we use the numpy)
# beta be Double.POSITIVE_INFINITY. Assume the worst case with infinity.
ALPHA = -inf
BETA = inf


class Node:
    def __init__(self, tokens_remain, parent, last_move, depth):
        self.tokens_remain = tokens_remain
        self.parent = parent
        self.last_move = last_move
        self.depth = depth
        self.e = 0
        self.children = []

        def addNode(self, obj):
            self.children.append(obj)
            self.depth += 1

        def addNodes(self, obj):
            self.children.extend(obj)
            self.depth += 1

        def setLast_move(self, last_move):
            self.last_move = last_move

        def setDepth(self, depth):
            self.depth = depth

        def get_tokens(self):
            return self.tokens_remain

        def getChildNodes(self):
            return self.children

        def getRemainTokens(self, parent, last_move):
            new_tokens_remain = copy.deepcopy(parent)
            new_tokens_remain.remove(last_move)
            return new_tokens_remain


def create_node(tokens_remain, parent_node, last_move, depth):
    return Node(tokens_remain, parent_node, last_move, depth)
    # return Node(tokens_remain, parent_node, last_move, depth, e)


# all possible nodes/choices
def findChildNodes(parent_node, turns): # , num_of_tokens
    tokens_remain = parent_node.tokens_remain
    #last_move = parent_node.last_move
    length = len(tokens_remain)
    child_nodes = []
    # At the first move
    if turns == 1:
        for move in tokens_remain:
            if move < length/2 and move % 2 == 1:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                #e = evaluation(turns, child_node, last_move, num_of_tokens)
                #child_node.e = e
                child_nodes.append(child_node)
    # At subsequent moves
    else:
        possible_moves = find_multiples_or_factors(parent_node.last_move, parent_node.tokens_remain)
        for move in tokens_remain:
            if move in possible_moves:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                #e = evaluation(turns, child_node, last_move, num_of_tokens)
                #child_node.e = e
                child_nodes.append(child_node)

    print("Children of", parent_node.tokens_remain, "=", len(child_nodes))
    for i in range(len(child_nodes)):
        print(child_nodes[i].tokens_remain, "move =", child_nodes[i].last_move, "depth = ", child_nodes[i].depth)

    parent_node.children = child_nodes
    return child_nodes


def build_tree(start_node, c1):
    #c1 = findChildNodes(start_node,turn)
    if c1:
        for i in c1:
            c2 = findChildNodes(i, turn+1)
            #if c2:
                #i.addNodes(c2)
        return build_tree(start_node, c2)
    else:
        print("TREE BUILT")
        return


# return list of all multiples and factors,
# add (and XXX in tokens_remain) if want to return the elements in token_remain only
def find_multiples_or_factors(num, tokens_remain):
    factors_multiples = []
    # factors
    for i in range(1, num + 1):
        mod = num % i
        if mod == 0:
            factors_multiples.append(i)
    # multiples
    multiplier = 2
    n = num
    while n < max(tokens_remain):
        n *= multiplier
        if n <= max(tokens_remain):
            factors_multiples.append(n)
            multiplier += 1
            n = num
    print(num, "'s all factors and multiples (include taken token) in", tokens_remain, ": ", factors_multiples)
    return factors_multiples


def generate_list(number):
    tokens = []
    for i in range(number):
        tokens.append(i+1)
    print(tokens)
    return tokens


def is_max_turn(taken_tokens):
    # taken_tokens is list
    if len(taken_tokens) % 2 == 0:
        return True
    else:
        return False


# ---------------------------------back up-------------------------------------------
def min_max(node, depth, alpha, beta, maximizingPlayer):
    child_nodes = node.children
    # If depth is 0, search to end game states and return the index of player.
    if depth == 0 or len(child_nodes) == 0:
        return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, False)
            max_value = max(max_value, eval)
            alpha = max(alpha, eval)
            # If beta is less or equal to alpha, break the loop
            if beta <= alpha:
                break
        return max_value
            # recursive for the children
    else:
        min_value = inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, True)
            min_value = min(min_value, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_value



def alpha_beta_search(node, depth, alpha, beta, maximizingPlayer):
    best_state = None
    child_nodes = node.children

    #test children
    for node in child_nodes:
        print(node.tokens_remain)
    print("alpha_beta_search depth =", depth)

    # If depth is 0, search to end game states and return the index of player.
    if depth == 0 or len(child_nodes) == 0:
        #print("Node", node.tokens_remain, "Node Depth", node.depth)
        e = evaluation(maximizingPlayer, node, node.last_move)
        #best_state = node
        print("Move:", node.last_move)
        return e
        #return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            max_value = alpha_beta_search(child, depth - 1, alpha, beta, False)
            #max_value = max(max_value, eval)
            alpha = max(alpha, max_value)
            # If beta is less or equal to alpha, break the loop
            if alpha >= beta:
                break
            #else:
                #best_state = child
                #print("Move:", best_state.last_move)
        print("Max =", max_value)
        return max_value
            # recursive for the children
    else:
        min_value = inf
        for child in child_nodes:
            min_value = alpha_beta_search(child, depth - 1, alpha, beta, True)
            #min_value = min(min_value, eval)
            beta = min(beta, min_value)
            if beta <= alpha:
                break
            #else:
                #best_state = child
                #print("Move:", best_state.last_move)
        print("Min =", min_value)
        return min_value


def evaluation(isMaxTurn, node, last_move): # , num_of_tokens, turns
    e = 0
    # game end
    #child_nodes = findChildNodes(node, turns)
    child_nodes = node.children
    if len(node.tokens_remain) == 0 or len(child_nodes) == 0:
        #Player A (MAX) wins: 1.0, Player B (MIN) wins: -1.0
        if isMaxTurn == False:   #min's turn & game finish /turns % 2 == 0
            e = 1.0
        else:               #max's turn & game finish
            e = -1.0
        print("Value =", e)
        return e
    # max turn
    if isMaxTurn == True: # turns % 2 == 1
        # token 1 is not taken yet
        if 1 in node.tokens_remain:
            e = 0
            print("Value =", e)
            return e
        # last move was 1
        if last_move == 1:
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.5
            elif len(child_nodes) % 2 == 0:
                e = -0.5
            print("Value =", e)
            return e
        # last move is a prime
        if is_prime(last_move):
            #child_nodes = findChildNodes(tokens_remain)
            prime_multiples = find_prime_multiples(last_move, child_nodes, True)
            if prime_multiples % 2 == 1:
                e = 0.7
            elif prime_multiples % 2 == 0:
                e = -0.7
            print("Value =", e)
            return e
        #the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            prime_multiples = find_prime_multiples(largest_prime, child_nodes, False)

            #count = 0
            #multiplier = 1
            #while largest_prime < num_of_tokens:
                #count += 1
                #multiplier += 1
                #largest_prime *= multiplier

            if prime_multiples % 2 == 1:
                e = 0.6
            elif prime_multiples % 2 == 0:
                e = -0.6
            print("Value =", e)
            return e
    # min turn
    if isMaxTurn == False:
        # token 1 is not taken yet
        if 1 in node.tokens_remain:
            e = 0
            return e
        # last move was 1
        if last_move == 1:
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = -0.5
            elif len(child_nodes) % 2 == 0:
                e = 0.5
            print("Value =", e)
            return e
        # last move is a prime
        if is_prime(last_move):
            #child_nodes = findChildNodes(tokens_remain)
            prime_multiples = find_prime_multiples(last_move, child_nodes, True)
            if prime_multiples % 2 == 1:
                e = -0.7
            elif prime_multiples % 2 == 0:
                e = 0.7
            print("Value =", e)
            return e
        # the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            prime_multiples = find_prime_multiples(largest_prime, child_nodes, False)

            # count = 0
            # multiplier = 1
            # while largest_prime < num_of_tokens:
            # count += 1
            # multiplier += 1
            # largest_prime *= multiplier

            if prime_multiples % 2 == 1:
                e = -0.6
            elif prime_multiples % 2 == 0:
                e = 0.6
            print("Value =", e)
            return e



def is_prime(n):
    if n < 2:
        print("Is prime = ", False)
        return False
    else:
        if n % 2 == 0 or n % 3 == 0:
            print("Is prime = ", False)
            return False
        # all primes are of the form 6k ± 1
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                print("Is prime = ", False)
                return False
            i = i + 6
        print(n, "is prime =", True)
        return True


def find_prime_multiples(num, child_nodes, is_prime):
    num_of_multiples = 0
    multiplier = 1
    list_multiples = []
    for node in child_nodes:
        copy_tokens_remain = copy.deepcopy(node.tokens_remain)
        n = num

        if is_prime == True:
            multiplier = 2
        elif is_prime == False:
            multiplier = 1

        while n < max(copy_tokens_remain):
            n *= multiplier
            if n <= max(copy_tokens_remain) and n in copy_tokens_remain:
                list_multiples.append(n)
                num_of_multiples += 1
                multiplier += 1
                n = num
    print("Find prime multiples in all children =", num_of_multiples, ":",list_multiples)
    return num_of_multiples


def maxPrimeFactors (n):
    max_prime = -1
    while n % 2 == 0:
        max_prime = 2
        #n /= 2
        n >>= 1
    # find last odd integer that cannot divide n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            max_prime = i
            n = n / i
    if n > 2:
        max_prime = n
    print("max_prime_factor:", max_prime)
    return int(max_prime)


# ----------Driver Code----------
#test
test_list = generate_list(7)
test_list2 = [2, 3, 4, 7, 8, 10]
input2 = [2, 3, 4, 5, 6, 7]
input3 = [1, 3, 5, 7, 8, 9, 10]

is_prime(31)
maxPrimeFactors(25)
find_multiples_or_factors(4,test_list2)

start_node = create_node(test_list, None, 0, 0)
second_node = create_node([3,6,7,9,12], start_node, 1, 1)
third_node = create_node([3,4,5,7], start_node, 1, 1)

# test find_prime_multiples
nodes = [second_node, third_node]
find_prime_multiples(3, nodes, True)
find_prime_multiples(3, nodes, False)
print()

# e(n)
#test_node = create_node(test_list2, None, 0, 0)
#test_node.children = nodes
#evaluation(3, test_node, 5)

# PNT
turn = 2
start1 = create_node(input2, None, 1, 0)
start2 = create_node(input3, None, 6, 0)
c1 = findChildNodes(start1, turn)
build_tree(start1, c1)
#child1 = start.children[1]
#child2 = child1.children[1]
#print(child2.tokens_remain)
print()
isMaxTurn = is_max_turn([1])
alpha_beta_search(start1, 2, ALPHA, BETA, isMaxTurn)
#alpha_beta_search(start2, 4, ALPHA, BETA, True)
