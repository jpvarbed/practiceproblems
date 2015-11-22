// longestcommonsubsequence.cpp : Defines the entry point for the console application.
//

//Given a string(1 - d array), find if there is any sub - sequence that repeats itself.Here, sub - sequence can be a non - contiguous pattern, with the same relative order.
//[http://www.careercup.com/question?id=5931067269709824]
//Abab ab is repeated
//abba none.A and b follow different order
//Acbdaghfb yes there is a followed by b at two places
//Abcdacb yes a followed by b twice
//My answer :
//Subsequence can be found with dynamic programming.
//Find longest subsequence starting with each letter.
//For strings a, b if a[i] == b[j]
//Then m[i][j] = max(1 + M[i - 1][j - 1], M[i - 1][j], m[i][j - 1]
//	Otherwise:
//M[i][j] = max(m[i - 1][j], m[i][j - 1])
//Max is then m[len(a) - 1, len(b) - 1]

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
using namespace std;

int findSub(const string& str)
{
	size_t size = str.size();
	vector<vector<int>> lookup(str.size(), vector<int>(str.size(), 0));
	for (size_t i = 0; i < size; i++)
	{
		if (str[0] == str[i])
		{
			lookup[0][i] = 1;
		}
	}

	for (size_t i = 0; i < size; i++)
	{
		if (str[0] == str[i])
		{
			lookup[i][0] = 1;
		}
	}

	for (size_t i = 1; i < size; i++)
	{
		for (size_t j = 1; j < size; j++)
		{
			if (i != j && str[i] == str[j])
			{
				lookup[i][j] = max(max(1 + lookup[i - 1][j - 1],
					lookup[i][j - 1]),
					lookup[i - 1][j]);
			}
			else
			{
				lookup[i][j] = max(lookup[i - 1][j], lookup[i][j - 1]);
			}
		}
	}

	return lookup[size - 1][size - 1];
}


int main() {
	struct TestRef {
		string in;
		int expected;
	};

	TestRef refs[] =
	{
		{ "abab", 2 },
		{ "abba", 1 },
		{ "acbdaghfb", 2 },
		{ "abcdacb", 2 }
	};

	for (auto const& ref : refs)
	{
		if (ref.expected != findSub(ref.in))
		{
			cout << "wrong for " << ref.in << endl;
		}
		else
		{
			cout << "correct for " << ref.in << endl;
		}
	}

	return 0;
}