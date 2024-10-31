const stdin = require("fs").readFileSync("/dev/stdin").toString().trim().split("\n");
const input = (() => {
    let line = 0;
    return () => stdin[line++];
})()

const [n, m, start] = input().split(" ").map(Number);
const graph = Array.from({ length: n + 1 }, () => []);

for (let i = 0; i < m; i++) {
    const [a, b] = input().split(" ").map(Number);
    graph[a].push(b)
    graph[b].push(a)
}

for (let j = 0; j < n+1; j++) {
    const temp = graph[j]
    temp.sort((a, b) => a - b)
    graph[j] = [...temp]
}

const bfs = (n, s, g) => {
    const bfsAnswer = [s];
    const visited = Array(n+1).fill(false);
    visited[s] = true;
    const q = [s];
    while (q.length > 0) {
        const x = q.shift();
        for (const w of g[x]) {
            if (!visited[w]) {
                visited[w] = true;
                q.push(w);
                bfsAnswer.push(w);
            }
        }
    }
    return bfsAnswer;
}

const dfs = (n, s, g) => {
    const dfsAnswer = [];
    const visited = Array(n + 1).fill(false);

    const recursiveDfs = (x) => {
        visited[x] = true;
        dfsAnswer.push(x);

        for (const w of g[x]) {
            if (!visited[w]) {
                recursiveDfs(w);
            }
        }
    };

    recursiveDfs(s);
    return dfsAnswer;
};

const ans1 = dfs(n,start,graph)
console.log(...ans1);
const ans2 = bfs(n,start,graph)
console.log(...ans2);