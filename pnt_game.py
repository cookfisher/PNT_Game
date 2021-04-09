from numpy import inf
# Initial value of alpha be Double.NEGATIVE_INFINITY (which is in JAVA, not python, here we use the numpy)
# beta be Double.POSITIVE_INFINITY. Assume the worst case with infinity.
ALPHA = -inf
BETA = inf

def min_max(position, depth, max):
    # If depth is 0, search to end game states and return the index of player.
    if depth == 0:
        return max

    # The player is max
    if max:
        max_value = -inf
        for child in position:
            eval = min_max(child, depth - 1, False)
            max_value = max(max_value, eval)
            alpha = max(ALPHA, eval)
            # If beta is less or equal to alpha, break the loop
            if BETA <= ALPHA:
                break
        return max_value
            # recursive for the children
    else:
        min_value = inf
        for child in position:
            eval = min_max(child, depth - 1, True)
            min_value = min(min_value, eval)
            beta = min(BETA,eval)
            if BETA <= ALPHA:
                break
        return min_value
