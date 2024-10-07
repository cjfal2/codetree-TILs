"""
n x n으로 이뤄진 나선형 미로 속에 1번, 2번, 3번 몬스터들이 침략하고 있습니다.
플레이어는 격자 속 가운데 탑에서 몬스터를 제거하려고 합니다. 몬스터는 다음 방법에 따라 제거됩니다.


1. 플레이어는 상하좌우 방향 중 주어진 공격 칸 수만큼 몬스터를 공격하여 없앨 수 있습니다.

2. 비어있는 공간만큼 몬스터는 앞으로 이동하여 빈 공간을 채웁니다.
3. 이때 몬스터의 종류가 4번 이상 반복하여 나오면 해당 몬스터 또한 삭제됩니다.
    해당 몬스터들은 동시에 사라집니다.
    삭제된 이후에는 몬스터들을 앞으로 당겨주고, 4번 이상 나오는 몬스터가 있을 경우 또 삭제를 해줍니다.
    4번 이상 나오는 몬스터가 없을 때까지 반복해줍니다.

4. 삭제가 끝난 다음에는 몬스터를 차례대로 나열했을 때 같은 숫자끼리 짝을 지어줍니다.
    이후 각각의 짝을 (총 개수, 숫자의 크기)로 바꾸어서 다시 미로 속에 집어넣습니다. (그림 보는게 좋음)
    만약 새로 생긴 배열이 원래 격자의 범위를 넘는다면 나머지 배열은 무시합니다.
5. 해당 과정이 끝나면 한 라운드가 끝납니다.
    1과 3 과정에서 삭제되는 몬스터의 번호는 점수에 합쳐집니다.


첫번째 줄에는 격자의 크기 n, 총 라운드 수 m이 주어집니다.

이후 두번째 줄부터 n+1번째 줄까지 몬스터의 종류가 주어집니다. 0은 비어있는 칸을 의미합니다.

이후 m개의 줄에는 각 라운드마다의 플레이어의 공격 방향 d과 공격 칸 수 p가 주어집니다.

d는 0번부터 3번까지 각각 → ↓ ← ↑으로 주어집니다.
"""
def attack(attack_direction, attack_range):
    cnt = 0
    dx, dy = directions[attack_direction]
    # 넘어 가지는 않음
    x, y = px, py
    for _ in range(attack_range):
        x += dx
        y += dy

        cnt += pan[x][y]
        pan[x][y] = 0
    return cnt


def find_monster():
    array = []
    d = 1
    x, y = px, py - 1
    for i in range(1, len(arr)):
        dx, dy = directions[direction[d]]
        for j in range(arr[i]):
            if pan[x][y] != 0:
                array.append((x, y))
            x, y = x + dx, y + dy
        d = (d+1)%4
    return array


def push_monster(monsters):
    score = 0
    cnt = 0
    num = -1
    poped = []
    real_poped = []
    for x, y in monsters:
        if pan[x][y] != num:
            if cnt >= 4:
                score += num * cnt
                for gx, gy in poped:
                    real_poped.append((gx, gy))
            cnt = 1
            num = pan[x][y]
            poped = []
            poped.append((x, y))

        else:
            cnt += 1
            poped.append((x, y))
    if cnt >= 4:
        score += num * cnt
        for gx, gy in poped:
            real_poped.append((gx, gy))
    for x, y in real_poped:
        monsters.remove((x, y))

    return monsters, score


def re_monster(mons):
    global pan

    d = 1
    k = 0
    x, y = px, py - 1
    new_pan = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(1, len(arr)):
        dx, dy = directions[direction[d]]
        for j in range(arr[i]):
            new_pan[x][y] = pan[mons[k][0]][mons[k][1]]
            k += 1
            if k == len(mons):
                pan = new_pan[:]
                return
            x, y = x + dx, y + dy
        d = (d+1)%4
    pan = new_pan[:]


def fill_monster(mon_arr):
    global pan

    new_monsters = []
    for rx, ry in mon_arr:
        new_monsters.append(pan[rx][ry])
    real_new_monsters = []
    num = 0
    cnt = 0
    for nm in range(len(new_monsters)):
        if new_monsters[nm] != num:
            if num != 0:
                real_new_monsters.append(num)
                real_new_monsters.append(cnt)
            num = new_monsters[nm]
            cnt = 1
        else:
            cnt += 1
    real_new_monsters.append(num)
    real_new_monsters.append(cnt)

    d = 1
    e = 0
    x, y = px, py - 1
    new_pan = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(1, len(arr)):
        dx, dy = directions[direction[d]]
        for j in range(arr[i]):
            new_pan[x][y] = real_new_monsters[e]
            e += 1
            if e == len(real_new_monsters):
                pan = new_pan[:]
                return
            x, y = x + dx, y + dy
        d = (d+1)%4
    pan = new_pan[:]


N, turn = map(int, input().split())
pan = [list(map(int, input().split())) for _ in range(N)]
arr = []
for i in range(1, N):
    if i == N - 1:
        arr.extend([i, i, i])
    else:
        arr.extend([i, i])
direction = [2, 1, 0, 3]
directions = {
    0: (0, 1), # 우
    1: (1, 0), # 하
    2: (0, -1), # 좌
    3: (-1, 0) # 상
}
px, py = N//2, N//2

answer = 0
for _ in range(turn):
    d, p = map(int, input().split())
    answer += attack(d, p)
    while 1:
        mon = find_monster()
        m, s = push_monster(mon)
        answer += s
        if s == 0 or not m:
            break
        re_monster(m)
    fill_monster(m)


print(answer)