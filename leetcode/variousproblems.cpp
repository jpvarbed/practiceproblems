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
#include <stack>
#include <unordered_map>

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

/*
Implement the MinStack class:

MinStack() initializes the stack object.
void push(int val) pushes the element val onto the stack.
void pop() removes the element on the top of the stack.
int top() gets the top element of the stack.
int getMin() retrieves the minimum element in the stack.
You must implement a solution with O(1) time complexity for each function.
*/
// priority queue for min
// priority queue push is log(n)
// stack push/pop top gives all of these in o(1) but not min
// key insight point to min before me
// 6
// 7
// 8
// pop 6, points to 7

// just know the dang minimum when you are pushed in and when you pop itll be the same

class MinStack {

public:
    class StackNode{
        public:
        StackNode(int val, int min) : val(val), currentMin(min) {};
    
        int val;
        int currentMin;
    };
    
    MinStack() {
        
    }
    
    void push(int val) {
        if (s.empty()) {
            StackNode sn(val, val);
            s.push(sn);
        } else {
            int currentMin = s.top().currentMin;
            currentMin = std::min(currentMin, val);
            StackNode sn(val, currentMin);
            s.push(sn);
        }
    }
    
    void pop() {
        s.pop();
    }
    
    int top() {
        return s.top().val;
    }
    
    int getMin() {
        return s.top().currentMin;
    }
private:
    stack<StackNode> s;
};

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack* obj = new MinStack();
 * obj->push(val);
 * obj->pop();
 * int param_3 = obj->top();
 * int param_4 = obj->getMin();
 */

/*
LogAggregator(int machines, int services) Initializes the object with machines and services representing the number of machines and services in the datacenter, respectively.
void pushLog(int logId, int machineId, int serviceId, String message) Adds a log with id logId notifying that the machine machineId sent a string message while executing the service serviceId.
List<Integer> getLogsFromMachine(int machineId) Returns a list of ids of all logs added by machine machineId.
List<Integer> getLogsOfService(int serviceId) Returns a list of ids of all logs added while running service serviceId on any machine.
List<String> search(int serviceId, String searchString) Returns a list of messages of all logs added while running service serviceId where the message of the log contains searchString as a substring.
Note that:

The entries in each list should be in the order they were added, i.e., the older logs should precede the newer logs.
A machine can run multiple services more than once. Similarly, a service can be run on multiple machines.
All logId may not be ordered.
A substring is a contiguous sequence of characters within a string.
*/
class LogAggregator {
public:
    LogAggregator(int machines, int services) {
        
    }
    
    void pushLog(int logId, int machineId, int serviceId, string message) {
        auto it = machineIdToLogs.find(machineId);
        if (it == machineIdToLogs.end()) {
            machineIdToLogs.insert({machineId, {logId}});
        } else {
            it->second.push_back(logId);
        }
        
        it = serviceIdToLogs.find(serviceId);
        if (it == serviceIdToLogs.end()) {
            serviceIdToLogs.insert({serviceId, {logId}});
        } else {
            it->second.push_back(logId);
        }
        
        auto sit = serviceIdToLogMessages.find(serviceId);
        if (sit == serviceIdToLogMessages.end()) {
            serviceIdToLogMessages.insert({serviceId, {message}});
        } else {
            sit->second.push_back(message);
        }
        
    }
    
    vector<int> getLogsFromMachine(int machineId) {
        return machineIdToLogs[machineId];
    }
    
    vector<int> getLogsOfService(int serviceId) {
        return serviceIdToLogs[serviceId];
    }
    
    vector<string> search(int serviceId, string searchString) {
        auto it = serviceIdToLogMessages.find(serviceId);
        if (it != serviceIdToLogMessages.end()) {
            auto const & messages = it->second;
            vector<string> matchingLogs;
            for (auto const message : messages) {
                auto pos = message.find(searchString);
                if (pos != string::npos) {
                    matchingLogs.push_back(message);
                }
            }
            return matchingLogs;
        }
        return {};
    }
private:
    unordered_map<int, vector<int>> machineIdToLogs;
    unordered_map<int, vector<int>> serviceIdToLogs;
    unordered_map<int, vector<string>> serviceIdToLogMessages;
};

/*
DCLoadBalancer() Initializes the object.
void addMachine(int machineId, int capacity) Registers a machine with the given machineId and maximum capacity.
void removeMachine(int machineId) Removes the machine with the given machineId. All applications running on this machine are automatically reallocated to other machines in the same order as they were added to this machine. The applications should be reallocated in the same manner as addApplication.
int addApplication(int appId, int loadUse) Allocates an application with the given appId and loadUse to the machine with the largest remaining capacity that can handle the additional request. If there is a tie, the machine with the lowest ID is used. Returns the machine ID that the application is allocated to. If no machine can handle the request, return -1.
void stopApplication(int appId) Stops and removes the application with the given appId from the machine it is running on, freeing up the machine's capacity by its corresponding loadUse. If the application does not exist, nothing happens.
List<Integer> getApplications(int machineId) Returns a list of application IDs running on a machine with the given machineId in the order in which they were added. If there are more than 10 applications, return only the first 10 IDs.
*/

