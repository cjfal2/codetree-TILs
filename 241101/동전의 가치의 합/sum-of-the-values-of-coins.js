const stdin = require('fs').readFileSync("/dev/stdin").toString().trim().split("\n");
const input = (() => {
    let line = 0;
    return () => stdin[line++];
})();

let N = parseInt(input());
const coins = [7, 5, 2, 1];
const dp = Array(N + 1).fill(Infinity);
dp[0] = 0;

for (let i = 1; i <= N; i++) {
    for (let coin of coins) {
        if (i >= coin) {
            dp[i] = Math.min(dp[i], dp[i - coin] + 1);
        }
    }
}

console.log(dp[N]);