const stdin = require("fs").readFileSync("/dev/stdin").toString().trim().split("\n");
const input = (() => {
    let line = 0;
    return () => stdin[line++];
})()

const N = parseInt(input());
const pan = Array.from(Array(N), () => input().trim());
const direction = [[1, 0], [0, 1], [-1, 0], [0, -1]];
const answer = [0, 0];

const normal = () => {
    let sectionNumber = 0;
    const visitedNormal = Array.from(Array(N), () => Array(N).fill(0));
    for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
            if (visitedNormal[i][j]) continue;
            const color = pan[i][j]
            const q = [[i, j]];
            visitedNormal[i][j] = true;
            sectionNumber++
            while (q.length > 0) {
                const [x, y] = q.shift();
                for (const [dx, dy] of direction) {
                    const [nx, ny] = [x + dx, y + dy];
                    if (N <= nx) continue;
                    if (N <= ny) continue;
                    if (0 > nx) continue;
                    if (0 > ny) continue;
                    if (pan[nx][ny] !== color) continue;
                    if (visitedNormal[nx][ny]) continue;
                    visitedNormal[nx][ny] = true;
                    q.push([nx, ny])
                }
            }
        }
    }
    return sectionNumber;
}
answer[0] = normal();

const gr = () => {
    let sectionNumber = 0;
    const visitedGr = Array.from(Array(N), () => Array(N).fill(0));
    for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
            if (visitedGr[i][j]) continue;
            const color = pan[i][j] === "B" ? "B" : "R";
            const q = [[i, j]];
            visitedGr[i][j] = true;
            sectionNumber++
            while (q.length > 0) {
                const [x, y] = q.shift();
                for (const [dx, dy] of direction) {
                    const [nx, ny] = [x + dx, y + dy];
                    if (N <= nx) continue;
                    if (N <= ny) continue;
                    if (0 > nx) continue;
                    if (0 > ny) continue;
                    if (visitedGr[nx][ny]) continue;
                    const tempColor = pan[nx][ny] === "B" ? "B" : "R";
                    if (color !== tempColor) continue;
                    visitedGr[nx][ny] = true;
                    q.push([nx, ny])
                }
            }
        }
    }
    return sectionNumber;
}
answer[1] = gr();

console.log(...answer);