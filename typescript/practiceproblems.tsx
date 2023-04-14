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

function twoSum(nums: number[], target: number): number[] {
  const values = new Set<number>();
  for (const num of nums) {
    values.add(num)
  }
  for (let i = 0; i < nums.length; i++) {
    const num = nums[i];
    const diff = target - num;
    if (values.has(diff) && nums.indexOf(diff) !== i) {
      return [i, nums.indexOf(diff)];
    }
  }
  return [];
};

// Happy if you square each digit and add them up and repeat until you get 1
function isHappy(n: number): boolean {
  if (n === 0)
    return false;
  // get each digit, square it, add it to the sum
  const seen = new Set<number>();
  for (let i = 0; i < 100; i++) {
    let sum = 0;
    while (n > 0) {
      const digit = n % 10;
      sum += digit * digit;
      n = Math.floor(n / 10);
    }
    if (sum === 1) {
      return true;
    }
    if (seen.has(sum)) {
      return false;
    }
    seen.add(sum);
    n = sum;
  }
  return false;
};

function isPalindrome(s: string): boolean {
  let i = 0;
  let j = s.length - 1;
  while (i < j) {
    if (s[i] !== s[j]) {
      return false;
    }
    i++;
    j--;
  }
  return true;
}

function longestPalindrome(s: string): string {
  let longest = "";
  for (let i = 0; i < s.length; i++) {
    for (let j = i + 1; j <= s.length; j++) {
      const word = s.slice(i, j);
      if (word.length > longest.length && isPalindrome(word)) {
        longest = word;
      }
    }
  }
  return longest;
};

function removeStars(s: string): string {
  // remove star to the left
  // find the first star
  // this is shitty performance
  let i = s.indexOf('*');
  while (i !== -1) {
    // remove the star and the char to the left
    s = s.slice(0, i - 1) + s.slice(i + 1);
    i = s.indexOf('*');
  }
  return s;
};

function groupAnagrams(strs: string[]): string[][] {
  const words = new Map<string, string[]>();
  for (const str of strs) {
    const sorted = str.split('').sort().join('');
    if (words.has(sorted)) {
      words.get(sorted)?.push(str);
    } else {
      words.set(sorted, [str]);
    }
  }
  return Array.from(words.values());
};


function strStr(haystack: string, needle: string): number {
  // find needle in haystack
  if (needle.length === 0) {
    return 0;
  }
  for (let i = 0; i < haystack.length; i++) {
    if (haystack[i] === needle[0]) {
      const sub = haystack.slice(i, i + needle.length);
      if (sub === needle) {
        return i;
      }
    }
  }
  return -1;
};

// prequisites ai,bi means you need to take bi before ai
// return true if you can finish all courses 0 to numcourses -1
function canFinish(numCourses: number, prerequisites: number[][]): boolean {
  // a class can have multiplie prereqs
  // could do a topological sort instead

  const courseMap = new Map<number, number[]>();
  for (const [a, b] of prerequisites) {
    if (a === b) {
      return false;
    }
    courseMap.get(a)?.push(b);
  }
  const canTake = new Set<number>();
  const soFar = new Set<number>();
  const dfs = (course: number) => {
    soFar.add(course);
    const preqs = courseMap.get(course);
    if (!preqs == undefined) {
      canTake.add(course);
      return true;
    } else if (preqs) {
      for (const pre of preqs) {
        if (canTake.has(pre)) {
          continue;
        }
        if (soFar.has(pre) || !dfs(pre)) {
          return false;
        }
      }
    }

    canTake.add(course);
    return true;
  }
  // visit
  for (let i = 0; i < numCourses; i++) {
    soFar.clear()
    if (!dfs(i)) {
      return false;
    }
  }

  return canTake.size >= numCourses;
};

// console.log(canFinish(2, [[1, 0]])); // true
// console.log(canFinish(2, [[0, 1]])); // true
// console.log(canFinish(2, [[1, 0], [0, 1]])); // false cycle
// console.log(canFinish(5, [[1, 4], [2, 4], [3, 1], [3, 2]])); // true normal
// console.log(canFinish(20, [[0, 10], [3, 18], [5, 5], [6, 11], [11, 14], [13, 1], [15, 1], [17, 4]])); // false preq is it's self
// console.log(canFinish(4, [[2, 0], [1, 0], [3, 1], [3, 2], [1, 3]])); // false cycle

