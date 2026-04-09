import { GRID, CELL, BALL_TYPES } from '../utils/constants.js';

class Board {
    constructor(probability) {
        this.grid = [];
        this.probability = probability;
        this.dropInfo = null;
        this.dropProgress = 0;
    }

    create() {
        const types = ['melee', 'ranged', 'heal', 'magic', 'invalid'];
        const getRandomType = () => {
            let r = Math.random();
            let cumulative = 0;
            for (let i = 0; i < types.length; i++) {
                cumulative += this.probability[types[i]];
                if (r < cumulative) return i;
            }
            return 4;
        };

        this.grid = [];
        for (let r = 0; r < GRID; r++) {
            this.grid[r] = [];
            for (let c = 0; c < GRID; c++) {
                let type;
                do {
                    type = getRandomType();
                } while (this._wouldMatch(r, c, type));
                this.grid[r][c] = type;
            }
        }
        return this.grid;
    }

    _wouldMatch(r, c, type) {
        if (c >= 2 && this.grid[r][c - 1] === type && this.grid[r][c - 2] === type) return true;
        if (r >= 2 && this.grid[r - 1][c] === type && this.grid[r - 2][c] === type) return true;
        return false;
    }

    getCell(x, y, startX, startY) {
        const c = Math.floor((x - startX) / CELL);
        const r = Math.floor((y - startY) / CELL);
        if (r >= 0 && r < GRID && c >= 0 && c < GRID) return { r, c };
        return null;
    }

    findAllMatchGroups() {
        const allMatches = [];

        for (let r = 0; r < GRID; r++) {
            let c = 0;
            while (c < GRID) {
                const type = this.grid[r][c];
                if (type !== null) {
                    let count = 1;
                    while (c + count < GRID && this.grid[r][c + count] === type) count++;
                    if (count >= 3) {
                        const cells = [];
                        for (let i = 0; i < count; i++) cells.push({ r, c: c + i });
                        allMatches.push({ type, cells });
                    }
                    c += count;
                } else {
                    c++;
                }
            }
        }

        for (let c = 0; c < GRID; c++) {
            let r = 0;
            while (r < GRID) {
                const type = this.grid[r][c];
                if (type !== null) {
                    let count = 1;
                    while (r + count < GRID && this.grid[r + count][c] === type) count++;
                    if (count >= 3) {
                        const cells = [];
                        for (let i = 0; i < count; i++) cells.push({ r: r + i, c });
                        allMatches.push({ type, cells });
                    }
                    r += count;
                } else {
                    r++;
                }
            }
        }

        if (allMatches.length === 0) return [];

        return this._mergeGroups(allMatches);
    }

    _mergeGroups(allMatches) {
        const groups = [];
        const cellToGroup = new Map();

        for (const match of allMatches) {
            const matchSet = new Set(match.cells.map(c => `${c.r},${c.c}`));
            const touchingGroups = [];

            for (const key of matchSet) {
                if (cellToGroup.has(key)) {
                    const gid = cellToGroup.get(key);
                    if (!touchingGroups.includes(gid)) touchingGroups.push(gid);
                }
            }

            if (touchingGroups.length === 0) {
                const newGroup = { type: match.type, cells: [...match.cells] };
                groups.push(newGroup);
                const gid = groups.length - 1;
                for (const c of match.cells) cellToGroup.set(`${c.r},${c.c}`, gid);
            } else {
                let mainGroup = groups[touchingGroups[0]];
                if (touchingGroups.length > 1) {
                    for (let i = 1; i < touchingGroups.length; i++) {
                        const oldGroup = groups[touchingGroups[i]];
                        for (const c of oldGroup.cells) {
                            cellToGroup.set(`${c.r},${c.c}`, touchingGroups[0]);
                        }
                        mainGroup.cells = mainGroup.cells.concat(oldGroup.cells);
                    }
                }
                for (const c of match.cells) {
                    if (!cellToGroup.has(`${c.r},${c.c}`)) {
                        cellToGroup.set(`${c.r},${c.c}`, touchingGroups[0]);
                    }
                }
                mainGroup.cells = mainGroup.cells.concat(match.cells);
            }
        }

        return groups;
    }

    async drop() {
        if (this.dropInfo) return;

        const dropInfo = [];
        const newBoard = [];

        for (let c = 0; c < GRID; c++) {
            const nonNull = [];
            for (let r = 0; r < GRID; r++) {
                if (this.grid[r][c] !== null) {
                    nonNull.push({ type: this.grid[r][c], fromR: r });
                }
            }

            const ballsToAdd = GRID - nonNull.length;
            const newBalls = [];
            for (let i = 0; i < ballsToAdd; i++) {
                newBalls.push({ type: Math.floor(Math.random() * 5), fromR: -(i + 1) });
            }

            const column = [...newBalls, ...nonNull];

            newBoard[c] = [];
            for (let r = 0; r < GRID; r++) {
                const ball = column[r];
                let distance;
                if (ball.fromR >= 0) {
                    distance = r - ball.fromR;
                } else {
                    distance = r + 1 - ball.fromR;
                }
                dropInfo.push({ r, c, type: ball.type, distance });
                newBoard[c][r] = ball.type;
            }
        }

        await new Promise(resolve => {
            const duration = 400;
            const start = Date.now();
            const animate = () => {
                const elapsed = Date.now() - start;
                const p = Math.min(1, elapsed / duration);
                this.dropProgress = p;
                this.dropInfo = dropInfo;
                if (p < 1) {
                    requestAnimationFrame(animate);
                } else {
                    this.dropInfo = null;
                    this.dropProgress = 0;
                    for (let col = 0; col < GRID; col++) {
                        for (let row = 0; row < GRID; row++) {
                            this.grid[row][col] = newBoard[col][row];
                        }
                    }
                    resolve();
                }
            };
            requestAnimationFrame(animate);
        });
    }

    clone() {
        return this.grid.map(row => [...row]);
    }
}

export default Board;
