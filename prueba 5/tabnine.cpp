#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <string>

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

int get_card_value(char card) {
    auto it = cardValues.find(card);
    return (it != cardValues.end()) ? it->second : -1;
}

array<int, 13> count_cards(const array<char, 5>& hand) {
    array<int, 13> counts{};
    for (char card : hand) {
        counts[get_card_value(card)]++;
    }
    return counts;
}

HandType get_hand_type(const array<char, 5>& hand) {
    auto counts = count_cards(hand);
    vector<int> non_zero_counts;
    for (int count : counts) {
        if (count > 0) non_zero_counts.push_back(count);
    }
    sort(non_zero_counts.begin(), non_zero_counts.end(), greater<int>());

    if (non_zero_counts[0] == 5) return HandType::FiveOfAKind;
    if (non_zero_counts[0] == 4) return HandType::FourOfAKind;
    if (non_zero_counts[0] == 3 && non_zero_counts[1] == 2) return HandType::FullHouse;
    if (non_zero_counts[0] == 3) return HandType::ThreeOfAKind;
    if (non_zero_counts[0] == 2 && non_zero_counts[1] == 2) return HandType::TwoPairs;
    if (non_zero_counts[0] == 2) return HandType::OnePair;
    return HandType::HighCard;
}

vector<Hand> read_hands(const string& filename) {
    ifstream file(filename);
    string line;
    vector<Hand> hands;

    while (getline(file, line)) {
        Hand hand;
        copy(line.begin(), line.begin() + 5, hand.cards.begin());
        hand.bid = stoi(line.substr(6));
        hand.type = get_hand_type(hand.cards);
        hands.push_back(hand);
    }

    return hands;
}

bool compare_hands(const Hand& a, const Hand& b) {
    if (a.type != b.type) {
        return static_cast<int>(a.type) > static_cast<int>(b.type);
    }
    for (int i = 0; i < 5; i++) {
        if (a.cards[i] != b.cards[i]) {
            return get_card_value(a.cards[i]) < get_card_value(b.cards[i]);
        }
    }
    return false;
}

void print_hands(const vector<Hand>& hands) {
    for (int i = 0; i < hands.size(); i++) {
        cout << "Hand: ";
        for (char c : hands[i].cards) {
            cout << c;
        }
        cout << " is rank " << i + 1 << endl;
    }
}

int calculate_total_winnings(const vector<Hand>& hands) {
    int total = 0;
    for (int i = 0; i < hands.size(); i++) {
        total += hands[i].bid * (i + 1);
    }
    return total;
}

int main() {
    vector<Hand> hands = read_hands("input.txt");
    sort(hands.begin(), hands.end(), compare_hands);
    print_hands(hands);
    int total_winnings = calculate_total_winnings(hands);
    cout << "Total winnings: " << total_winnings << endl;
    return 0;
}