/*
Given an integer n, return a string array answer (1-indexed) where:

answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
answer[i] == "Fizz" if i is divisible by 3.
answer[i] == "Buzz" if i is divisible by 5.
answer[i] == i (as a string) if none of the above conditions are true.
*/
#include <string> 
#include <vector>
#include <iostream>
#include <iterator>
#include <algorithm>

using namespace std;
class Solution {
public:
    vector<string> fizzBuzz(int n) {
        vector<string> ans;
        for (int i = 1; i <= n; i++) {
            if ((i % 3 == 0) && (i % 5 == 0)) {
                ans.push_back("FizzBuzz");
            } else if (i % 3 == 0) {
                ans.push_back("Fizz");
            } else if (i % 5 == 0) {
                ans.push_back("Buzz");
            } else {
                ans.push_back(to_string(i));
            }
        }
        return ans;
    }
};

/*
Given an integer array nums, design an algorithm to randomly shuffle the array. All permutations of the array should be equally likely as a result of the shuffling.

Implement the Solution class:

Solution(int[] nums) Initializes the object with the integer array nums.
int[] reset() Resets the array to its original configuration and returns it.
int[] shuffle() Returns a random shuffling of the array.

Input
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
Output
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

Explanation
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // Shuffle the array [1,2,3] and return its result.
                       // Any permutation of [1,2,3] must be equally likely to be returned.
                       // Example: return [3, 1, 2]
solution.reset();      // Resets the array back to its original configuration [1,2,3]. Return [1, 2, 3]
solution.shuffle();    // Returns the random shuffling of array [1,2,3]. Example: return [1, 3, 2]

Note that the input is a ref, not const so you must change the passed in deck
*/

#include <algorithm>
#include <random>       // std::default_random_engine
#include <chrono>       // std::chrono::system_clock

class ShuffleSolution {
public:
    ShuffleSolution(vector<int>& nums) : _originalNums(nums) {
         // std::vector<int> ivec(nums.size());
        //std::iota(ivec.begin(), ivec.end(), 0);
        _positions = _originalNums;
    }
    
    vector<int> reset() {
        _originalNums = _positions;
        return _originalNums;
    }
    
    vector<int> shuffle() {
        auto seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::shuffle(_originalNums.begin(), _originalNums.end(), std::default_random_engine(seed));
        return _originalNums;
    }
private:
    vector<int> &_originalNums;
    vector<int> _positions;
};

/**
 * Your Solution object will be instantiated and called as such:
 * Solution* obj = new Solution(nums);
 * vector<int> param_1 = obj->reset();
 * vector<int> param_2 = obj->shuffle();
 */

int main() {
	int test[] = { 1, 7, 4, 6, 3, 10, 2 };
    Solution sol;
    auto fizzBuzz = sol.fizzBuzz(15);

    cout << "Fizzbuzz" << endl;
    std::ostream_iterator<string> out_it (std::cout,", ");
    copy ( fizzBuzz.begin(), fizzBuzz.end(), out_it );
	return 0;
}