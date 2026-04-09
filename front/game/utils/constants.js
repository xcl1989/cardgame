const BALL_COLORS = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#888888'];
const BALL_TYPES = ['melee', 'ranged', 'heal', 'magic', 'invalid'];
const GRID = 5;
const CELL = 60;

const TYPE_MAP = { 1: 'melee', 2: 'ranged', 3: 'magic' };
const TYPE_NAMES = { 1: '战士', 2: '弓箭手', 3: '法师' };
const TYPE_COLORS = { 1: '#ff4444', 2: '#4488ff', 3: '#ffff44' };
const TYPE_CLASS = { 1: 'warrior', 2: 'archer', 3: 'mage' };

const CANVAS_WIDTH = 310;
const CANVAS_HEIGHT = 350;

export {
    BALL_COLORS, BALL_TYPES, GRID, CELL,
    TYPE_MAP, TYPE_NAMES, TYPE_COLORS, TYPE_CLASS,
    CANVAS_WIDTH, CANVAS_HEIGHT
};
