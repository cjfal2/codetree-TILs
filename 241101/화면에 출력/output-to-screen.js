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
visited.add("1,0");

while (q.length > 0) {
  const [screen, clipboard, time] = q.shift();

  if (screen === S) {
    console.log(time);
    break;
  }

  for (const [s, c] of [[screen, screen], [screen + clipboard, clipboard], [screen - 1, clipboard]]) {
    if (s >= 0 && s <= 2 * S && !visited.has(`${s},${c}`)) {
      visited.add(`${s},${c}`);
      q.push([s, c, time + 1]);
    }
  }
}