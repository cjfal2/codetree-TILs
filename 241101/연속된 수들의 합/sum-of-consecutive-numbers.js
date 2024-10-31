const fs = require("fs");
const stdin = (
    process.platform === "linux"
        ? fs.readFileSync("/dev/stdin").toString()
        : `15`
)
    .trim()
    .split("\n");

const input = (() => {
    let line = 0;
    return () => stdin[line++];
})();


const N = parseInt(input().trim());
let left = 0;
let right = 1;

const sumOfRange = (s, e) => {
    let sum = 0
    for (let i = s; i <= e; i++) sum+=i;
    return sum
}

let answer = 1
while (left < right) {
    const tempSum = sumOfRange(left, right);
    if (tempSum === N) {
        answer++
        right++
    }
    else if (tempSum < N) {
        right++
    }
    else {
        left++
    }
}
console.log(answer);