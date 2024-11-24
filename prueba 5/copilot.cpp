#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

enum class HandCategory {
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
    int bet;
    HandCategory category;
};

int get_card_value(char card) {
    if (card == '2') return 0;
    if (card == '3') return 1;
    if (card == '4') return 2;
    if (card == '5') return 3;
    if (card == '6') return 4;
    if (card == '7') return 5;
    if (card == '8') return 6;
    if (card == '9') return 7;
    if (card == 'T') return 8;
    if (card == 'J') return 9;
    if (card == 'Q') return 10;
    if (card == 'K') return 11;
    if (card == 'A') return 12;
    return -1;
}

array<int, 13> count_cards(const array<char, 5>& hand) {
    array<int, 13> counts{};
    for (char card : hand) {
        counts[get_card_value(card)]++;
    }
    return counts;
}

HandCategory classify_hand(const array<char, 5>& hand) {
    auto counts = count_cards(hand);
    vector<int> non_zero_counts;
    for (int count : counts) {
        if (count > 0) non_zero_counts.push_back(count);
    }
    sort(non_zero_counts.begin(), non_zero_counts.end(), greater<int>());

    if (non_zero_counts[0] == 5) return HandCategory::FiveOfAKind;
    if (non_zero_counts[0] == 4) return HandCategory::FourOfAKind;
    if (non_zero_counts[0] == 3 && non_zero_counts[1] == 2) return HandCategory::FullHouse;
    if (non_zero_counts[0] == 3) return HandCategory::ThreeOfAKind;
    if (non_zero_counts[0] == 2 && non_zero_counts[1] == 2) return HandCategory::TwoPairs;
    if (non_zero_counts[0] == 2) return HandCategory::OnePair;
    return HandCategory::HighCard;
}

bool compare_hands(const Hand& a, const Hand& b) {
    if (a.category != b.category) {
        return a.category < b.category;
    }
    for (int i = 0; i < 5; i++) {
        if (a.cards[i] != b.cards[i]) {
            return get_card_value(a.cards[i]) > get_card_value(b.cards[i]);
        }
    }
    return false;
}

Hand parse_hand(const string& line) {
    Hand hand;
    for (int i = 0; i < 5; i++) {
        hand.cards[i] = line[i];
    }
    hand.bet = stoi(line.substr(6));
    hand.category = classify_hand(hand.cards);
    return hand;
}

vector<Hand> load_hands(const string& filename) {
    ifstream file(filename);
    vector<Hand> hands;
    string line;
    while (getline(file, line)) {
        hands.push_back(parse_hand(line));
    }
    return hands;
}

void print_hands_and_ranks(const vector<Hand>& hands) {
    for (size_t i = 0; i < hands.size(); i++) {
        cout << "Hand: ";
        for (char card : hands[i].cards) {
            cout << card;
        }
        cout << " is rank " << i + 1 << endl;
    }
}

int calculate_total_score(const vector<Hand>& hands) {
    int total_score = 0;
    for (size_t i = 0; i < hands.size(); i++) {
        total_score += hands[i].bet * (i + 1);
    }
    return total_score;
}

int main() {
    string filename = "practice.txt";
    vector<Hand> hands = load_hands(filename);

    sort(hands.begin(), hands.end(), compare_hands);

    print_hands_and_ranks(hands);

    int total_score = calculate_total_score(hands);
    cout << "Total score: " << total_score << endl;

    return 0;
}