#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>

using namespace std;

constexpr int CARD_VALUES = 13;

int get_card_value(char card) {
    switch (card) {
        case '2': return 0;
        case '3': return 1;
        case '4': return 2;
        case '5': return 3;
        case '6': return 4;
        case '7': return 5;
        case '8': return 6;
        case '9': return 7;
        case 'T': return 8;
        case 'J': return 9;
        case 'Q': return 10;
        case 'K': return 11;
        case 'A': return 12;
        default: return -1;
    }
}

class Hand {
public:
    array<char, 5> cards;
    int bet;
    int value;

    Hand(const array<char, 5>& cards, int bet)
        : cards(cards), bet(bet), value(get_hand_value(cards)) {}

    static int get_hand_value(const array<char, 5>& cards) {
        if (is_five_of_a_kind(cards)) return 0;
        if (is_four_of_a_kind(cards)) return 1;
        if (is_full_house(cards)) return 2;
        if (is_three_of_a_kind(cards)) return 3;
        if (is_two_pairs(cards)) return 4;
        if (is_one_pair(cards)) return 5;
        return 6;  // High card
    }

private:
    static array<int, CARD_VALUES> calculate_card_frequencies(const array<char, 5>& cards) {
        array<int, CARD_VALUES> frequencies{};
        for (char card : cards) {
            frequencies[get_card_value(card)]++;
        }
        return frequencies;
    }

    static bool is_five_of_a_kind(const array<char, 5>& cards) {
        return all_of(cards.begin(), cards.end(), [&](char card) { return card == cards[0]; });
    }

    static bool is_four_of_a_kind(const array<char, 5>& cards) {
        auto frequencies = calculate_card_frequencies(cards);
        return any_of(frequencies.begin(), frequencies.end(), [](int count) { return count == 4; });
    }

    static bool is_full_house(const array<char, 5>& cards) {
        auto frequencies = calculate_card_frequencies(cards);
        bool has_three = false, has_two = false;
        for (int count : frequencies) {
            if (count == 3) has_three = true;
            if (count == 2) has_two = true;
        }
        return has_three && has_two;
    }

    static bool is_three_of_a_kind(const array<char, 5>& cards) {
        auto frequencies = calculate_card_frequencies(cards);
        return any_of(frequencies.begin(), frequencies.end(), [](int count) { return count == 3; });
    }

    static bool is_two_pairs(const array<char, 5>& cards) {
        auto frequencies = calculate_card_frequencies(cards);
        int pair_count = count_if(frequencies.begin(), frequencies.end(), [](int count) { return count == 2; });
        return pair_count == 2;
    }

    static bool is_one_pair(const array<char, 5>& cards) {
        auto frequencies = calculate_card_frequencies(cards);
        return any_of(frequencies.begin(), frequencies.end(), [](int count) { return count == 2; });
    }
};

tuple<array<char, 5>, int> parse_line(const string& line) {
    array<char, 5> cards = {line[0], line[1], line[2], line[3], line[4]};
    int bet = stoi(line.substr(6));
    return make_tuple(cards, bet);
}

bool compare_hands(const Hand& hand1, const Hand& hand2) {
    if (hand1.value != hand2.value) {
        return hand1.value < hand2.value;
    }
    return lexicographical_compare(hand1.cards.rbegin(), hand1.cards.rend(),
                                    hand2.cards.rbegin(), hand2.cards.rend(),
                                    [](char a, char b) { return get_card_value(a) > get_card_value(b); });
}

int main() {
    ifstream input_file("input.txt");
    vector<Hand> hands;

    string line;
    while (getline(input_file, line)) {
        auto [cards, bet] = parse_line(line);
        hands.emplace_back(cards, bet);
    }

    sort(hands.begin(), hands.end(), compare_hands);

    int total_score = 0;
    for (size_t i = 0; i < hands.size(); ++i) {
        const auto& hand = hands[i];
        cout << "Hand: ";
        for (char card : hand.cards) {
            cout << card;
        }
        cout << " is rank " << i + 1 << endl;
        total_score += hand.bet * (i + 1);
    }

    cout << total_score << endl;
    return 0;
}