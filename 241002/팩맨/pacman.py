from collections import defaultdict

def spawn_egg():
    global where_egg
    # 몬스터 위치와 방향을 복제
    where_egg = defaultdict(list)
    for pos, directions in where_monster.items():
        where_egg[pos] = directions[:]
    return

def move_monster():
    global where_monster, pan, packman

    ghosts = set()
    new_pan = [[[] for _ in range(4)] for _ in range(4)]
    for where_ghost in where_ghosts:
        for gx, gy in where_ghost:
            ghosts.add((gx, gy))

    new_monster = defaultdict(list)
    for (x, y), directions in where_monster.items():
        for d in directions:
            for direction in range(8):
                nd = (d + direction) % 8
                dx, dy = monster_direction[nd]
                nx, ny = x + dx, y + dy
                if 0 <= nx < 4 and 0 <= ny < 4 and (nx, ny) not in ghosts and (nx, ny) != packman:
                    new_monster[(nx, ny)].append(nd)
                    new_pan[nx][ny].append(nd)
                    break
            else:
                new_monster[(x, y)].append(d)
                new_pan[x][y].append(d)

    where_monster = new_monster
    pan = new_pan
    return


def move_choice_packman():
    global packman, packman_go, packman_score

    if len(packman_go) == 3:
        nx, ny = packman
        score = 0
        kill_monster = []
        for go in packman_go:
            dx, dy = packman_direction[go]
            nx += dx
            ny += dy
            if 0 <= nx < 4 and 0 <= ny < 4:
                if pan[nx][ny]:
                    if (nx, ny) not in kill_monster:
                        score += len(pan[nx][ny])
                        kill_monster.append((nx, ny))
            else:
                return
        packman_score.append((-score, *packman_go, kill_monster, (nx, ny)))
        return

    for d in range(4):
        packman_go.append(d)
        move_choice_packman()
        packman_go.pop()

def disappear_ghost():
    if len(where_ghosts) == 3:
        where_ghosts.pop(0)
    return

def born_egg():
    global where_egg
    for (ex, ey), ed_list in where_egg.items():
        for ed in ed_list:
            where_monster[(ex, ey)].append(ed)
            pan[ex][ey].append(ed)
    where_egg = defaultdict(list)
    return

m, t = map(int, input().split())  # 몬스터의 마리 수 m과 진행되는 턴의 수 t
r, c = map(lambda x: int(x) - 1, input().split())  # 팩맨의 격자에서의 초기 위치 r, c
packman = (r, c)
packman_go = []
packman_score = []
pan = [[[] for _ in range(4)] for _ in range(4)]
where_monster = defaultdict(list)
monster_direction = [
    (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)  # 상부터 반시계로 배열
]
packman_direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # 상 좌 하 우

# 그 다음 줄부터 m개의 줄에는 몬스터의 위치 r, c와 방향 정보 d가 주어집니다
for _ in range(m):
    r, c, d = map(lambda x: int(x) - 1, input().split())
    pan[r][c].append(d)
    where_monster[(r, c)].append(d)

where_ghosts = []
where_egg = defaultdict(list)

for _ in range(t):
    spawn_egg()
    move_monster()
    move_choice_packman()

    packman_score.sort()
    temp = packman_score[0][-2]
    where_ghosts.append(temp)
    for x, y in temp:
        pan[x][y] = []
        # 해당 위치에 있는 몬스터 제거
        if (x, y) in where_monster:
            del where_monster[(x, y)]

    packman = packman_score[0][-1]

    disappear_ghost()
    born_egg()
    packman_score = []

# 남아있는 몬스터의 수 계산
answer = sum(len(pan[x][y]) for x in range(4) for y in range(4))
print(answer)