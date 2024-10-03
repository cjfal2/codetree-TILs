"""
-1, 0, 그리고 1이상 m이하의 숫자로만 이루어진 n * n 크기의 격자가 주어집니다.
-1은 해당 칸에 검은색 돌이, 0은 빨간색 폭탄이,
1이상 m이하의 숫자는 빨간색과는 다른 서로 다른 색의 폭탄이 들어가 있음을 의미합니다.

더 이상 폭탄 묶음이 없을 때까지 계속 반복하려 합니다.

1. 현재 격자에서 크기가 가장 큰 폭탄 묶음을 찾습니다.
폭탄 묶음이란 2개 이상의 폭탄으로 이루어져 있어야 하며,
모두 같은 색깔의 폭탄으로만 이루어져 있거나 빨간색 폭탄을 포함하여
정확히 2개의 색깔로만 이루어진 폭탄을 의미합니다.

다만, 빨간색 폭탄으로만 이루어져 있는 경우는 올바른 폭탄 묶음이 아니며,

모든 폭탄들이 전부 격자 상에서 연결되어 있어야만 합니다.

여기서 연결되어 있다는 말은, 폭탄 묶음 내 한 폭탄으로부터 시작하여 상하좌우
인접한 곳에 있는 폭탄 묶음 내 폭탄으로만 이동했을 때 모든 폭탄들에 도달이 가능함을 의미합니다.


* 크기가 큰 폭탄 묶음들 중 빨간색 폭탄이 가장 적게 포함된 것 부터 선택
* 오른쪽 아래 있는 것이 기준 (행이 크고 열이 작은)


2. 선택된 폭탄 묶음에 해당되는 폭탄들을 전부 제거합니다. ** 점수계산 터진 폭탄 수 ** 2
폭탄들이 제거된 이후에는 중력이 작용하여 위에 있던 폭탄들이 떨어지지만,
돌은 유지

3. 반시계 방향으로 회전
4. 다시 중력 작용

터질 폭탄 없을 때 까지 반복
"""
N, M = map(int, input().split())
pan = [list(map(int, input().split())) for _ in range(N)]


def rotate_pan():
    global pan

    pan = list(map(list, zip(*pan)))[::-1]


def find_bombs():
    bombs = []
    visited = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if pan[i][j] > 0 and not visited[i][j]:
                num = pan[i][j]
                red = 0
                b = 1
                visited[i][j] = 1
                q = [(i, j)]
                memory = {(i, j)}
                where_x = i
                where_y = j
                red_visited = [[0 for _ in range(N)] for _ in range(N)]
                while q:
                    x, y = q.pop(0)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                            if pan[nx][ny] == 0 and not red_visited[nx][ny]:  # 빨간 색일 경우
                                red += 1
                                b += 1
                                q.append((nx, ny))
                                red_visited[nx][ny] = 1
                                memory.add((nx, ny))
                            elif pan[nx][ny] == num:  # 같은 색일 경우
                                b += 1
                                q.append((nx, ny))
                                visited[nx][ny] = 1
                                memory.add((nx, ny))
                                if where_x < nx:
                                    where_x, where_y = nx, ny
                                elif where_x == nx:
                                    if where_y > ny:
                                        where_x, where_y = nx, ny

                if b > 1:
                    bombs.append([-b, red, -where_x, where_y, memory])
    bombs.sort()
    return bombs[0] if bombs else [0, 0, 0, 0, 0]


def explosion(where):
    for x, y in where:
        pan[x][y] = -2


def gravity():
    for y in range(N):
        for x in range(N-2, -1, -1):
            if pan[x][y] >= 0:
                nx, ny = x, y
                while nx < N-1:
                    if pan[nx+1][ny] == -2 and pan[nx][ny] >= 0:
                        pan[nx+1][ny], pan[nx][ny] = pan[nx][ny], -2
                        nx += 1
                    else:
                        break

def print_pan(what):
    print(f"=========={what}============")
    for p in pan:
        print(p)


score = 0
while True:
    bomb_num, red_num, p, q, where_bombs = find_bombs()
    # print(bomb_num, red_num, p, q, where_bombs)
    if where_bombs == 0:
        break
    score += (bomb_num ** 2)
    explosion(where_bombs)
    gravity()
    rotate_pan()
    gravity()
print(score)