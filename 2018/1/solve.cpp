// https://adventofcode.com/2018/day/1

#include <iostream>
#include <iterator>
#include <fstream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <numeric>
#include <ranges>
#include <unordered_set>

using namespace std;

// Input file path (default is "input.txt")
const string INPUT = "input.txt";

// Part to solve: 1, 2 or all
const string PART = "1";

auto toint = [](const string &line)
{ return stoi(line); };

string prob1(vector<string> &data)
{
    auto freqs = data | views::transform(toint);
    return to_string(reduce(freqs.begin(), freqs.end()));
}

string prob2(vector<string> &data)
{
    auto freqs = data | views::transform(toint);
    unordered_set<int> seen{};
    int freq{0};

    while (true)
    {
        for (const auto &f : freqs)
        {
            freq += f;
            if (!seen.insert(freq).second)
                return to_string(freq);
        }
    }
}

typedef string (*AoCFunc)(vector<string> &data);

void solve(vector<string> args, string part, string input, AoCFunc prob1, AoCFunc prob2)
{
    auto it = ranges::find(args, "-p");
    part = it != args.end() ? *next(it) : part;

    it = ranges::find(args, "-i");
    input = it != args.end() ? *next(it) : input;

    ifstream file(input);
    istream_iterator<string> head(file), tail;
    vector<string> data(head, tail);

    auto start = chrono::steady_clock::now();

    if (part == "1" || part == "all")
        cout << "Part 1: " << prob1(data) << endl;
    if (part == "2" || part == "all")
        cout << "Part 2: " << prob2(data) << endl;

    auto elapsed = chrono::steady_clock::now() - start;
    cout << "Time: " << chrono::duration<double>(elapsed).count() << " s" << endl;
}

int main(int argc, char *argv[])
{
    solve(vector<string>(argv, argv + argc), PART, INPUT, prob1, prob2);
}