const fs = require("fs");
const stdin = (
  process.platform === "linux"
    ? fs.readFileSync("/dev/stdin").toString()
    : `2`
)
  .trim()
  .split("\n");

const input = (() => {
  let line = 0;
  return () => stdin[line++];
})();

const S = parseInt(input());
const q = [[1, 0, 0]];
const visited = new Set();
visited.add([1, 0, 0]);
while (q.length > 0) {
  const [screen, clipboard, time] = q.shift();
  if (screen === S) {
    console.log(time);
    break;
  }
  for (const [s, c, t] of [[screen, screen, time + 1], [screen + clipboard, clipboard, time + 1], [screen - 1, clipboard, time + 1]]) {
    if (visited.has([s, c, t])) {
      continue;
    }
    visited.add([s, c, t]);
    q.push([s, c, t]);
  }
}