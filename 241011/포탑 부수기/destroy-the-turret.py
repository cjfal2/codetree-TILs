def set_attacker_target(turn):
    candidate = []  # [공격력(낮은순), 언제 공격 (높은거: 최근), 행+열(높은거), 열(높은거), 좌표]
    for tower_place in where_tower:
        tower_information = towers[tower_place]
        a_attack = tower_information["attack"]
        a_when = -tower_information["when"]
        a_nm_sum = -sum(tower_place)
        a_m = -tower_place[1]
        candidate.append((a_attack, a_when, a_nm_sum, a_m, tower_place))

    if len(candidate) <= 1:
        return (-1, -1), (-1, -1)

    candidate.sort()

    a_where = candidate[0][-1]
    towers[a_where]["attack"] += P
    towers[a_where]["when"] = turn

    return candidate[0][-1], candidate[-1][-1]  # 어태커 좌표, 타겟 좌표 리턴


def layzer_attack(ax, ay, tx, ty):
    visited = [[0 for _ in range(M)] for _ in range(N)]
    visited[ax][ay] = 1
    q = [(ax, ay, [])]  # x, y, 경로
    while q:
        x, y, routes = q.pop(0)
        for dx, dy in directions:
            nx = (x + dx) % N
            ny = (y + dy) % M
            if not visited[nx][ny] and towers.get((nx, ny)):
                if (nx, ny) == (tx, ty):
                    for route in routes:
                        towers[route]["attack"] -= half_damage
                    return routes, True

                visited[nx][ny] = 1
                q.append((nx, ny, routes + [(nx, ny)]))
    return [], False  # 레이저 공격 실패


def bomb_attack(ax, ay, tx, ty):
    bombed_towers = []
    for tdx, tdy in bomb_directions:  # 추가적으로 주위 8개의 방향에 있는 포탑도 피해를 입는데,
        ntx = (tx + tdx) % N
        nty = (ty + tdy) % M
        if (ntx, nty) == (ax, ay):  # 공격자는 해당 공격에 영향을 받지 않습니다
            continue

        if (ntx, nty) in where_tower:
            towers[(ntx, nty)]["attack"] -= half_damage  # 공격자 공격력의 절반 만큼의 피해를 받습니다.
            bombed_towers.append((ntx, nty))
    return bombed_towers


def remove_towers():
    for where in list(where_tower):
        if towers[where]["attack"] <= 0:
            towers.pop(where)
            where_tower.remove(where)  # 0이된 타워 부수기


def heal_towers(relations):
    for where in where_tower:
        if where not in relations:
            towers[where]["attack"] += 1


def get_high_score():
    answer = 0
    for key, value in towers.items():
        answer = max(answer, value["attack"])
    return answer


N, M, K = map(int, input().split())  # N * M, K턴
P = N + M  # 올라 가는 공격력
towers = dict()
where_tower = set()
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우하좌상
bomb_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
for v in range(N):
    temp = list(map(int, input().split()))
    for w in range(M):
        if temp[w]:
            towers[(v, w)] = {
                "attack": temp[w],
                "when": 0
            }
            where_tower.add((v, w))


for k in range(1, K + 1):
    attacker, target = set_attacker_target(k)
    if attacker == target:
        break

    damage = towers[attacker]["attack"]
    half_damage = damage // 2
    towers[target]["attack"] -= damage  # 공격 대상은 공격자 공격력 만큼의 피해를 받습니다.

    attacked_route, flag = layzer_attack(*attacker, *target)
    if not attacked_route and not flag:
        # 레이저 루트가 없을 때 포탄 공격
        attacked_route = bomb_attack(*attacker, *target)
    attacked_route.extend([attacker, target])
    remove_towers()
    heal_towers(attacked_route)
print(get_high_score())