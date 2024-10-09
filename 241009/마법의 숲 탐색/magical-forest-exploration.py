"""
정령들이 R행 C열의 격자 형태로 이루어진 마법의 숲을 탐색하려고 합니다.
격자는 가장 위를 1행, 가장 아래를 R행으로 합니다.

숲의 동쪽, 서쪽, 남쪽은 마법의 벽으로 막혀 있으며,
정령들은 숲의 북쪽을 통해서만 숲에 들어올 수 있습니다.

총 K명의 정령은 각자 골렘을 타고 숲을 탐색합니다.
각 골렘은 십자 모양의 구조, 중앙 칸을 포함해 총 5칸
골렘의 중앙을 제외한 4칸 중 한 칸은 골렘의 출구, 골렘에서 내릴 때에는 정해진 출구를 통해야함

중앙이 c 열이 되도록 하는 위치에서 내려오기 시작합니다. 초기 골렘의 출구는 d 의 방향에 위치

더 이상 움직이지 못할 때까지 해당 과정을 반복합니다.
(1) 남쪽으로 한 칸 내려갑니다.
(2) (1)의 방법으로 이동할 수 없으면 서쪽 방향으로 회전하면서 내려갑니다. 반시계로 출구가 이동
(3) (1)과 (2)의 방법으로 이동할 수 없으면 동쪽 방향으로 회전하면서 내려갑니다. 출구가 시계방향으로 이동

골렘이 이동할 수 있는 가장 남쪽에 도달해 더이상 이동할 수 없으면
정령은 골렘 내에서 상하좌우 인접한 칸으로 이동이 가능합니다.
단, 만약 현재 위치하고 있는 골렘의 출구가 다른 골렘과 인접하고 있다면
해당 출구를 통해 다른 골렘으로 이동할 수 있습니다.

정령은 갈 수 있는 모든 칸 중 가장 남쪽의 칸으로 이동하고 종료

골렘의 몸 일부가 여전히 숲을 벗어난 상태라면, 해당 골렘을 포함해
숲에 위치한 모든 골렘들은 숲을 빠져나간
뒤 다음 골렘부터 새롭게 숲의 탐색을 시작  => pan reset

숲이 다시 텅 비게 돼도 행의 총합은 누적되는 것에 유의합니다. 턴마다 answer 를 갱신
"""


