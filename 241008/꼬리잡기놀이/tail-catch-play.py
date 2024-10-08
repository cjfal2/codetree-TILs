def move_head():
    print(k)
    visited = [[0 for _ in range(N)] for _ in range(N)]
    for _ in range(M):
        n, m = heads.pop(0)
        four_three = 0
        nx, ny = 0, 0
        for dx, dy in directions:
            nnx, nny = n + dx, m + dy
            if 0 <= nnx < N and 0 <= nny < N and pan[nnx][nny] in [4, 3]:
                if pan[nnx][nny] == 4:
                    four_three = 4
                    nx, ny = nnx, nny

                if pan[nnx][nny] == 3 and four_three == 0:
                    four_three = 3
                    nx, ny = nnx, nny

        if four_three == 4:
            pan[nx][ny], pan[n][m] = 1, 4
            visited[nx][ny] = 1
            visited[n][m] = 1
            heads.append((nx, ny))
            flag = True
            while flag:
                for dx, dy in directions:
                    nx, ny = n + dx, m + dy
                    if 0 <= nx < N and 0 <= ny < N and 1 < pan[nx][ny] < 4 and not visited[nx][ny]:
                        if pan[nx][ny] == 3:
                            flag = False
                            pan[n][m], pan[nx][ny] = 3, 4
                            visited[nx][ny] = 1
                            break

                        pan[n][m], pan[nx][ny] = 2, 4
                        visited[nx][ny] = 1
                        n, m = nx, ny
                        break
                else:
                    break

        elif four_three == 3:
            pan[nx][ny], pan[n][m] = 1, 2
            visited[nx][ny] = 1
            visited[n][m] = 1
            heads.append((nx, ny))
            for dx, dy in directions:
                nnx, nny = nx + dx, ny + dy
                if 0 <= nnx < N and 0 <= nny < N and 1 < pan[nnx][nny] < 4 and not visited[nnx][nny]:
                    pan[nnx][nny] = 3
                    break


def throw_ball(round):
    global d, bx, by, s

    if (round - 1) % N == 0 and round != 1:
        s = (s+1) % 4
    else:
        sx, sy = directions[s]
        bx += sx
        by += sy

    dx, dy = directions[d]
    if round % N == 0:
        d = (d+1) % 4

    x, y = bx, by
    score = 0
    while 1:
        if 0 < pan[x][y] < 4:
            visited = [[0 for _ in range(N)] for _ in range(N)]
            visited[x][y] = 1
            q = [(x, y)]
            ox, oy = 0, 0
            tx, ty = 0, 0
            while q:
                i, j = q.pop(0)
                if pan[i][j] == 1:
                    score += visited[i][j] ** 2
                    ox, oy = i, j

                if pan[i][j] == 3:
                    tx, ty = i, j


                for dx, dy in directions:
                    nx, ny = i + dx, j + dy
                    if N > nx >= 0 and N > ny >= 0 and not visited[nx][ny] and 0 < pan[nx][ny] < 4:
                        if pan[i][j] == 3 and pan[nx][ny] == 1:
                            continue

                        if pan[i][j] == 1 and pan[nx][ny] == 3:
                            continue

                        visited[nx][ny] = visited[i][j] + 1
                        q.append((nx, ny))
            break
        else:
            x += dx
            y += dy
            if N > x >= 0 and N > y >= 0:
                continue
            else:
                break
    if score:
        pan[tx][ty], pan[ox][oy] = 1, 3
        heads.remove((ox, oy))
        heads.append((tx, ty))
    return score


N, M, K = map(int, input().split())  # 격자의 크기 n, 팀의 개수 m, 라운드 수 k

# 1은 머리사람, 2는 머리사람과 꼬리사람이 아닌 나머지, 3은 꼬리사람, 4는 이동 선을 의미합니다.
pan = []
heads = []
visited_teams = [[0 for _ in range(N)] for _ in range(N)]
for n in range(N):
    temp = list(map(int, input().split()))
    for m in range(N):
        if temp[m] == 1:
            heads.append((n, m))
    pan.append(temp)
d = 0
bx, by = -1, 0
s = 3
directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # 우상좌하
answer = 0
for k in range(1, K+1):
    move_head()
    answer += throw_ball(k)
print(answer)