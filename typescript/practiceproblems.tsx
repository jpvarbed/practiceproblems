function hammingWeight(n: number): number {
  // number of 1 bits
  // take log base 2, go from that to 0
  let numberOfOnes = 0;
  let largestOne = Math.pow(2, Math.floor(Math.log2(n)));
  while (n > 0) {
    numberOfOnes++;
    n -= largestOne;
    largestOne = Math.pow(2, Math.floor(Math.log2(n)));
  }
  return numberOfOnes;
};

function countSheep(num: number): string {
  let ans = "";
  for (let i: number = 0; i < num; i++) {
    ans += (i + 1) + " sheep...";
  }
  return ans;
}


function strEndsWith(str: string, ending: string): boolean {
  // can use .endsWith
  return str.includes(ending, str.length - ending.length);
}

function spinWords(words: string): string {
  // only spaces if more than word is present
  // if 5 or more letters reverse it
  let split = words.split(" ");
  split = split.map((word: string) => {
    if (word.length > 4) {
      word = word.split("").reverse().join("");
    }
    return word;
  });

  return split.join(" ");
}

/*
Sam Harris => S.H

patrick feeney => P.F
*/
function abbrevName(name: string): string {
  let [first, last] = name.split(" ");
  const initials = first[0].toUpperCase() + "." + last[0].toUpperCase();
  return initials;

}

// dont count highest or lowest
function sumArray(array: number[]): number {
  if (!array || array.length <= 1) return 0;
  return array.sort((a, b) => a - b).slice(1, -1).reduce((p, n) => p + n, 0);
}

/*
better solution
  const spinWords = (words: string): string => words.split(' ')
                                                        .map(m => m.length >= 5 
                                                             ? m.split('').reverse().join('') 
                                                             : m)
                                                        .join(' ')
*/

function removeChar(str: string): string {
  return str.slice(1, -1);
}

function narcissistic(value: number): boolean {
  if (value < 10) {
    return true
  }
  const numDigits = Math.ceil(Math.log10(value));
  let sum = 0;
  let temp = value;
  while (temp) {
    sum += Math.pow(temp % 10, numDigits);
    temp = Math.floor(temp / 10);
  }
  return sum === value;
}


// show all posts from their friends, latest ones first
// add friends, can ignore
// could store all the posts in one object in order
// pull them all out by user id
// there is no remove friend

type Post = {
  id: number;
  content: string;
};

class Facebook {
  constructor() {

  }

  writePost(userId: number, postContent: string): void {
    if (!this.posts.has(userId)) {
      // new user
      this.posts.set(userId, []);
    }

    this.posts.get(userId)!.push({ id: this.postCount++, content: postContent });
  }

  addFriend(user1: number, user2: number): void {
    if (!this.friendsList.has(user1)) {
      this.friendsList.set(user1, []);
    }
    if (!this.friendsList.has(user2)) {
      this.friendsList.set(user2, []);
    }

    const list1 = this.friendsList.get(user1)!;
    const list2 = this.friendsList.get(user2)!;

    if (!list1.includes(user2)) {
      list1.push(user2);
    }

    if (!list2.includes(user1)) {
      list2.push(user1);
    }
  }

  showPosts(userId: number): string[] {
    if (!this.friendsList.has(userId)) {
      return [];
    }

    this.friendsList.get(userId);

    return this.friendsList.get(userId)!.map((friendId) => {
      if (!this.posts.has(friendId)) {
        return [];
      }
      return this.posts.get(friendId);
    }).flat()
      .sort((a, b) => b!.id - a!.id)
      .map((post) => post!.content);
  }
  private postCount = 0;
  private friendsList: Map<number, number[]> = new Map();
  private posts: Map<number, Post[]> = new Map();
}

/**
 * Your Facebook object will be instantiated and called as such:
 * var obj = new Facebook()
 * obj.writePost(userId,postContent)
 * obj.addFriend(user1,user2)
 * var param_3 = obj.showPosts(userId)
 */

function duplicateCount(text: string): number {
  const counts = new Map<string, number>();
  (text || "").split("").forEach(letter => {
    const c = letter.toLowerCase();
    if (counts.get(c)) {
      counts.set(c, counts.get(c)! + 1);
    } else {
      counts.set(c, 1);
    }
  });

  let count = 0;
  counts.forEach((c: number, k: string) => { if (c > 1) { count++; } });
  return count;
}

