const fs = require('fs');
const stdin = fs.readFileSync('/dev/stdin').toString().trim().split("\n");

const input = (() => {
    let line = 0;
    return () => stdin[line++];
})();

const [n, q] = input().split(" ").map(Number);
const pan = Array.from(Array(n), () => input().split(" ").map(Number));
const prefixSum = Array.from(Array(n + 1), () => Array(n + 1).fill(0));


for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= n; j++) {
        prefixSum[i][j] = pan[i - 1][j - 1]
                        + prefixSum[i - 1][j]
                        + prefixSum[i][j - 1]
                        - prefixSum[i - 1][j - 1];
    }
}

const result = [];
for (let k = 0; k < q; k++) {
    const [x1, y1, x2, y2] = input().split(" ").map(Number);

    let sum = prefixSum[x2][y2];
    if (x1 > 1) sum -= prefixSum[x1 - 1][y2];
    if (y1 > 1) sum -= prefixSum[x2][y1 - 1];
    if (x1 > 1 && y1 > 1) sum += prefixSum[x1 - 1][y1 - 1];

    result.push(sum);
}

console.log(result.join("\n"));