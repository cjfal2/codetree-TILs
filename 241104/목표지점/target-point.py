N, M = map(int, input().split())
visited = [[-1 for _ in range(M)] for _ in range(N)]
pan = []
sx, sy = 0, 0
for n in range(N):
    temp = list(map(int, input().split()))
    for m in range(M):
        if temp[m] == 2:
            sx, sy = n, m
            visited[n][m] = 0
        elif temp[m] == 0:
            visited[n][m] = 0
    pan.append(temp)

q = [(sx, sy)]
while q:
    x, y = q.pop(0)
    for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
        nx, ny = x + dx, y + dy
        if N > nx >= 0 and M > ny >= 0 and visited[nx][ny] == -1:
            visited[nx][ny] = visited[x][y] + 1
            q.append((nx, ny))

for v in visited:
    print(*v)