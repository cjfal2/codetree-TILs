"""
n * n 격자
나무의 성장을 억제  초제의 경우 k의 범위만큼 대각선으로 퍼지며,  벽이 있는 경우 가로막혀서 전파되지 않습니다

1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
    => grow_trees()

2. 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행합니다.
    이때 각 칸의 나무 그루 수에서 총 번식이 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식이 되며,
    나눌 때 생기는 나머지는 버립니다. 번식의 과정은 모든 나무에서 동시에 일어나게 됩니다.
    => breed_trees()
    * 마지막에 빈칸들을 한 번에 처리해야함
    * 현재 나무 // 번식 가능 칸 수 만큼 번식칸 수 +
    * 제초제만 있는 칸이 있을 수 있음

3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제를 뿌립니다.
    나무가 없는 칸에 제초제를 뿌리면 박멸되는 나무가 전혀 없는 상태로 끝이 나지만,
    나무가 있는 칸에 제초제를 뿌리게 되면 4개의 대각선 방향으로 k칸만큼 전파되게 됩니다.
    단 전파되는 도중 벽이 있거나 나무가 아얘 없는 칸이 있는 경우,
    그 칸 까지는 제초제가 뿌려지며 그 이후의 칸으로는 제초제가 전파되지 않습니다.
    제초제가 뿌려진 칸에는 c년만큼 제초제가 남아있다가 c+1년째가 될 때 사라지게 됩니다.
    제초제가 뿌려진 곳에 다시 제초제가 뿌려지는 경우에는 새로 뿌려진 해로부터 다시 c년동안 제초제가 유지됩니다.
    => cut_tree()
    * 모든 나무에 대한 박멸 시뮬레이션을 거쳐야함
        (나무의 수가 동일한 칸이 있는 경우에는 행이 작은 순서대로, 만약 행이 같은 경우에는 열이 작은 칸에 제초제를 뿌리게 됩니다.)
    * 나무 없는 칸을 대상으로 지정할 수 도 있음 => 그럼 그냥 제초제 처리만
    * 대각선으로 한 칸씩 전진하며 뿌리기 (벽에 막힘, 나무없으면 끝)
    * 제초제 처리: 새로 들어오면 +가아니라 1로 초기화하여 c까지 다시 셈

m년 동안 총 박멸한 나무의 그루 수를 구하는 프로그램을 작성해보세요.
    => 계속 박멸한 나무 수 기록


"""


def grow_trees():
    temp_trees = dict()
    # 성장은 모든 나무에게 동시에 일어납니다.
    for tree_where in trees_place.keys():
        temp_trees[tree_where] = 0
        for dn, dm in tree_directions:
            nn, nm = tree_where[0] + dn, tree_where[1] + dm
            if N > nn >= 0 and N > nm >= 0 and (nn, nm) in trees_place:
                # 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다.
                temp_trees[tree_where] += 1
    for key, value in temp_trees.items():
        trees_place[key] += value


def breed_trees():
    new_trees = dict()
    for tree_where, tree_amount in trees_place.items():
        temp_breed = set()
        for dn, dm in tree_directions:
            nn, nm = tree_where[0] + dn, tree_where[1] + dm
            if N > nn >= 0 and N > nm >= 0:
                if (nn, nm) not in trees_place and (nn, nm) not in killar and (nn, nm) not in walls:
                    temp_breed.add((nn, nm))
        breed_num = len(temp_breed)
        if breed_num:
            breed_amount = tree_amount // breed_num
            for breed_where in temp_breed:
                if breed_where in new_trees:
                    new_trees[breed_where] += breed_amount
                else:
                    new_trees[breed_where] = breed_amount
    for new_tree, value in new_trees.items():
        trees_place[new_tree] = value


def kill_trees():
    if not trees_place:
        return 0, set()

    temp_kill_trees = []  # [-박멸 나무 수, r, c]
    temp_kill_trees_info = dict()
    for tree_where, value in trees_place.items():
        r, c = tree_where
        killing_tree = value
        temp_kill = {tree_where}
        for dx, dy in killar_directions:
            nx, ny = r, c
            for _ in range(K):
                nx += dx
                ny += dy
                if N > nx >= 0 and N > ny >= 0 and (nx, ny) not in walls:
                    if (nx, ny) in trees_place:
                        killing_tree += trees_place[(nx, ny)]
                        temp_kill.add((nx, ny))
                    else:
                        temp_kill.add((nx, ny))
                        break
                else:
                    break
        temp_kill_trees.append((-killing_tree, r, c))
        temp_kill_trees_info[tree_where] = temp_kill

    temp_kill_trees.sort()
    kill_trees_real = temp_kill_trees[0]

    # 나무 죽이기
    kx, ky = kill_trees_real[1], kill_trees_real[2]
    score = -kill_trees_real[0]
    return score, temp_kill_trees_info[(kx, ky)]


def killar_adjust(killar_where):
    for kx, ky in killar_where:
        if (kx, ky) in trees_place:
            trees_place.pop((kx, ky))
        killar[(kx, ky)] = 1

    temp = set()
    for key, value in killar.items():
        killar[key] += 1
        if killar[key] == C+2:
            temp.add(key)

    for key in temp:
        killar.pop(key)


def print_tree(what):
    print(f"{what}################")
    pan = [["0" for _ in range(N)] for _ in range(N)]
    for x, y in walls:
        pan[x][y] = "*"

    for x, y in killar.keys():
        pan[x][y] = "K"

    # print("tree")
    for k, v in trees_place.items():
        # print(k, ":", v)
        pan[k[0]][k[1]] = str(v)
    # print("killar")
    for k, v in killar.items():
        pan[k[0]][k[1]] = str(-v)
        # print(k, ":", v)
    for p in pan:
        print(p)
    print("============================")


# 첫 번째 줄에 격자의 크기 n, 박멸이 진행되는 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c
N, M, K, C = map(int, input().split())
trees_place = dict()  # (좌표): 나무 수
killar = dict()  # (좌표): 턴
walls = set()
killar_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
tree_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
answer = 0
for n in range(N):
    temp_map = list(map(int, input().split()))
    for m in range(N):
        if temp_map[m] == -1:
            walls.add((n, m))
        elif temp_map[m] > 0:
            trees_place[(n, m)] = temp_map[m]
# print_tree("원래")
for mmmmmmm in range(M):
    if not trees_place:
        break
    # print(f"-------------------턴:{mmmmmmm}-----------------------")
    grow_trees()
#     print_tree(f"{mmmmmmm}, 성장")
    breed_trees()
#     print_tree(f"{mmmmmmm}, 번식")
    s, info = kill_trees()
    answer += s
    killar_adjust(info)
#     print_tree(f"{mmmmmmm}, 죽임")
#     print(answer)
#     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(answer)