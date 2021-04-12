import math

from numpy import inf
# Initial value of alpha be Double.NEGATIVE_INFINITY (which is in JAVA, not python, here we use the numpy)
# beta be Double.POSITIVE_INFINITY. Assume the worst case with infinity.
ALPHA = -inf
BETA = inf


class Node:
    def __init__(self, tokens, last_move, depth, e):
        self.tokens = tokens
        self.last_move = last_move
        self.depth = depth
        self.e = e


def generate_list(number):
    tokens = []
    for i in range(number):
        tokens.append(i+1)
    print(tokens)
    return tokens


def is_max_turn(taken_tokens):
    # taken_tokens is list
    if len(taken_tokens) % 2 == 1:
        return True
    else:
        return False


def min_max(child_nodes, depth, alpha, beta, maximizingPlayer):
    # If depth is 0, search to end game states and return the index of player.
    if depth == 0:
        return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, False)        #--------why depth-1 not+1?-----------
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


def move():

    return 0


def evaluation(turn, tokens_remain, last_move, num_of_tokens):
    e = 0
    # game end
    if len(tokens_remain) ==0:
        #Player A (MAX) wins: 1.0, Player B (MIN) wins: -1.0
        if turn % 2 == 0:   #min's turn & game finish
            e = 1.0
        else:               #max's turn & game finish
            e = -1.0
        return e
    # max turn
    if turn % 2 == 1:
        # token 1 is not taken yet
        if 1 in tokens_remain:
            e = 0
            return e
        # last move was 1
        if last_move == 1:
            child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.5
            elif len(child_nodes) % 2 == 0:
                e = -0.5
            return e
        # last move is a prime
        if is_prime(last_move):
            child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.7
            elif len(child_nodes) % 2 == 0:
                e = -0.7
            return e
        #the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            count = 0
            multiplier = 1
            while largest_prime < num_of_tokens:
                count += 1
                multiplier += 1
                largest_prime *= multiplier

            if count % 2 == 1:
                e = 0.6
            elif count % 2 == 0:
                e = -0.6
            return e
    # min turn
    if turn % 2 == 0:
        # token 1 is not taken yet
        if 1 in tokens_remain:
            e = 0
            return e
        # last move was 1
        if last_move == 1:
            child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = -0.5
            elif len(child_nodes) % 2 == 0:
                e = 0.5
            return e
        # last move is a prime
        if is_prime(last_move):
            child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = -0.7
            elif len(child_nodes) % 2 == 0:
                e = 0.7
            return e
        # the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            count = 0
            multiplier = 1
            while largest_prime < num_of_tokens:
                count += 1
                multiplier += 1
                largest_prime *= multiplier

            if count % 2 == 1:
                e = -0.6
            elif count % 2 == 0:
                e = 0.6
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
        print("Is prime = ", True)
        return True

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
    print("Max_prime_factor: ", max_prime)
    return int(max_prime)


# all possible nodes
def findChildNodes(tokens_remain):
    child_nodes = []
    return child_nodes

# Driver Code
generate_list(4)
is_prime(31)
maxPrimeFactors(105)