//   function duplicateCount(text: string): number{
//   const values = text.toLowerCase();
//   const distinctValues = [... new Set(values)]; 
//   const count = (s: string) => values.split(s).length - 1 > 1 ;
//   return distinctValues.filter(value => count(value)).length;
// }


const findOdd = (items: number[]): number => {
  const uniqueItems = Array.from(new Set(items))

  for (const uniqueItem of uniqueItems) {
    const numberOccurences = items.filter(item => item === uniqueItem).length
    if (isOdd(numberOccurences)) return uniqueItem
  }

  throw new Error('none found')
}

function isOdd(num: number): boolean {
  return num % 2 === 1
}

function singleNumber(nums: number[]): number {
  // sort would take extra linear time
  let ans = 0;
  for (const n of nums) {
    ans ^= n;
  }
  return ans;
};

function subsetsWithDup(nums: number[]): number[][] {
  nums.sort();
  const subsets = new Array<number[]>();
  let indexOfFirstNewlyAddedElement = 0;
  for (let i = 0; i < nums.length; i++) {
    let startIndex = 0;
    if (nums[i] === nums[i - 1])
      startIndex = indexOfFirstNewlyAddedElement;

    indexOfFirstNewlyAddedElement = subsets.length;
    for (let j = startIndex; j < indexOfFirstNewlyAddedElement; j++) {
      const set = Array<number>(...subsets[j]);
      set.push(nums[i]);
      subsets.push(set);
    }
  }
  return subsets;
};

interface Datam {
  ts: number;
  val: string;
}
class TimeMap {
  requests: Map<string, Datam[]>;
  constructor() {
    this.requests = new Map();
  }

  set(key: string, value: string, timestamp: number): void {
    const val = this.requests.get(key);
    if (!val) {
      this.requests.set(key, [{ ts: timestamp, val: value }]);
    } else {
      val.push({ ts: timestamp, val: value });
    }
  }

  get(key: string, timestamp: number): string {
    console.log("get " + key + " timestamp: " + timestamp);
    const vals = this.requests.get(key);
    if (!vals || vals[0].ts > timestamp) {
      return "";
    }

    const index = this.binarySearch(timestamp, vals);
    console.log("index " + index);
    if (vals[index].ts > timestamp)
      return vals[index - 1].val;
    return vals[index].val;
  }

  binarySearch(timestamp: number, values: Datam[]): number {
    let start = 0;
    let end = values.length - 1;
    let mid = 0, ts, val;
    while (start <= end) {
      mid = Math.floor((start + end) / 2);
      ts = values[mid].ts;
      if (ts === timestamp)
        return mid;
      else if (ts < timestamp) {
        start = mid + 1;
      } else
        end = mid - 1;
    }
    return mid;
  }
}

/**
 * Your TimeMap object will be instantiated and called as such:
 * var obj = new TimeMap()
 * obj.set(key,value,timestamp)
 * var param_2 = obj.get(key,timestamp)
 */

class LRUCache {
  cap: number;
  map: Map<number, number>;
  constructor(capacity: number) {
    this.cap = capacity;
    this.map = new Map();
  }

  get(key: number): number {
    const val = this.map.get(key);
    if (val !== undefined) {
      this.map.delete(key);
      this.map.set(key, val);
      return val;
    } else {
      return -1;
    }
  }