function validateStackSequences(pushed: number[], popped: number[]): boolean {
  // push pushed onto stack until you hit the first popped
  // then pop until you hit the next popped
  // if you hit the end of popped return true
  // if you hit the end of pushed return false
  const stack = [];
  let i = 0;
  for (const num of pushed) {
    stack.push(num);
    while (stack.length && stack[stack.length - 1] === popped[i]) {
      stack.pop();
      i++;
    }
  }
  return i === popped.length;
};

// merge accounts if the have the same email (they will have the same name)
// just because they have the same name doesn't mean they are the same accounts
// union find?
function accountsMerge(accounts: string[][]): string[][] {
  // add email to account index map
  const emailToAccount = new Map<string, number[]>();
  for (let i = 0; i < accounts.length; i++) {
    const account = accounts[i];
    for (let j = 1; j < account.length; j++) {
      const email = account[j];
      if (emailToAccount.has(email)) {
        emailToAccount.get(email)?.push(i);
      } else {
        emailToAccount.set(email, [i]);
      }
    }
  }

  // merge accounts from the email to account map
  const merged = new Set<number>();
  const mergedAccounts = [];
  for (let i = 0; i < accounts.length; i++) {
    if (merged.has(i)) {
      continue;
    }
    const account = accounts[i];
    // all merged emails for account
    const emails = new Set<string>();
    const stack = [i];
    while (stack.length > 0) {
      const accountIndex = stack.pop() || i;
      if (merged.has(accountIndex)) {
        continue;
      }
      merged.add(accountIndex);
      const account = accounts[accountIndex];
      for (let j = 1; j < account.length; j++) {
        const email = account[j];
        emails.add(email);
        const accountIndexes = emailToAccount.get(email);
        if (accountIndexes) {
          for (const index of accountIndexes) {
            if (!merged.has(index)) {

              stack.push(index);
            }
          }
        }
      }
    }
    const mergedAccount = [account[0], ...Array.from(emails).sort((a, b) => a > b ? 1 : -1)];
    mergedAccounts.push(mergedAccount);
  }
  return mergedAccounts;
};

// const accounts = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]];
// console.log(accountsMerge(accounts));


// weighted graph where distance is the weight
// find the minimum spanning tree
function minCostConnectPoints(points: number[][]): number {

  const calculateDistance = (a: number[], b: number[]) => {
    return Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
  }
  // sort all edges in increasing order of their edge weights
  // normally would do kruskal but we know its a full graph
  const edges = new Map<number, number[][]>();
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const distance = calculateDistance(points[i], points[j]);
      if (!edges.has(distance)) {
        edges.set(distance, []);
      }
      edges.get(distance)?.push([i, j]);
    }
  }
  const sortedEdges = Array.from(edges.entries()).sort((a, b) => a[0] - b[0]);
  // union find
  const parents = new Map<number, number>();
  const find = (a: number) => {
    if (!parents.has(a)) {
      parents.set(a, a);
    }
    if (parents.get(a) !== a) {
      parents.set(a, find(parents.get(a) || a));
    }
    return parents.get(a) || a;
  }
  const union = (a: number, b: number) => {
    const parentA = find(a);
    const parentB = find(b);
    if (parentA !== parentB) {
      parents.set(parentA, parentB);
    }
  }
  let cost = 0;
  for (const [distance, listOfPoints] of sortedEdges) {
    for (const points of listOfPoints) {
      const [a, b] = points;
      if (find(a) !== find(b)) {
        cost += distance;
        union(a, b);
      }
    }
  }
  return cost;
};

// console.log(minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]])); // 20

/**
 * Definition for singly-linked list.
 * class ListNode {
 *     val: number
 *     next: ListNode | null
 *     constructor(val?: number, next?: ListNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.next = (next===undefined ? null : next)
 *     }
 * }
 */
