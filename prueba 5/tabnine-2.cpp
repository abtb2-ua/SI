#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <string>
#include <sstream>

using namespace std;

enum class HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPairs,
    OnePair,
    HighCard
};

struct Hand {
    array<char, 5> cards;
    int bid;
    HandType type;
};

const map<char, int> cardValues = {
    {'2', 0}, {'3', 1}, {'4', 2}, {'5', 3}, {'6', 4}, {'7', 5}, {'8', 6}, {'9', 7},
    {'T', 8}, {'J', 9}, {'Q', 10}, {'K', 11}, {'A', 12}
};

int getCardValue(char card) {
    auto it = cardValues.find(card);
    return (it != cardValues.end()) ? it->second : -1;
}

array<int, 13> countCards(const array<char, 5>& hand) {
    array<int, 13> counts{};
    for (char card : hand) {
        counts[getCardValue(card)]++;
    }
    return counts;
}

HandType determineHandType(const array<char, 5>& hand) {
    auto counts = countCards(hand);
    vector<int> nonZeroCounts;
    for (int count : counts) {
        if (count > 0) nonZeroCounts.push_back(count);
    }
    sort(nonZeroCounts.begin(), nonZeroCounts.end(), greater<int>());

    if (nonZeroCounts[0] == 5) return HandType::FiveOfAKind;
    if (nonZeroCounts[0] == 4) return HandType::FourOfAKind;
    if (nonZeroCounts[0] == 3 && nonZeroCounts[1] == 2) return HandType::FullHouse;
    if (nonZeroCounts[0] == 3) return HandType::ThreeOfAKind;
    if (nonZeroCounts[0] == 2 && nonZeroCounts[1] == 2) return HandType::TwoPairs;
    if (nonZeroCounts[0] == 2) return HandType::OnePair;
    return HandType::HighCard;
}

bool compareHands(const Hand& a, const Hand& b) {
    if (a.type != b.type) {
        return a.type < b.type;
    }
    for (int i = 0; i < 5; i++) {
        if (a.cards[i] != b.cards[i]) {
            return getCardValue(a.cards[i]) > getCardValue(b.cards[i]);
        }
    }
    return false;
}

Hand parseHand(const string& line) {
    Hand hand;
    stringstream ss(line);
    string cards;
    ss >> cards >> hand.bid;
    copy(cards.begin(), cards.end(), hand.cards.begin());
    hand.type = determineHandType(hand.cards);
    return hand;
}

vector<Hand> readHandsFromFile(const string& filename) {
    ifstream file(filename);
    vector<Hand> hands;
    string line;
    while (getline(file, line)) {
        hands.push_back(parseHand(line));
    }
    return hands;
}

int calculateTotalWinnings(vector<Hand>& hands) {
    sort(hands.begin(), hands.end(), compareHands);
    int totalWinnings = 0;
    for (int i = 0; i < hands.size(); i++) {
        totalWinnings += hands[i].bid * (hands.size() - i);
    }
    return totalWinnings;
}

void printHandsAndRanks(const vector<Hand>& hands) {
    for (int i = hands.size(); i >= 0; i--) {
        cout << "Hand: ";
        for (char c : hands[i].cards) {
            cout << c;
        }
        cout << " is rank " << hands.size() - i << endl;
    }
}

int main() {
    vector<Hand> hands = readHandsFromFile("input.txt");
    int totalWinnings = calculateTotalWinnings(hands);
    printHandsAndRanks(hands);
    cout << "Total winnings: " << totalWinnings << endl;
    return 0;
}