#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>

using namespace std;

// Enumeración para los valores de las manos
enum HandRank {
    FIVE_OF_A_KIND = 0,
    FOUR_OF_A_KIND,
    FULL_HOUSE,
    THREE_OF_A_KIND,
    TWO_PAIRS,
    ONE_PAIR,
    HIGH_CARD
};

// Representación de una carta
struct Card {
    char value;

    int getNumericValue() const {
        static const map<char, int> cardValues{
            {'2', 0}, {'3', 1}, {'4', 2}, {'5', 3}, {'6', 4}, {'7', 5},
            {'8', 6}, {'9', 7}, {'T', 8}, {'J', 9}, {'Q', 10}, {'K', 11}, {'A', 12}};
        return cardValues.at(value);
    }
};

// Representación de una mano
struct Hand {
    array<Card, 5> cards;

    // Devuelve un vector con las frecuencias de los valores de las cartas
    vector<int> getFrequencies() const {
        array<int, 13> freq = {};
        for (const auto &card : cards) {
            freq[card.getNumericValue()]++;
        }
        return vector<int>(freq.begin(), freq.end());
    }

    // Verifica el tipo de la mano
    HandRank evaluateHand() const {
        auto freq = getFrequencies();
        sort(freq.rbegin(), freq.rend()); // Orden descendente

        if (freq[0] == 5) return FIVE_OF_A_KIND;
        if (freq[0] == 4) return FOUR_OF_A_KIND;
        if (freq[0] == 3 && freq[1] == 2) return FULL_HOUSE;
        if (freq[0] == 3) return THREE_OF_A_KIND;
        if (freq[0] == 2 && freq[1] == 2) return TWO_PAIRS;
        if (freq[0] == 2) return ONE_PAIR;
        return HIGH_CARD;
    }

    // Compara dos manos basándose en sus cartas
    bool operator<(const Hand &other) const {
        for (size_t i = 0; i < 5; ++i) {
            int thisValue = cards[i].getNumericValue();
            int otherValue = other.cards[i].getNumericValue();
            if (thisValue != otherValue) return thisValue > otherValue;
        }
        return false;
    }
};

// Representación de una entrada de mano
struct HandEntry {
    Hand hand;
    int weight;
    HandRank rank;

    // Define un orden de comparación basado en el ranking y cartas
    bool operator<(const HandEntry &other) const {
        if (rank != other.rank) return rank < other.rank;
        return hand < other.hand;
    }
};

// Carga las manos desde un archivo
vector<HandEntry> loadHands(const string &filename) {
    ifstream file(filename);
    string line;
    vector<HandEntry> hands;

    while (getline(file, line)) {
        Hand hand;
        for (int i = 0; i < 5; ++i) {
            hand.cards[i] = {line[i]};
        }
        int weight = stoi(line.substr(6));
        hands.push_back({hand, weight, hand.evaluateHand()});
    }

    return hands;
}

// Ordena las manos y calcula el puntaje final
int processHands(vector<HandEntry> &hands) {
    sort(hands.rbegin(), hands.rend()); // Orden descendente
    int totalScore = 0;

    for (size_t i = 0; i < hands.size(); ++i) {
        const auto &entry = hands[i];
        cout << "Hand: ";
        for (const auto &card : entry.hand.cards) {
            cout << card.value;
        }
        cout << " is rank " << i + 1 << endl;
        totalScore += entry.weight * (i + 1);
    }

    return totalScore;
}

int main() {
    const string filename = "input.txt";
    vector<HandEntry> hands = loadHands(filename);

    int finalScore = processHands(hands);
    cout << finalScore << endl;

    return 0;
}
