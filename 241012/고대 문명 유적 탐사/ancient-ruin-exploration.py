"""
choose_cube()

    90도씩 회전
    rotate_cube()

    bfs로 점수
    get_score()

    최종반영

이후 반복
get_score()
remove_cell()
fill_cell()

"""
from copy import deepcopy


def choose_cube():
    rotated_pans = []  # 점수, 돌아간 수, 열, 행, 후보, 돌아간 temp판
    # 5x5 니까 왼쪽 위 꼭지점 기준으로 돌려보면 됨
    for i in range(3):
        for j in range(3):  # 꼭지점 찾기
            temp_pan = deepcopy(pan)
            for t in range(3):  # 90, 180, 270
                # 돌려서 -> 점수, 돌아간 수(t), 꼭지점, 돌아간 temp판 저장
                temp_pan = rotate_cube_90(temp_pan, i, j)
                score, hoobo = get_score_bfs(temp_pan)
                rotated_pans.append((-score, t, j, i, hoobo, deepcopy(temp_pan)))

    rotated_pans.sort()
    return rotated_pans[0]


def rotate_cube_90(rotated_cube_pan, cube_x, cube_y):
    cube_array = [[0 for _ in range(3)] for _ in range(3)]
    for n in range(3):
        for m in range(3):
            cube_array[n][m] = rotated_cube_pan[n+cube_x][m+cube_y]
    cube_array = list(map(list, zip(*cube_array[::-1])))
    for n in range(3):
        for m in range(3):
            rotated_cube_pan[n+cube_x][m+cube_y] = cube_array[n][m]
    return rotated_cube_pan


def get_score_bfs(bfs_pan):

    # print("***********************")
    # for p in bfs_pan:
    #     print(*p)

    cnt = 0
    hubo = set()
    visited = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if not visited[i][j] and bfs_pan[i][j] != 0:
                visited[i][j] = 1
                num = bfs_pan[i][j]
                q = [(i, j)]
                num_amount = 1
                temp_hubo = {(i, j)}
                while q:
                    x, y = q.pop(0)
                    for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                        nx, ny = x + dx, y + dy
                        if 5 > nx >= 0 and 5 > ny >= 0 and bfs_pan[nx][ny] == num and not visited[nx][ny]:
                            num_amount += 1
                            visited[nx][ny] = 1
                            q.append((nx, ny))
                            temp_hubo.add((nx, ny))

                if num_amount >= 3:
                    cnt += num_amount
                    hubo.update(temp_hubo)
    # print(cnt, hubo)
    # print("-----------------------")
    return cnt, hubo


def remove_cell(cells):
    for x, y in cells:
        pan[x][y] = 0


def fill_cell():
    global num_lists
    # 단, 벽면의 숫자는 충분히 많이 적혀 있어 생겨날 조각의 수가 부족한 경우는 없다고 가정해도 좋습니다.
    for j in range(5):  # (1) 열 번호가 작은 순으로 조각이 생겨납니다. 만약 열 번호가 같다면
        for i in range(4, -1, -1):  # (2) 행 번호가 큰 순으로 조각이 생겨납니다
            if pan[i][j] == 0:
                pan[i][j] = num_lists.pop(0)


K, M = map(int, input().split())  # 탐사의 반복 횟수 K와 벽면에 적힌 유물 조각의 개수 M
pan = [list(map(int, input().split())) for _ in range(5)]
num_lists = list(map(int, input().split()))
answers = []
for turn in range(K):
    # print("#####################################################")
    answer = 0
    getted_score, _, _, _, will_romove, rotated_pan = choose_cube()  # 점수, 돌아간 수, 열, 행, 꼭지점, 돌아간 temp판
    if getted_score == 0:
        break
#     print(getted_score, will_romove, rotated_pan)
    pan = rotated_pan
#     for p in pan:
#         print(*p)
#     print("````````````````````")
    remove_cell(will_romove)
    fill_cell()
    answer -= getted_score
#     for p in pan:
#         print(*p)
#     print("````````````````````")
#     print(answer)
    while getted_score:
        getted_score, will_romove = get_score_bfs(pan)
#         print("!@!!!", getted_score)
        answer += getted_score
        remove_cell(will_romove)
        fill_cell()
#         for p in pan:
#             print(*p)
#         print("````````````````````")
#         print(answer)
#     print(answer,"!@#$!@#$!@#$!@#$")
    answers.append(answer)

print(*answers)