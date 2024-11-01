const fs = require("fs");
const stdin = (
  process.platform === "linux"
    ? fs.readFileSync("/dev/stdin").toString()
    : `4 9`
)
  .trim()
  .split("\n");

const input = (() => {
  let line = 0;
  return () => stdin[line++];
})();

const backSetting = () => {
  const [time, target] = input().split(" ").map(Number);
  const dice = [1, 2, 3, 4, 5, 6];
  const answer = [];
  const nowNumbers = [];

  const back = () => {
    if (nowNumbers.length === time) {
      const sumNumbers = nowNumbers.reduce((sum, number) => sum + number, 0);
      if (target === sumNumbers) {
        answer.push([...nowNumbers]);
      }
      return
    }
    for (let i = 0; i < 6; i++) {
      nowNumbers.push(dice[i]);
      back();
      nowNumbers.pop()
    }
  }
  back();

  return answer;
}
const answers = backSetting();
for (const answer of answers) {
  console.log(...answer);
}