def move_golem(y, where_exit, turn):
    global pan, golem

    # y: 시작열, where_exit: 출구 방향
    x = -2
    # -2, y 에서부터 골렘이 들어갈 수 있는지 부터 봐야함
    golem = [(x, y)]
    for dx, dy in directions:
        golem.append((x + dx, y + dy))
    flag = True

    check_rl = 0

    temp_golem = golem[:]
    temp_exit = where_exit

    while flag:
        new_golem = []
        # 남쪽으로 이동
        for x, y in temp_golem:
            new_golem.append((x+1, y))
        # 남쪽 가능한지 체크
        for x, y in new_golem:
            if x < 0:
                continue
            else:
                if 0 <= x < N and 0 <= y < M:
                    if pan[x][y]:
                        break
                else:
                    break
        else:
            # 남쪽 가능한거임
            temp_golem = list(tuple(new_golem))
            golem = temp_golem[:]
            check_rl = 1
            where_exit = temp_exit
            continue


        if temp_golem[0][0] != N-2:
            # 서쪽으로 이동
            new_golem.clear()
            for x, y in temp_golem:
                new_golem.append((x, y-1))

            # 서쪽 가능한지 체크
            for x, y in new_golem:
                if x < 0:
                    continue
                if 0 <= x < N and 0 <= y < M:
                    if pan[x][y]:
                        break
                else:
                    break
            else:
                # 서쪽 가능한거임
                temp_golem = list(tuple(new_golem))
                temp_exit = (temp_exit - 1) % 4
                check_rl = 2
                # 남쪽으로 이동
                new_golem.clear()
                for x, y in temp_golem:
                    new_golem.append((x + 1, y))
                # 남쪽 가능한지 체크
                for x, y in new_golem:
                    if x < 0:
                        continue
                    else:
                        if 0 <= x < N and 0 <= y < M:
                            if pan[x][y]:
                                break
                        else:
                            break
                else:
                    # 남쪽 가능한거임
                    temp_golem = list(tuple(new_golem))
                    golem = temp_golem[:]
                    check_rl = 1
                    where_exit = temp_exit
                    continue



        if temp_golem[0][0] != N - 2:
            # 동쪽으로 이동
            new_golem.clear()
            for x, y in temp_golem:
                new_golem.append((x, y + 1))

            # 동쪽 가능한지 체크
            for x, y in new_golem:
                if x < 0:
                    continue
                if 0 <= x < N and 0 <= y < M:
                    if pan[x][y]:
                        break
                else:
                    break
            else:
                # 동쪽 가능한거임
                temp_golem = list(tuple(new_golem))
                temp_exit = (temp_exit + 1) % 4
                check_rl = 3
                # 남쪽으로 이동
                new_golem.clear()
                for x, y in temp_golem:
                    new_golem.append((x + 1, y))
                # 남쪽 가능한지 체크
                for x, y in new_golem:
                    if x < 0:
                        continue
                    else:
                        if 0 <= x < N and 0 <= y < M:
                            if pan[x][y]:
                                break
                        else:
                            break
                else:
                    # 남쪽 가능한거임
                    temp_golem = list(tuple(new_golem))
                    golem = temp_golem[:]
                    check_rl = 1
                    where_exit = temp_exit
                    continue



        # 아무것도 못한다면 나갔는지 판단후 pan에 저장
        for x, y in golem:
            if 0 <= x < N and 0 <= y < M:
                continue
            else:
                # 나간거임, pan clear
                pan = [[0 for _ in range(M)] for _ in range(N)]
                return
        else:
            # 정착
            ex, ey = directions[where_exit]
            cx, cy = golem[0]
            cx += ex
            cy += ey
            for x, y in golem:
                if (x, y) == (cx, cy):
                    pan[x][y] = -turn  # 출구
                else:
                    pan[x][y] = turn

            return


def check_score():
    global golem

    if not golem:
        return 0

    visited = [[0 for _ in range(M)] for _ in range(N)]
    max_hang = 0
    i, j = golem[0]
    visited[i][j] = 1
    q = [(i, j, pan[i][j])]
    max_hang = max(max_hang, i+1)
    while q:
        x, y, now_num = q.pop(0)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < M and visited[nx][ny] == 0:
                if now_num < 0: # 여기가 출구라면, 0 아니면 갈 수 있음?
                    if 0 != pan[nx][ny]:
                        visited[nx][ny] = 1
                        max_hang = max(max_hang, nx+1)
                        q.append((nx, ny, pan[nx][ny]))

                elif now_num != 0: # 다른 숫자라면 pan[nx][ny]가 now_num랑 -now_num이면 갈 수 있음
                    if pan[nx][ny] in [now_num, -now_num]:
                        visited[nx][ny] = 1
                        max_hang = max(max_hang, nx+1)
                        q.append((nx, ny, pan[nx][ny]))

    return max_hang


N, M, K = map(int, input().split())  # 정령의 수 K
pan = [[0 for _ in range(M)] for _ in range(N)]
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
answer = 0
golem = []
for k in range(1, K+1):
    # d 는 0과 3 사이의 수로 주어지며 각각의 숫자 0,1,2,3은 북, 동, 남, 서쪽
    c, d = map(int, input().split())  # 출발열, 출구 방향
    c -= 1  # 열 맞추기
    move_golem(c, d, k)
    # for p in pan:
    #     print(*p)
    # print("=============")
    answer += check_score()

print(answer)