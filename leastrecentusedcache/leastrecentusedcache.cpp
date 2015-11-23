// leastrecentusedcache.cpp : Defines the entry point for the console application.
//

//How would you implement an LRU cache using just a *single container* ? i.e.map or unordered_map ?
//The cache must support operations :
//1. Value_t find(key_t) - find a certain value in cache
//2. Insert(key_t, value_t) insert a new value to the cache(with optionally deleteing an LRU entry)
//[http://www.careercup.com/question?id=5747511056662528]
//My answer :
//Linked list keeps track of LRU
//Hash map to look up ?
//Remember that if you access it you must move
//unorderedmap<key, node*>

#include <iostream>
#include <list>
#include <unordered_map>
using namespace std;

enum class operation { insert, get };

template <typename key_t, typename value_t>
struct TestInputRef {
	operation op;
	pair<key_t, value_t> item;
};

// We want LRU<int, int> and TestLRU<int, int> to be friends, but not TestLRU<int, double>
// http://web.mst.edu/~nmjxv3/articles/templates.html
template <typename key_t, typename value_t>
void TestLRU(const vector<TestInputRef<key_t, value_t>>& input, const vector<pair<key_t, value_t>>& reference, size_t testSize);

// on insert, check if need to kick out
template <typename key_t, typename value_t>
class LRU
{
public:
	LRU(size_t max) : m_max(max)
	{

	}

	value_t Find(key_t k)
	{
		// just testing. dont ensure exists
		auto it = m_map.find(k);
		m_list.splice(m_list.begin(), m_list, it->second);
		return it->second->second;
	}

	void Insert(key_t k, value_t v)
	{
		// let the person insert key twice. lazy
		m_list.emplace_front(make_pair(k, v));
		m_map.insert(make_pair(k, m_list.begin()));
		clean();
		return;
	}

private:
	using CacheItem = pair<key_t, value_t>;
	list<CacheItem> m_list;
	//decltype(m_list.begin()) returns C2100 illegal indirection
	using CacheIterator = typename list<CacheItem>::iterator;
	using ConstCacheIterator = typename list<CacheItem>::const_iterator;

	// For lazy testing
	ConstCacheIterator getIterator()
	{
		return m_list.cbegin();
	}

	void clean()
	{
		while (m_map.size() > m_max)
		{
			// remember end isn't an actual elt
			auto lastIt = m_list.end();
			lastIt--;
			m_map.erase(lastIt->first);
			m_list.pop_back();
		}
	}

	unordered_map<key_t, CacheIterator> m_map;
	size_t m_max = 0;
	// Need to ensure global namespace to find friend
	// http://stackoverflow.com/questions/3230562/friend-function-cannot-access-private-function-if-class-is-under-a-namespace
	friend void ::TestLRU(const vector<TestInputRef<key_t, value_t>>& input, const vector<pair<key_t, value_t>>& reference, size_t testSize);
};

template <typename key_t, typename value_t>
void TestLRU(const vector<TestInputRef<key_t, value_t>>& input, const vector<pair<key_t, value_t>>& reference, size_t testSize)
{
	cout << "new test" << endl;
	LRU<key_t, value_t> testCache(testSize);
	for (auto const& action : input)
	{
		if (action.op == operation::insert)
		{
			testCache.Insert(action.item.first, action.item.second);
		}
		else
		{
			testCache.Find(action.item.first);
		}
	}
	auto cit = testCache.getIterator();
	for (auto const& ref : reference)
	{
		bool keyEqual = cit->first == ref.first;
		bool valueEqual = cit->second == ref.second;
		cout << "For:\t" << ref.first << "\tkey:\t" << keyEqual << "\tvalue:\t" << valueEqual << endl;
		cit++;
	}
}

int main() {
	const vector<TestInputRef<int, int>> input1 = {
		{operation::insert, make_pair(0, 0)},
		{operation::insert, make_pair(1, 1)},
		{operation::insert, make_pair(2, 2)},
		{operation::insert, make_pair(3,3)}
	};

	const vector<pair<int, int>> output1 =
	{
		make_pair(3,3), make_pair(2, 2), make_pair(1, 1), make_pair(0, 0)
	};

	size_t testSize1 = 4;

	const vector<TestInputRef<int, int>> findInput1 = {
		{ operation::insert,	make_pair(0, 0) },
		{ operation::insert,	make_pair(1, 1) },
		{ operation::insert,	make_pair(2, 2) },
		{ operation::get,		make_pair(0, 0) },
		{ operation::insert,	make_pair(3, 3) },
	};

	const vector<pair<int, int>> findOutput1 =
	{
		make_pair(3,3), make_pair(0, 0), make_pair(2, 2)
	};

	size_t findSize1 = 3;

	TestLRU<int, int>(input1, output1, testSize1);
	TestLRU<int, int>(findInput1, findOutput1, findSize1);
	cout << "done" << endl;
	return 0;
}


