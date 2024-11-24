#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <tuple>
#include <vector>
#include <map>

using namespace std;

const int NUM_CARDS = 5;
const int NUM_RANKS = 13;

// Mapeo para los valores de las cartas
const map<char, int> CARD_VALUES = {
    {'2', 0}, {'3', 1}, {'4', 2}, {'5', 3}, {'6', 4}, {'7', 5},
    {'8', 6}, {'9', 7}, {'T', 8}, {'J', 9}, {'Q', 10}, {'K', 11}, {'A', 12}
};

// Obtiene el valor numérico de una carta
int get_card_value(char card) {
    return CARD_VALUES.at(card);
}

// Cuenta la cantidad de cada carta en la mano
array<int, NUM_RANKS> count_card_frequencies(const array<char, NUM_CARDS>& hand) {
    array<int, NUM_RANKS> frequencies = {};
    for (char card : hand) {
        frequencies[get_card_value(card)]++;
    }
    return frequencies;
}

// Clasifica la mano según su categoría
enum HandCategory {
    FIVE_OF_A_KIND,
    FOUR_OF_A_KIND,
    FULL_HOUSE,
    THREE_OF_A_KIND,
    TWO_PAIR,
    ONE_PAIR,
    HIGH_CARD
};

// Determina la categoría de la mano
HandCategory classify_hand(const array<char, NUM_CARDS>& hand) {
    array<int, NUM_RANKS> frequencies = count_card_frequencies(hand);
    vector<int> counts;
    for (int count : frequencies) {
        if (count > 0) counts.push_back(count);
    }

    sort(counts.rbegin(), counts.rend()); // Orden descendente

    if (counts[0] == 5) return FIVE_OF_A_KIND;
    if (counts[0] == 4) return FOUR_OF_A_KIND;
    if (counts[0] == 3 && counts[1] == 2) return FULL_HOUSE;
    if (counts[0] == 3) return THREE_OF_A_KIND;
    if (counts[0] == 2 && counts[1] == 2) return TWO_PAIR;
    if (counts[0] == 2) return ONE_PAIR;
    return HIGH_CARD;
}

// Carga las manos desde un archivo
vector<tuple<array<char, NUM_CARDS>, int>> load_hands(const string& filename) {
    ifstream file(filename);
    vector<tuple<array<char, NUM_CARDS>, int>> hands;
    string line;

    while (getline(file, line)) {
        array<char, NUM_CARDS> hand;
        int bet = 0;

        // Leer cartas
        for (int i = 0; i < NUM_CARDS; i++) {
            hand[i] = line[i];
        }

        // Leer apuesta
        if (line.size() > NUM_CARDS) {
            bet = stoi(line.substr(NUM_CARDS));
        }

        hands.emplace_back(hand, bet);
    }

    return hands;
}

// Compara dos manos para ordenarlas
bool compare_hands(const tuple<array<char, NUM_CARDS>, int, HandCategory>& hand1,
                   const tuple<array<char, NUM_CARDS>, int, HandCategory>& hand2) {
    if (get<2>(hand1) != get<2>(hand2)) {
        return get<2>(hand1) < get<2>(hand2);
    }

    const auto& cards1 = get<0>(hand1);
    const auto& cards2 = get<0>(hand2);

    for (int i = 0; i < NUM_CARDS; i++) {
        int value1 = get_card_value(cards1[i]);
        int value2 = get_card_value(cards2[i]);
        if (value1 != value2) {
            return value1 > value2;
        }
    }

    return false;
}

// Imprime las manos ordenadas y calcula la puntuación final
void process_and_output_hands(vector<tuple<array<char, NUM_CARDS>, int>>& hands) {
    vector<tuple<array<char, NUM_CARDS>, int, HandCategory>> classified_hands;

    // Clasificar cada mano
    for (const auto& [hand, bet] : hands) {
        classified_hands.emplace_back(hand, bet, classify_hand(hand));
    }

    // Ordenar las manos
    sort(classified_hands.begin(), classified_hands.end(), compare_hands);

    int total_score = 0;

    // Imprimir resultados
    for (size_t i = 0; i < classified_hands.size(); i++) {
        const auto& [hand, bet, category] = classified_hands[i];
        cout << "Hand: ";
        for (char card : hand) {
            cout << card;
        }
        cout << " is rank " << i + 1 << endl;

        total_score += bet * (i + 1);
    }

    cout << "Total score: " << total_score << endl;
}

int main() {
    string filename = "practice.txt";
    vector<tuple<array<char, NUM_CARDS>, int>> hands = load_hands(filename);

    process_and_output_hands(hands);

    return 0;
}
