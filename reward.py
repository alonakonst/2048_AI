def calculate_reward(board):
    reward = 20
    max_value=0
    count_of_max = 0
    count_of_2nd_max = 0
    count_of_3rd_max = 0
    count_of_nonzero = 0
    for row in range(4):
        for col in range(4):
            if board[row][col]==max_value:
                count_of_max += 1
            if board[row][col]>max_value:
                count_of_max = 1
                max_value=board[row][col]

    for row in range(4):
        for col in range(4):
            if board[row][col]==max_value/2:
                count_of_2nd_max += 1
            if board[row][col]==max_value/4:
                count_of_3rd_max += 1
            if board[row][col]!= 0:
                count_of_nonzero += 1

    reward += 100 * ((count_of_max+count_of_2nd_max+count_of_3rd_max)/count_of_nonzero if count_of_nonzero>0 else 1)

    reward += ((16-count_of_nonzero)/16)*300
    if max_value==2048:
        reward += 100
    elif max_value==1024:
        reward += 90
    elif max_value == 512:
        reward += 80
    elif max_value == 256:
        reward += 70
    elif max_value == 128:
        reward += 60
    elif max_value == 64:
        reward += 50
    elif max_value == 32:
        reward += 40
    elif max_value == 16:
        reward += 30
    elif max_value == 8:
        reward += 20
    elif max_value == 4:
        reward += 10
    elif max_value == 2:
        reward += 5


    if board[3][3] or board[0][0] or board[0][3] or board[3][0] == max_value:
        reward += 100


    max_monoticity = 0
    for row in range(4):
        monoticity = monoticity_calculation(board[row])
        if monoticity > max_monoticity:
            max_monoticity=monoticity

    for col in range(4):
        monoticity = monoticity_calculation([row[col] for row in board])
        if monoticity > max_monoticity:
            max_monoticity=monoticity

    reward += max_monoticity

    return reward


def monoticity_calculation(sequence):


    if all(sequence[i] <= sequence[i + 1] for i in range(len(sequence) - 1)):
        return 100  # Increasing monotonicity
    elif all(sequence[i] >= sequence[i + 1] for i in range(len(sequence) - 1)):
        return 100  # Decreasing monotonicity
    elif sequence[0] >= sequence[1] >= sequence[2]:
        return 95
    elif sequence[3] >= sequence[2] >= sequence[1]:
        return 95
    elif sequence[0] >= sequence[1]:
        return 60
    elif sequence[3] >= sequence[2]:
        return 60

    else:
        return 0