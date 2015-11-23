// LongestChainAndFriends.cpp : Defines the entry point for the console application.
//
#include <vector>
#include <string>
#include <iostream>
using namespace std;

// what we have is an adjancency list
// try to dfs until you can't. That is 1
// next unvisited node is a new group
bool FriendsAreConnected(int a, int b, vector<string>&friends)
{
	return friends[a][b] == 'Y';
}

// you can instead pop off a queue and put back on if not a match
// See if they recognize O(V^2) vs O(V*E)
void dfs(int node, vector<string>&friends, vector<bool>&visited)
{
	for (int neighbor = 0; neighbor < friends.size(); neighbor++)
	{
		if (FriendsAreConnected(node, neighbor, friends)
			&& !visited[neighbor])
		{
			visited[neighbor] = true;
			dfs(neighbor, friends, visited);
		}
	}
}


// input is array of Y/N. Friends are directly friends when both have Y's. Friendships are transitive
// A friend circle is a group of friends who are all directly or indirectly friends with each other
// Count  the number of friend circles
int friendCircles(vector <string> friends) {
	vector<bool> visited(friends.size(), false);
	int count = 0;
	for (int node = 0; node < friends.size(); node++)
	{
		if (!visited[node])
		{
			count++;
			visited[node] = 1;
			dfs(node, friends, visited);
		}
	}
	return count;
}


// for each word, remove letter, if that word exists see if 1 + chain is higher than current
// sort of like dikjstras the rest?
#include <unordered_map>
const int badVal = -1;
// if I cared about style the dict would be global or in a class so I didn't pass it
// as is the reference makes it not that bad
int getLongestChain(string str, unordered_map<string, int>& dict)
{
	cout << str << endl;
	int localMax = 1;
	for (size_t i = 0; i < str.size(); i++)
	{
		//lazy copy
		string copy(str);
		copy.erase(i, 1);
		auto searchWordIt = dict.find(copy);
		if (searchWordIt != dict.end())
		{
			if (searchWordIt->second == badVal)
			{
				searchWordIt->second = getLongestChain(searchWordIt->first, dict);
			}

			if (searchWordIt->second != badVal)
			{
				int possibleNewMax = searchWordIt->second + 1;
				if (localMax < possibleNewMax)
				{
					localMax = possibleNewMax;
				}
			}
			else
			{
				cout << "bad!!" << endl;
			}
		}
	}
	cout << localMax << endl;
	return localMax;
}

int longest_chain(vector<string> w) {
	unordered_map<string, int> dict;
	for (auto const& word : w)
	{
		dict.insert(make_pair(word, badVal));
	}

	auto it = dict.begin();
	auto end = dict.end();
	for (; it != end; it++)
	{
		it->second = getLongestChain(it->first, dict);
	}

	int max = -1;
	// loop through for longest
	for (auto const& ans : dict)
	{
		if (ans.second > max)
		{
			max = ans.second;
		}
	}
	return max;
}

enum class TestType {friendChain, longestWordChain};
struct TestRef {
	const vector<string> input;
	int expectedOut;
	const string testName;
};

void Test(TestType type, const TestRef& ref)
{
	int result = 0;
	if (type == TestType::friendChain)
	{
		result = friendCircles(ref.input);
	}
	else if (type == TestType::longestWordChain)
	{
		result = longest_chain(ref.input);
	}

	if (result != ref.expectedOut)
	{
		cout << "found " << result << " expected " << ref.expectedOut << endl;
		throw std::exception(ref.testName.c_str());
	}
	else
	{
		cout << ref.testName << " succeeded" << endl;
	}
}

int main()
{
	// Say 0 and 1 are friends. 1 and 2 are friends. 3 and 4
	vector<string> friendGroup1{
		"YYNNN",
		"YYYNN",
		"NYYNN",
		"NNNYY",
		"NNNYY",
	};
	int expectedFriendGroup1 = 2;
	TestRef friendGroupRef1 = {
		friendGroup1,
		expectedFriendGroup1,
		"friendGroup1"
	};
	Test(TestType::friendChain, friendGroupRef1);

	vector<string> wordChain1{
		"abcd",
		"abc",
		"abd",
		"ab",
		"a",
		"b"
	};
	int expectedWordChain1 = 4;
	TestRef wordChainRef1 = {
		wordChain1,
		expectedWordChain1,
		"wordChain1"
	};
	Test(TestType::longestWordChain, wordChainRef1);

	vector<string> wordChain2{
		"abcd",
		"a",
		"defg"
	};

	TestRef wordChainRef2 = {
		wordChain2,
		1,
		"wordChain2"
	};
	Test(TestType::longestWordChain, wordChainRef2);
	
    return 0;
}

