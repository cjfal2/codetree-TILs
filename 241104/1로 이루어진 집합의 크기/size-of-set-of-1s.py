def bfs():
    result = 0
    visited = [[0 for _ in range(M)] for _ in range(N)]
    
    for n in range(N):
        for m in range(M):
            if pan[n][m] == 1 and visited[n][m] == 0:
                visited[n][m] = 1
                q = [(n, m)]
                amount = 1
                while q:
                    x, y = q.pop(0)
                    for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                        nx, ny = x + dx , y + dy
                        if N > nx >= 0 and M > ny >= 0 and not visited[nx][ny] and pan[nx][ny]:
                            q.append((nx, ny))
                            visited[nx][ny] = 1
                            amount += 1
                result = max(result, amount)

    return result


N, M = map(int, input().split())
pan = []
zeros = set()
for n in range(N):
    temp = list(map(int, input().split()))
    pan.append(temp)
    for m in range(M):
        if temp[m] == 0:
            zeros.add((n, m))

answer = 0
for zx, zy in zeros:
    pan[zx][zy] = 1
    answer = max(answer, bfs())
    pan[zx][zy] = 0
print(answer)