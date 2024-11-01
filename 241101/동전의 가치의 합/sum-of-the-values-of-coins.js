const stdin = require('fs').readFileSync("/dev/stdin").toString().trim().split("\n");
const input = (() => {
    let line = 0;
    return () => stdin[line++];
})();

let N = parseInt(input());
const coins = [7, 5, 2, 1];
let pointer = 0;
let answer = 0;

while (N > 0) {
    const coin = coins[pointer];
    if (N >= coin) {
        N -= coin
        answer += 1
    }
    else {
        pointer++
    }
}
console.log(answer);