/*
    struct Machine {
        int id;
        int cap;
        map <int, int> applicationAndLoad;
        vector<int> appOrder;
    };

class mycompare
{
public:
    bool operator()(const Machine*a , Machine* b) const
    {
        if(a->cap == b->cap)
        {
            return a->id < b->id;
        }
        
        return a->cap > b->cap;
    }
};

std::ostream& operator<<(std::ostream& os, const Machine& p)
{
    os << "(id: "
              << p.id << ", cap: "
              << p.cap << " apps: ";
    for (auto app : p.applicationAndLoad) {
        os << " appid:" << app.first << " load: " << app.second;
    }
    os << ")";
    return os;
}

std::ostream& operator<<(std::ostream& os, const set<Machine*, mycompare> &p) {
    os << "cap +++++++++++++++"  << endl;
    for (auto const * m : p) {
        os << *m << endl;
    }
    os << "+++++++++++++";
    return os;
}
*/

#include <queue>

auto comp = [](vector<int>& a, vector<int>& b) -> bool {
    if(a[0] == b[0])
        return a[1] > b[1];
    return a[0] < b[0];
};

class DCLoadBalancer {
public:
    priority_queue<vector<int>, vector<vector<int>>, decltype(comp)> pq;// {capacity, machineId}
    unordered_map<int, int> app;// appId -> machineId
    unordered_map<int, int> load;// appId -> load
    unordered_map<int, vector<int>> mach;// machineId -> [appId]

    DCLoadBalancer() : pq(comp) {

    }

    void addMachine(int machineId, int capacity) {
        pq.push({capacity, machineId});
    }

    void removeMachine(int machineId) {
        vector<vector<int>> vv;
        while (!pq.empty()) {
            auto top = pq.top();
            pq.pop();
            if (top[1] != machineId) {
                vv.push_back(top);
            } else {
                break;
            }
        }

        for (auto v: vv) {
            pq.push(v);
        }

        for(auto appId : mach[machineId]) {            
            if(addApplication(appId, load[appId]) == -1) {
                // drop app
                app.erase(appId);
                load.erase(appId);
            }
        }

        mach.erase(machineId);
    }

    int addApplication(int appId, int loadUse) {
        if (!pq.empty()) {
            auto v = pq.top();
            pq.pop();
            if(v[0] < loadUse) {
                pq.push(v);
                return -1;    
            }
            v[0] -= loadUse;
            app[appId] = v[1];
            mach[v[1]].push_back(appId);
            pq.push(v);
            load[appId] = loadUse;
            return v[1];
        }
        return -1;
    }

    void stopApplication(int appId) {
        vector<vector<int>> vv;
        int machineId = app[appId];

        while (!pq.empty()) {
            auto top = pq.top();
            // Find machine, if not machine put into holder v that we'll re-add later
            if (top[1] == machineId) {
                top[0] += load[appId];
                pq.pop();
                pq.push(top);
                break;
            }
            vv.push_back(top);
            pq.pop();
        }

        auto it = find(mach[machineId].begin(), mach[machineId].end(), appId);
        if(it != mach[machineId].end())
            mach[machineId].erase(it);
        app.erase(appId);
        load.erase(appId);

        for (auto v: vv) {
            pq.push(v);
        }
    }

    vector<int> getApplications(int machineId) {
        if(mach[machineId].size() < 10)
            return mach[machineId];
        return vector<int>(mach[machineId].begin(), mach[machineId].begin()+10);
    }
};



/**
 * Your DCLoadBalancer object will be instantiated and called as such:
 * DCLoadBalancer* obj = new DCLoadBalancer();
 * obj->addMachine(machineId,capacity);
 * obj->removeMachine(machineId);
 * int param_3 = obj->addApplication(appId,loadUse);
 * obj->stopApplication(appId);
 * vector<int> param_5 = obj->getApplications(machineId);
 */

/**
 * Your LogAggregator object will be instantiated and called as such:
 * LogAggregator* obj = new LogAggregator(machines, services);
 * obj->pushLog(logId,machineId,serviceId,message);
 * vector<int> param_2 = obj->getLogsFromMachine(machineId);
 * vector<int> param_3 = obj->getLogsOfService(serviceId);
 * vector<string> param_4 = obj->search(serviceId,searchString);
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