class ListNode {
  val: number
  next: ListNode | null
  constructor(val?: number, next?: ListNode | null) {
    this.val = (val === undefined ? 0 : val)
    this.next = (next === undefined ? null : next)
  }
}
function addTwoNumbers(l1: ListNode | null, l2: ListNode | null): ListNode | null {
  // add the two numbers together and keep the remainder
  // keep going through each index until its the next null
  // if the next index is null then add the remainder
  // if the remainder is 0 then return the list
  let remainder = 0;
  let head = new ListNode();
  let current = head;
  while (l1 || l2) {
    const sum = (l1?.val || 0) + (l2?.val || 0) + remainder;
    remainder = Math.floor(sum / 10);
    current.next = new ListNode(sum % 10);
    current = current.next;
    l1 = l1?.next || null;
    l2 = l2?.next || null;
  }
  if (remainder > 0) {
    current.next = new ListNode(remainder);
  }
  return head.next;
};

// bbbab becomes bbbb
// reverse the string and compute the longest common subsequence
function longestPalindromeSubseq(s: string): number {
  const reverse = s.split('').reverse().join('');
  // dp[i][j] = longest common subsequence between s[0...i] and reverse[0...j]
  const dp = new Array(s.length + 1).fill(0).map(() => new Array(s.length + 1).fill(0));
  for (let i = 1; i <= s.length; i++) {
    for (let j = 1; j <= s.length; j++) {
      if (s[i - 1] === reverse[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[s.length][s.length];
};


/**
 * Definition for singly-linked list.
 * class ListNode {
 *     val: number
 *     next: ListNode | null
 *     constructor(val?: number, next?: ListNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.next = (next===undefined ? null : next)
 *     }
 * }
 */

function swapPairs(head: ListNode | null): ListNode | null {
  //starting with head until next is null, get next, set this nodes next to that nodes next and set next to this node
  // swap every two nodes not the next node

  let current = head;
  let start = null;
  let previous = null;
  while (current && current.next) {
    const next = current.next;
    current.next = next?.next || null;
    if (start === null) {
      start = next;
    }
    next.next = current;
    // the next one we want to swap is the next one after the next one
    if (previous) {
      previous.next = next;
    }
    previous = current;
    current = current.next;
    console.log(current)
  }

  if (start === null) {
    return head;
  }
  return start;
};

/**
 * Definition for singly-linked list.
 * class ListNode {
 *     val: number
 *     next: ListNode | null
 *     constructor(val?: number, next?: ListNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.next = (next===undefined ? null : next)
 *     }
 * }
 */
// Lists sorted in ascending order
// merge k lists into one sorted list
// can instead store the values in an array and sort it and then create a linked list from it
function mergeKLists(lists: Array<ListNode | null>): ListNode | null {
  // merge the first two lists
  // merge the result with the next list
  // keep going until we have one list
  const mergeTwoLists = (l1: ListNode | null, l2: ListNode | null): ListNode | null => {
    let head = new ListNode();
    let current = head;
    while (l1 && l2) {
      if (l1.val < l2.val) {
        current.next = l1;
        l1 = l1.next;
      } else {
        current.next = l2;
        l2 = l2.next;
      }
      current = current.next;
    }
    if (l1) {
      current.next = l1;
    }
    if (l2) {
      current.next = l2;
    }
    return head.next;
  }

  if (lists.length === 0) {
    return null;
  }
  let result = lists[0];
  for (let i = 1; i < lists.length; i++) {
    result = mergeTwoLists(result, lists[i]);
  }
  return result;
};

// List is rotated to the right by k places
// In one rotation, the last element of the list becomes the first element of the list
// Find the length of the list, modulate k by the length of the list
// Find the node at the length - k index
// Set the next of that node to null
function rotateRight(head: ListNode | null, k: number): ListNode | null {
  if (head === null) {
    return null;
  }
  let length = 1;
  let current = head;
  while (current.next) {
    current = current.next;
    length++;
  }
  current.next = head;
  k = k % length;
  let newHead = head;
  for (let i = 0; i < length - k; i++) {
    current = newHead;
    if (newHead.next) {

      newHead = newHead.next;
    }
  }
  current.next = null;
  return newHead;
};

// reverse k nodes at a time and return the modified list
// if the number of nodes is not a multiple of k then left-out nodes in the end should remain as it is
// 1 2 3 4 5, k = 3 => 3 2 1 4 5
function reverseKGroup(head: ListNode | null, k: number): ListNode | null {
  // reverse the first k nodes
  // set the next of the last node to the next group
  // keep going until we have no more nodes
  const reverse = (head: ListNode | null, k: number): ListNode | null => {
    let current = head;
    let previous = null;
    let count = 0;
    while (current && count < k) {
      const next = current.next;
      current.next = previous;
      previous = current;
      current = next;
      count++;
    }
    if (count < k) {
      return reverse(previous, count);
    }
    return previous;
  }

  let current = head;
  let count = 0;
  while (current && count < k) {
    current = current.next;
    count++;
  }
  if (count === k && head) {
    const newHead = reverse(head, k);
    head.next = reverseKGroup(current, k);
    return newHead;
  }
  return head;
};


class TreeNode {
  val: number
  left: TreeNode | null
  right: TreeNode | null
  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = (val === undefined ? 0 : val)
    this.left = (left === undefined ? null : left)
    this.right = (right === undefined ? null : right)
  }
}
// number of paths where the sum of the values along the path equals targetSum
// the path does not need to start or end at the root or a leaf, but it must go downwards
// only one node can be traversed along the path
function pathSum(root: TreeNode | null, targetSum: number): number {
  // dynamic programming
  // keep track of the sum of the path
  // if the sum is equal to the target sum, increment the count
  // if the sum is greater than the target sum, return
  // if the sum is less than the target sum, keep going
  const map = new Map();
  let count = 0;
  const traverse = (node: TreeNode | null, sum: number): void => {
    if (node === null) {
      return;
    }
    sum += node.val;
    if (sum === targetSum) {
      count++;
    }
    // In the stack we have a node that we are including but don't need to
    // Try subtracting that and if we havent popped it off yet then we can use it
    if (map.has(sum - targetSum)) {
      count += map.get(sum - targetSum);
    }
    if (map.has(sum)) {
      map.set(sum, map.get(sum) + 1);
    } else {
      map.set(sum, 1);
    }
    traverse(node.left, sum);
    traverse(node.right, sum);
    // pop off this value
    map.set(sum, map.get(sum) - 1);
  }
  traverse(root, 0);
  return count;
};

// Given the root of a binary tree, return the maximum path sum of any path
// A path is a sequence of nodes where any two adjacent nodes in the sequence have an edge connecting them
// A node can only appear in the sequence at most once
// The path must go through at least one node and does not need to go through the root
// remember for trees, define your base case and just traverse baby
function maxPathSum(root: TreeNode | null): number {
  // keep track of the max sum
  // traverse the tree
  // if the sum is greater than the max sum, update the max sum
  // return the max sum
  let maxSum = -Infinity;
  const traverse = (node: TreeNode | null): number => {
    if (node === null) {
      return 0;
    }
    const left = traverse(node.left);
    const right = traverse(node.right);
    // biggest sum is this node plus the left sum or 0 plus the right sum or 0
    const sum = node.val + Math.max(left, 0) + Math.max(right, 0);
    if (sum > maxSum) {
      maxSum = sum;
    }
    // the largest sequence including this node is ending here, going to to my right or my left
    return node.val + Math.max(left, right, 0);
  }
  traverse(root);
  return maxSum;
};

// Piles of coins with their values from top to bottom
// You can fill your wallet with k coins
// if you take a coin from a pile then you can access the coin below it
// return the maximum value of coins you can get
function maxValueOfCoins(piles: number[][], k: number): number {
  // it's possible it's worth it to take the smallest coin from the top of the pile because the coins below it are bigger
  // kind of like a path finding problem
  // can only traverse down or side to side
  // keep track of the max value
  // traverse the piles
  // if the value is greater than the max value, update the max value
  // return the max value
  // can only take k coins
  // store the value you can take at each coin

  // num piles by k
  const memoize = new Array(k + 1).fill(0).map(() => new Array(piles.length).fill(-1));
  const traverse = (row: number, coinsLeft: number): number => {
    if (coinsLeft <= 0 || row >= piles.length) {
      return 0;
    }
    if (memoize[coinsLeft][row] !== -1) {
      return memoize[coinsLeft][row];
    }
    const cointCount = piles[row].length;
    const maxPickCount = Math.min(coinsLeft, cointCount);
    let result = traverse(row + 1, coinsLeft);

    let resultPickFromThisPile = 0;
    let traverseFromhere = 0;
    for (let i = 0; i < maxPickCount; i++) {
      resultPickFromThisPile += piles[row][i];
      traverseFromhere = traverse(row + 1, coinsLeft - i - 1);
      result = Math.max(result, resultPickFromThisPile + traverseFromhere);
    }
    memoize[coinsLeft][row] = result;
    return result;
  }
  return traverse(0, k);
}

// console.log(maxValueOfCoins([[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]], 7)); // 706
// console.log(maxValueOfCoins([[37, 88], [51, 64, 65, 20, 95, 30, 26], [9, 62, 20], [44]], 9)); // 494

// build a tree given the preorder and inorder traversal of that tree
// preorder is the root, left, right
// inorder is the left, root, right
function buildTree(preorder: number[], inorder: number[]): TreeNode | null {
  // base case
  if (preorder.length === 0) {
    return null;
  }

  const root = new TreeNode(preorder[0]);
  const rootIndex = inorder.indexOf(preorder[0]);
  const leftInorder = inorder.slice(0, rootIndex);
  const rightInorder = inorder.slice(rootIndex + 1);
  const leftPreorder = preorder.slice(1, leftInorder.length + 1);
  const rightPreorder = preorder.slice(leftInorder.length + 1);
  root.left = buildTree(leftPreorder, leftInorder);
  root.right = buildTree(rightPreorder, rightInorder);
  return root;
};

// console.log(buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]));

function findMinHeightTrees(n: number, edges: number[][]): number[] {
  // if there is only one node, return that node
  // if there are two nodes, return those nodes
  // if there are more than two nodes, find the node with the least amount of edges
  // remove that node and its edges
  // repeat until there are only two nodes left
  // return those two nodes
  if (n === 1) {
    return [0];
  }
  const graph = new Array<number>(n).fill(0).map(() => new Array<number>());
  for (let i = 0; i < edges.length; i++) {
    const [a, b] = edges[i];
    graph[a].push(b);
    graph[b].push(a);
  }
  let leaves = new Array<number>();
  for (let i = 0; i < graph.length; i++) {
    if (graph[i].length === 1) {
      leaves.push(i);
    }
  }
  while (n > 2) {
    n -= leaves.length;
    const newLeaves = [];
    for (let i = 0; i < leaves.length; i++) {
      const leaf = leaves[i];
      const neighbor = graph[leaf][0];
      graph[neighbor] = graph[neighbor].filter(node => node !== leaf);
      if (graph[neighbor].length === 1) {
        newLeaves.push(neighbor);
      }
    }
    leaves = newLeaves;
  }
  return leaves;
};

// find lowest common ancestor of two nodes in a binary tree
function widthOfBinaryTree(root: TreeNode | null): number {
  // find the leaves of the tree
  // the widest with is the lowest depth of the tree with at least two leaves

  // leaves is an array of arrays
  const leaves = new Array<bigint[]>();
  const traverse = (node: TreeNode | null, depth: number, index: bigint) => {
    if (node === null) {
      return;
    }
    if (leaves[depth] === undefined) {
      leaves[depth] = [];
    }
    leaves[depth].push(BigInt(index));
    traverse(node.left, depth + 1, index * BigInt(2));
    traverse(node.right, depth + 1, index * BigInt(2) + BigInt(1));
  }
  traverse(root, 0, BigInt(0));
  let maxWidth = BigInt(1);
  for (let i = 0; i < leaves.length; i++) {
    const leaf = leaves[i];
    if (leaf.length > 1) {
      maxWidth = maxWidth > leaf[leaf.length - 1] - leaf[0] + BigInt(1) ? maxWidth : leaf[leaf.length - 1] - leaf[0] + BigInt(1);
    }
  }
  return Number(maxWidth);
};

function numberOfPeopleOnTheBus(busStops: [number, number][]): number {
  let peopleOnTheBus = 0;
  for (let i = 0; i < busStops.length; i++) {
    peopleOnTheBus += busStops[i][0] - busStops[i][1];
  }
  return peopleOnTheBus;
}

// # How many days does the patient have drugs on hand to take.
// #
// # Numerator: Number of days in date range with meds on hand
// # Denominator: Days in range
// #
// #
// #
// # For this problem lets assume each patient is taking a single drug
// # and they must take exactly one pill a day
// # We will work off of a simplified calendar that starts at 0 and goes up one integer at a time.
// #
// # 0---1---2---3---4---5---6---7---8---9---10---11---12---13---14
// # fills = [{ day:  , amount:  }, { day:  , amount:  }]
// #
// #
// #

// # RxFill
// #   day: int
// #   amount: int
// #
// # def pdc(fills: List[RxFill], start_day: int, end_day: int) -> float:
// #   # fills is sorted by day ascending
// #   # start_day <= end_day
// #   pass
// #
// #
// #
// # fills = [{ day: 2, amt: 2 }, { day: 8, amt: 2 }]
// # 0 - 9
// # 4/10 = .4
// start: 0 end: 9

// give patients an experiecne that helps them stay on drugs
// portion of days covered over the days we have covered
// 0 one day at at time, one pill a day
interface RxFill {
  day: number;
  amount: number;
}

// including start and end day
// once they pick up, we assume they are taking it
// 0 1 2 3 4 5 6 7 8 9
// N Y Y N N N N Y Y N
// fills are sorted by day
/// can fill up even though you havent used up your pills
// scan through fills, add amount to meds left
// count through days

// can get fills outside the timeframe
// could have a big fill up before the start day
function pdc(fills: RxFill[], start_day: number, end_day: number): number {
  if (fills.length === 0) {
    return 0;
  }
  let earliestDay = fills[0].day;
  let lastDay = fills[fills.length - 1].day + fills[fills.length - 1].amount - 1;

  earliestDay = Math.min(earliestDay, start_day);
  lastDay = Math.max(lastDay, end_day);

  // how many pills they have on hand from start date to end date
  let pillsOnHand = 0;
  let daysWithMeds = 0;
  let fillIndex = 0;
  for (let day = earliestDay; day <= lastDay; day++) {
    if (fillIndex < fills.length && fills[fillIndex].day === day) {
      // fill up
      pillsOnHand += fills[fillIndex].amount;
      fillIndex++;
    }
    if (pillsOnHand) {
      pillsOnHand--;
      if (day >= start_day && day <= end_day) {
        daysWithMeds++;
      }
    }
  }

  return daysWithMeds / (end_day - start_day + 1);
}

// console.log(pdc([{ day: 2, amount: 2 }, { day: 8, amount: 2 }], 0, 9)); // .4
// console.log(pdc([{ day: 2, amount: 2 }, { day: 8, amount: 2 }], 5, 9)); // .4

// high level explanation
// Implement something similar to uber
// drivers driving aroudn
// riders closest ride

// driver service having some idea of each drivers location
// rider request service -> cab finder service
// drivers will periodically send up their location to the driver service
// when you make a request for a ride send up your location, -> cab finder service, do a calc for all drivers in a location bloc
// for the cab location service ill put them all in 10 mile square blocks

// poor mans dns for location grouping of cabs
// partition drivers by avaialble drivers and ending trips
// time to end trip plus distance

// want to send the request to 5 drivers and the first driver who accepts the ride will be connnected
// rider service, find drievrs close -> pns to each drivers phone,
// driver choosing service -> send an accept one person hits accept -> update your ride request db with accepted driver -> thing watching updates on the ride tells the driver and rider
// driver choosing service or some other watcher tells all the drivesr who got that psn the ride is no longer available

