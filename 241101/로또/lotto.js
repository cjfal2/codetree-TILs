const fs = require("fs");
const stdin = (
  process.platform === "linux"
    ? fs.readFileSync("/dev/stdin").toString()
    : `7
1 2 3 4 5 6 7`
)
  .trim()
  .split("\n");

const input = (() => {
    let line = 0;
    return () => stdin[line++];
})();

const backSetting = () => {
    const N = parseInt(input());
    const numbers = input().split(" ").map(Number);
    const result = [];
    const nowNumbers = [];

    const back = (start) => {
        if (nowNumbers.length === 6) {
            result.push([...nowNumbers]);
            return;
        }
        for (let i = start; i < N; i++) {
            nowNumbers.push(numbers[i]);
            back(i + 1);
            nowNumbers.pop();
        }
    }
    back(0);

    return result;
}

const answers = backSetting();
for (const answer of answers) {
    console.log(...answer);
}