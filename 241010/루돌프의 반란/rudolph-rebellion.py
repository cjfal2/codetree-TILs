def cal_distance(ax, ay, bx, by):
    return (ax - bx) ** 2 + (ay - by) ** 2


def get_where_santas(my):  # my인 산타 번호는 제외
    temp_santas = set()
    temp_santas_where = dict()
    for key, value in santas.items():
        if value["alive"] and key != my:  # 탈락 안했으면 + 산타 번호가 아니라면
            # 단, 기절한 도중 충돌이나 상호작용으로 인해 밀려날 수는 있습니다.
            temp_santas.add(value["where"])
            temp_santas_where[value["where"]] = key
    return temp_santas, temp_santas_where


def move_dear():
    global dear_x, dear_y
    # 루돌프는 기절한 산타를 돌진 대상으로 선택할 수 있습니다.
    targets = []  # (루-산 거리, -r, -c)
    for i in range(P):
        # 산타별 거리 구하기
        santa = santas[i]
        if not santa.get("alive"):  # 탈락 산타 제외
            continue
        santa_x, santa_y = santa["where"]
        targets.append((cal_distance(dear_x, dear_y, santa_x, santa_y), -santa_x, -santa_y, i))

    # 타겟이 있을 때만
    if targets:
        targets.sort()
        target_x, target_y = -targets[0][1], -targets[0][2]
        santa_num = targets[0][-1]
        # 타겟 산타 구했으니 루돌프의 이동
        where_dear_go = []  # (이동후 산타와의 거리, -r, -c)
        for dear_dx, dear_dy in dear_directions:
            new_dear_x, new_dear_y = dear_x + dear_dx, dear_y + dear_dy
            where_dear_go.append((cal_distance(target_x, target_y, new_dear_x, new_dear_y), new_dear_x, new_dear_y, (dear_dx, dear_dy)))
        where_dear_go.sort()
        dear_x, dear_y = where_dear_go[0][1], where_dear_go[0][2]

        if (dear_x, dear_y) == (target_x, target_y):  # 루돌프 -> 산타 충돌
            crash("dear", santa_num, *where_dear_go[0][-1])


def crash(who, santa_number, crash_dx, crash_dy):
    # 산타는 crash_dxdy 를 반대로 설정해야함

    new_santa_x, new_santa_y = dear_x, dear_y  # 부딪혔으니까 루돌프자리랑 같음
    # 부딪혔으니까 스턴걸림
    santas[santa_number]["stun"] = 1

    power = C if who == "dear" else D
    santas[santa_number]["score"] += power  # 산타가 점수를 얻음

    # 산타가 밀려남
    for _ in range(power):
        new_santa_x += crash_dx
        new_santa_y += crash_dy
    # 탈락 판단
    if 0 <= new_santa_x < N and 0 <= new_santa_y < N:
        santas[santa_number]["where"] = (new_santa_x, new_santa_y)
        # 상호작용 여부 판단
        while santa_number != -1:
            santa_number, new_santa_x, new_santa_y = push_santa(santa_number, new_santa_x, new_santa_y, crash_dx, crash_dy)
            if santa_number != -1:
                santas[santa_number]["where"] = (new_santa_x, new_santa_y)
    else:
        # 넘어가서 탈락
        santas[santa_number]["alive"] = False


def push_santa(push_santa_number, push_x, push_y, dx, dy):
    temp_where_santa, temp_dict_santa = get_where_santas(push_santa_number)
    if (push_x, push_y) in temp_where_santa:  # 산타set에 이동한 좌표가 있으면
        # 부딪힌 산타가 그 방향으로 밀려나야 함
        crashed_santa_x, crashed_santa_y = push_x, push_y
        crashed_santa_num = temp_dict_santa[(crashed_santa_x, crashed_santa_y)]
        crashed_santa_x += dx
        crashed_santa_y += dy
        if (crashed_santa_x, crashed_santa_y) in temp_where_santa:
            return crashed_santa_num, crashed_santa_x, crashed_santa_y
        else:
            # 밀려난 산타가 넘어갔는지 확인
            if 0 <= crashed_santa_x < N and 0 <= crashed_santa_y < N:
                # 밀려난 산타 자리 저장
                santas[crashed_santa_num]["where"] = (crashed_santa_x, crashed_santa_y)
                return crashed_santa_num, crashed_santa_x, crashed_santa_y
            else:
                # 넘어가서 탈락
                santas[crashed_santa_num]["alive"] = False
                return -1, -1, -1
    return -1, -1, -1


def move_santa():
    # 산타는 1번부터 P번까지 순서대로 움직입니다. (난 0번부터 P-1)
    for key, value in santas.items():
        if not value["alive"] or value["stun"] > 0:
            # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
            continue
        x, y = value["where"]
        now_distance = cal_distance(dear_x, dear_y, x, y)

        temp_santa_go = []  # (거리, 방향, dx, dy)
        # 1.산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동합니다.
        for d in range(4):
            dx, dy = santa_directions[d]  # 5.산타는 상하좌우로 인접한 4방향 중 한 곳으로 움직일 수 있습니다.
            nx, ny = x + dx, y + dy
            where_santas, _ = get_where_santas(key)
            new_distance = cal_distance(dear_x, dear_y, nx, ny)

            # 4.움직일 수 있는 칸이 있더라도 만약 루돌프로부터 가까워질 수 있는 방법이 없다면 산타는 움직이지 않습니다.
            if (nx, ny) in where_santas or N <= nx or 0 > nx or N <= ny or 0 > ny or now_distance <= new_distance:
                continue  # 2.산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.

            temp_santa_go.append((new_distance, d, dx, dy, nx, ny))  # 모두 통과
        if temp_santa_go:  # 3.움직일 수 있는 칸이 없다면 산타는 움직이지 않습니다.
            # 6.이때 가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위에 맞춰 움직입니다.
            temp_santa_go.sort()
            temp = temp_santa_go[0]
            dx, dy, nx, ny = temp[2:]
            santas[key]["where"] = (nx, ny)
            # 부딪히는지 확인
            if (dear_x, dear_y) == (nx, ny):
                crash("santa", key, -dx, -dy)


def heal_santas_and_get_alive_score():
    for key, value in santas.items():
        if value["alive"]:  # 탈락 안한 애만
            value["score"] += 1
            if value["stun"] != 0:
                value["stun"] += 1  # 기절을 한 턴 세주기, 지금 기절했으면 2가 될거고 기절했던애는 3이될거임
                if value["stun"] == 3:
                    value["stun"] = 0  # 기절 풀어줌


# 첫 번째 줄에 N, M, P, C, D가 공백을 사이에 두고 주어집니다.
N, M, P, C, D = map(int, input().split())
dear_x, dear_y = map(lambda x: int(x)-1, input().split())
santas = dict()

ttt = []

for _ in range(P):
    number_santa, xxx, yyy = map(lambda x: int(x)-1, input().split())
    ttt.append((number_santa, xxx, yyy))
ttt.sort()
for number_santa, xxx, yyy in ttt:
    santas[number_santa] = {
        "where": (xxx, yyy),
        "alive": True,
        "stun": 0,
        "score": 0
    }
dear_directions = [
    (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)
]  # 8방향
santa_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상우하좌
for mmm in range(1, M+1):
    move_dear()
    move_santa()
    heal_santas_and_get_alive_score()

answer = []
for santa in santas.values():
    answer.append(santa["score"])
print(*answer)