  put(key: number, value: number): void {
    const val = this.map.get(key);
    if (val) {
      this.map.delete(key);
    }
    this.map.set(key, value);
    let keys = this.map.keys();
    while (this.map.size > this.cap) {
      this.map.delete(keys.next().value);
    }
  }
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * var obj = new LRUCache(capacity)
 * var param_1 = obj.get(key)
 * obj.put(key,value)
 */


// top left to right = 1
const topLeftFB = 1;
const topRightFB = -1;
const noAnswerFB = -1;
// Stuck when on grid[0][x] == topRightFB || grid[n-1[x] == topLeftRB
// stuck when this cell is 1 and the one to the right is -1

function findBallSearch(x: number, y: number, grid: number[][]): number {
  const n = grid.length;
  const m = grid[0].length;
  console.log("x" + x);
  console.log("y" + y);
  console.log("val" + grid[x][y]);

  // wall
  if (y === 0 && grid[x][y] === topRightFB) {
    console.log("wall0");
    return noAnswerFB;
  }

  // wall
  if (y === (m - 1) && grid[x][y] === topLeftFB) {
    console.log("wall1");
    return noAnswerFB;
  }

  if (grid[x][y] === topLeftFB && (grid[x][y + 1] === topRightFB)) {
    console.log("v");
    return noAnswerFB;
  }

  if (grid[x][y] === topRightFB && grid[x][y - 1] === topLeftFB) {
    return noAnswerFB;
  }


  if (x === n - 1) {
    console.log("answer " + y);
    return y + grid[x][y];
  }



  // V

  return findBallSearch(x + 1, y + grid[x][y], grid);
}
function findBall(grid: number[][]): number[] {
  const n = grid.length;
  const m = grid[0].length;
  const ans = new Array<number>();
  // starting points are grid[0][0] though grid[0][m-1]
  for (let i = 0; i < m; i++) {
    const out = findBallSearch(0, i, grid);
    ans.push(out);
  }
  return ans;
};

enum Direction {
  right = 1,
  left,
  up,
  down
}

interface Spiral {
  xmax: number;
  xmin: number;
  ymax: number;
  ymin: number;

}

function getDirection(x: number, y: number, spiral: Spiral, direction: Direction): Direction {
  switch (direction) {
    case Direction.down:
      if (x < spiral.xmax) {
        return Direction.down;
      }
      spiral.xmax -= 1;
      return Direction.left;
    case Direction.up:
      if (x > spiral.xmin) {
        return Direction.up;
      }
      spiral.xmin += 1;
      return Direction.right;
    case Direction.left:
      if (y > spiral.ymin) {
        return Direction.left;
      }
      spiral.ymin += 1;
      return Direction.up;
    case Direction.right:
      if (y < spiral.ymax) {
        return Direction.right;
      }
      spiral.ymax -= 1;
      return Direction.down;
  }
}

function spiralOrder(matrix: number[][]): number[] {
  const n = matrix.length;
  const m = matrix[0].length;

  // go until you hit a boundary
  let spiral = { xmax: n - 1, xmin: 1, ymax: m - 1, ymin: 0 };
  // 1 is right, 2 is down, 3 is left, 4 is up
  let direction = Direction.right;
  let ans = new Array<number>();
  let x = 0;
  let y = 0;
  ans.push(matrix[0][0]);
  for (let i = 1; i < n * m; i++) {

    direction = getDirection(x, y, spiral, direction);
    switch (direction) {
      case Direction.right:
        y += 1;
        break;
      case Direction.left:
        y -= 1;
        break;
      case Direction.up:
        x -= 1;
        break;
      case Direction.down:
        x += 1;
        break;
    }
    // if not a boundary, continue
    ans.push(matrix[x][y]);
  }
  return ans;
};


// find 3 ints such that their sum is closest to target
// take one number, consider all the other pairs is n^3
// 
function threeSumClosest(nums: number[], target: number): number {
  nums.sort((a: number, b: number) => { return a - b; });
  let diff = Number.MAX_SAFE_INTEGER;
  console.log(nums);
  for (let i = 0; i < nums.length; i++) {
    let lo = i + 1;
    let hi = nums.length - 1;
    while (lo < hi) {
      const sum = nums[i] + nums[lo] + nums[hi];
      if (Math.abs(target - sum) < Math.abs(diff)) {
        // found a closer diff
        diff = target - sum;
      }
      if (sum < target) {
        // try a bigger number
        ++lo;
      } else {
        --hi;
      }
    }

  }
  return target - diff;
};

// p0 starting pop
// increases at %
// aug people coming in
// p target population
const nbYear = (p0: number, percent: number, aug: number, p: number): number => {
  // your code
  const annualCount = p0 + Math.trunc(p0 * (percent / 100)) + aug;

  if (annualCount >= p) {
    return 1;
  }
  return 1 + nbYear(annualCount, percent, aug, p);
}
//   const nbYear = (p0:number, percent:number, aug:number, p:number): number => {
//   let years = 0
//   for(; p0 < p ; ++years) {
//     p0 += Math.floor(p0 * (percent/100) + aug)
//   }
//   return years
// }

function positiveSum(arr: number[]): number {
  let sum = 0;
  for (const item of arr) {
    if (item > 0) sum += item;
  }
  return sum;
  return 0;
}

//   function positiveSum(arr:number[]):number {
//   return arr.filter((e) => e >= 0).reduce((acc, e) => acc + e , 0)
// }

//   function positiveSum(arr:number[]):number {
//   return arr.reduce((sum, n) => n > 0 ? sum + n : sum, 0);
// }

function maps(x: number[]): number[] {
  return x.map((value: number, index: number, x) => value * 2);
}

//   function maps(x: number[]): number[]{
//   return x.map(value => value * 2);
// }

function number(array: string[]): string[] {
  return array.map((value: string, index: number) => (index + 1).toString() + ": " + value);
}

//   function number(array: string[]): string[]{
//   return array.map((el, i) => `${i+1}: ${el}`);
// }

function multiplicationTable(size: number): number[][] {
  // a size x size array
  const ans = new Array<Array<number>>(size);
  for (let i = 0; i < size; i++) {
    ans[i] = new Array<number>(size);
    for (let j = 0; j < size; j++) {
      ans[i][j] = (i + 1) * (j + 1);
    }
  }
  return ans;
}

/**
 * The goal of this exercise is to convert a string to a new string where each character in the new string is 
 * "(" if that character appears only once in the original string, or ")" if that character appears more than
 * once in the original string. Ignore capitalization when determining if a character is a duplicate.
 * @param word 
 * @returns 
 */
function duplicateEncode(word: string) {
  const ans = new Set<string>();
  const appearsTwice = new Set<string>();
  // mark each letter  in the word
  for (const letter of word) {
    const lower = letter.toLowerCase();
    if (ans.has(lower)) {
      appearsTwice.add(lower);
    }
    ans.add(lower);
  }
  // if the letter is in the set, it is a duplicate use ) if not use (
  let out = "";
  for (const letter of word) {
    const lower = letter.toLowerCase();
    if (appearsTwice.has(lower)) {
      out += ")";
    } else {
      out += "(";
    }
  }
  return out;
}
// function duplicateEncode(word: string){
//     // ...
//     return word
//     .toLowerCase()
//     .split('')
//     .map((a, i, w) => {
//       return w.indexOf(a) == w.lastIndexOf(a) ? '(' : ')'
//     })
//     .join('')
// }

// leetcode with robot. you don't know the graph size, but you can move in 4 directions
// function cleanRoom(robot: Robot) {
//   const directions = [[0, 1], [1, 0], [0, -1], [-1, 0]], visited = new Set();

//   function goBack() {
//     robot.turnRight();
//     robot.turnRight();
//     robot.move();
//     robot.turnRight();
//     robot.turnRight();
//   }

//   function backTrack(cell: number[], prev: number) {
//     visited.add(cell.join());
//     robot.clean();
//     for (let i = 0; i < 4; i++) {
//       const newDir = (prev + i) % 4;
//       const [x, y] = directions[newDir];
//       const newCell = [cell[0] + x, cell[1] + y];
//       if (!visited.has(newCell.join()) && robot.move()) {
//         backTrack(newCell, newDir);
//         goBack();
//       }
//       robot.turnRight();
//     }
//   }
//   backTrack([0, 0], 0);
// };

// clear out all the 1s in the island
function dfs(grid: string[][], i: number, j: number) {
  if (i < 0 || i >= grid.length || j < 0 || j >= grid[i].length || grid[i][j] === '0') {
    return;
  }
  grid[i][j] = '0';
  dfs(grid, i - 1, j);
  dfs(grid, i + 1, j);
  dfs(grid, i, j - 1);
  dfs(grid, i, j + 1);
}

// 1s are land and 0s are water
// count number of islands
function numIslands(grid: string[][]): number {
  let count = 0;
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      if (grid[i][j] === '1') {
        count++;
        dfs(grid, i, j);
      }
    }
  }
  return count;
};

// valid if () {} [] are balanced
function isValid(s: string): boolean {
  const stack: string[] = [];
  // map with (). {} and [
  const map = new Map<string, string>();
  map.set('(', ')');
  map.set('{', '}');
  map.set('[', ']');
  for (const char of s) {
    if (map.has(char)) {
      stack.push(char);
    } else {
      const last = stack.pop();
      if (!last || map.get(last) !== char) {
        return false;
      }
    }
  }
  return stack.length === 0;

};
console.log(duplicateEncode('recede'));