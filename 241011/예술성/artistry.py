def get_score():
    groups = dict()
    visited = [[0 for _ in range(N)] for _ in range(N)]
    g = 0
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                g += 1
                num = pan[i][j]
                visited[i][j] = g
                q = [(i, j)]
                cnt = 1
                temp = [(i, j)]
                while q:
                    x, y = q.pop(0)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if N > nx >= 0 and N > ny >= 0 and not visited[nx][ny] and pan[nx][ny] == num:
                            visited[nx][ny] = g
                            q.append((nx, ny))
                            temp.append((nx, ny))
                            cnt += 1
                groups[g] = {
                    "count": cnt,
                    "number": num,
                    "where": temp,
                    "side": dict(),
                }
    colabo = set()
    for g in range(1, len(groups.keys())+1):
        group = groups.get(g)
        temp_colabo = set()
        sides = dict()
        for x, y in group["where"]:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if N > nx >= 0 and N > ny >= 0:
                    tg_number = pan[nx][ny]
                    for k in groups.keys():
                        if k == g or (g, k) in colabo or (k, g) in colabo or tg_number == group["number"]:
                            continue
                        temporary_group = groups.get(k)
                        if temporary_group["number"] == tg_number and (nx, ny) not in group["where"] and (nx, ny) in temporary_group["where"]:
                            temp_colabo.update({(g, k), (k, g)})
                            if sides.get(k):
                                sides[k] += 1
                            else:
                                sides[k] = 1

        groups[g]["side"] = sides
        colabo.update(temp_colabo)

    getted_score = 0
    for a, value_a in groups.items():
        a_kan = value_a["count"]
        a_num = value_a["number"]
        for b, side_amount in value_a["side"].items():
            b_kan = groups[b]["count"]
            b_num = groups[b]["number"]

            temp_score = (a_kan + b_kan) * a_num * b_num * side_amount
            getted_score += temp_score

    return getted_score


def turn_cross():
    mx, my = M, M
    for t in range(1, M+1):
        mx -= 1
        pan[mx][my], pan[my][mx], pan[my+t][mx+t], pan[mx+t][my+t] = pan[mx+t][my+t], pan[mx][my], pan[my][mx], pan[my+t][mx+t]



def turn_pieces():
    for x, y in corners:
        piece = []
        for n in range(M):
            temp = []
            for m in range(M):
                temp.append(pan[x+n][y+m])
            piece.append(temp)
        turn_piece = list(map(list, zip(*piece[::-1])))

        for n in range(M):
            for m in range(M):
                pan[x+n][y+m] = turn_piece[n][m]


N = int(input())
M = N // 2
corners = [(0, 0), (M+1, 0), (0, M+1), (M+1, M+1)]
pan = [list(map(int, input().split())) for _ in range(N)]
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
answer = 0
answer += get_score()
for _ in range(3):

    # 십자 회전
    turn_cross()

    # 조각 회전
    turn_pieces()

    score = get_score()
    answer += score

print(answer)