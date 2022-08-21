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

int main() {
	int test[] = { 1, 7, 4, 6, 3, 10, 2 };
    Solution sol;
    auto fizzBuzz = sol.fizzBuzz(15);

    cout << "Fizzbuzz" << endl;
    std::ostream_iterator<string> out_it (std::cout,", ");
    copy ( fizzBuzz.begin(), fizzBuzz.end(), out_it );
	return 0;
}