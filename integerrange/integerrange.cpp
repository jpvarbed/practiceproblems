// integerrange.cpp : Defines the entry point for the console application.
//

//Given a list of integers, find out the biggest interval that has all its members in the given list : e.g.given list 1, 7, 4, 6, 3, 10, 2 then answer would be[1, 4].
//http ://www.careercup.com/question?id=21630672
//	1, 2, 3, 4 are in the list
//	Sorting is o(nlogn)
#include <iostream>
#include <set>
using namespace std;

int* range(const int * const arr, size_t size)
{
	cout << "size is " << size << endl;
	int *ans = new int[2];
	ans[0] = 0;
	ans[1] = -1;
	set<int> set;
	for (size_t i = 0; i < size; i++)
	{
		set.insert(arr[i]);
	}

	while (set.size() > 0)
	{
		int i = *set.begin();
		set.erase(i);
		int smaller = i;
		int larger = i;
		for (; set.size() > 0; smaller--)
		{
			auto findSmaller = smaller - 1;
			if (set.find(findSmaller) == set.end())
			{
				break;
			}
			else
			{
				set.erase(findSmaller);
			}
		}
		for (; set.size() > 0; larger++)
		{
			auto findLarger = larger + 1;
			if (set.find(findLarger) == set.end())
			{
				break;
			}
			else
			{
				set.erase(findLarger);
			}
		}

		if (larger - smaller > ans[1] - ans[0])
		{
			ans[0] = smaller;
			ans[1] = larger;
		}
	}
	return ans;
}

int main() {
	// your code goes here
	int test[] = { 1, 7, 4, 6, 3, 10, 2 };
	int *ans = range(test, sizeof(test) / sizeof(*test));
	cout << "[" << ans[0] << "," << ans[1] << "]" << endl;
	delete[] ans;
	return 0;
}