// https://adventofcode.com/2018/day/2

#include <iostream>
#include <iterator>
#include <fstream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <numeric>
#include <ranges>
#include <unordered_set>
#include <map>

using namespace std;

// Input file path (default is "input.txt")
const string INPUT = "input.txt";

// Part to solve: 1, 2 or all
const string PART = "1";

string prob1(vector<string> &data)
{
    int n2{0}, n3{0};

    for (const auto &line : data)
    {
        map<char, int> counter{};
        for (const auto &c : line)
            counter[c] += 1;
        auto values = counter | views::values;
        n2 += ranges::find(values, 2) != values.end() ? 1 : 0;
        n3 += ranges::find(values, 3) != values.end() ? 1 : 0;
    }

    return to_string(n2 * n3);
}

string prob2(vector<string> &data)
{
    for (auto a : data)
    {
        for (auto b : data)
        {
            auto diff_idx = views::iota(0, (int)a.length()) | views::filter([&](int i)
                                                                            { return a[i] != b[i]; });
            if (auto b = diff_idx.begin(); distance(b, diff_idx.end()) == 1)
                return a.erase(*b, 1);
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