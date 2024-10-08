"""
n * n 격자에서 꼬리잡기놀이를 진행합니다. 꼬리잡기놀이는 다음과 같이 진행됩니다.

3명 이상이 한 팀이 됩니다. 모든 사람들은 자신의 앞 사람의 허리를 잡고 움직이게 되며,
맨 앞에 있는 사람을 머리사람, 맨 뒤에 있는 사람을 꼬리사람이라고 합니다.
각 팀은 게임에서 주어진 이동 선을 따라서만 이동합니다.
각 팀의 이동 선은 끝이 이어져있습니다. 각 팀의 이동 선은 서로 겹치지 않습니다.


1. 먼저 각 팀은 머리사람을 따라서 한 칸 이동합니다.
2. 각 라운드마다 공이 정해진 선을 따라 던져집니다. n개의 행,
n개의 열이 주어진다고 했을 때 공이 던져지는 선은 다음과 같습니다.
그림참조 - 라운드마다 한 줄 씩 동서남북이 다름
4n번째 라운드를 넘어가는 경우에는 다시 1번째 라운드의 방향으로 돌아갑니다.

3. 공이 던져지는 경우에 해당 선에 사람이 있으면 최초에 만나게 되는 사람만이
공을 얻게 되어 점수를 얻게 됩니다. 점수는 해당 사람이 머리사람을 시작으로
팀 내에서 k번째 사람이라면 k의 제곱만큼 점수를 얻게 됩니다.
아무도 공을 받지 못하는 경우에는 아무 점수도 획득하지 못합니다.
위의 예시에서 1라운드는 다음과 같이 진행됩니다.

머리사람에서 3번째에 있는 사람이 공을 얻었기 때문에 9(3 * 3)점을 획득하게 됩니다.
공을 획득한 팀의 경우에는 머리사람과 꼬리사람이 바뀝니다. 즉 방향을 바꾸게 됩니다.

각 팀이 획득한 점수의 총합을 구하는 프로그램을 구하세요.
"""
def move_head():
    visited = [[0 for _ in range(N)] for _ in range(N)]
    for _ in range(M):
        n, m = heads.pop(0)
        four_two = 0
        nx, ny = 0, 0
        for dx, dy in directions:
            nnx, nny = n + dx, m + dy
            if 0 <= nnx < N and 0 <= nny < N and pan[nnx][nny] in [4, 2]:
                if pan[nnx][nny] == 4:
                    four_two = 4
                    nx, ny = nnx, nny
                if pan[nnx][nny] == 2 and four_two == 0:
                    four_two = 2
                    nx, ny = nnx, nny

        if four_two == 4:
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

        elif four_two == 2:
            pan[nx][ny], pan[n][m] = 1, 2
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
                            pan[n][m], pan[nx][ny] = 3, 2
                            visited[nx][ny] = 1
                            break

                        visited[nx][ny] = 1
                        n, m = nx, ny
                        break
                else:
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
                    if (i, j) != (x, y):
                        continue

                for dx, dy in directions:
                    nx, ny = i + dx, j + dy
                    if N > nx >= 0 and N > ny >= 0 and not visited[nx][ny] and 0 < pan[nx][ny] < 4:
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