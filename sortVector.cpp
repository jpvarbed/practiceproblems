#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;


void print(const vector<auto> &v)
{
	for (auto const& e : v)
	{
		cout << e << "\t";
	}
	cout << endl;
}

int main() {
	vector<int> a{ 10,	9,	8,	7,	6,	5,	4,	3,	2,	1};
	vector<int> b{ 20,	18,	16,	14,	12,	10,	8,  6,  4,  2};
	vector<int> c{ 19,	17,	15,	13,	11,	9,	7,	5,	3,	1};
	
	sort(a.begin(), a.end());
	sort(b.begin(), b.end());
	sort(c.begin(), c.end());
	print(a);	
	return 0;
}