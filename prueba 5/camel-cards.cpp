#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

int get_card_value(char w) {
    if (w == '2') return 0;
    if (w == '3') return 1;
    if (w == '4') return 2;
    if (w == '5') return 3;
    if (w == '6') return 4;
    if (w == '7') return 5;
    if (w == '8') return 6;
    if (w == '9') return 7;
    if (w == 'T') return 8;
    if (w == 'J') return 9;
    if (w == 'Q') return 10;
    if (w == 'K') return 11;
    if (w == 'A') return 12;
    return -1;
}

bool is_five_of_a_kind(array<char, 5> hdc) {
    return hdc[0] == hdc[1] && hdc[1] == hdc[2] && hdc[2] == hdc[3] && hdc[3] == hdc[4];
}

bool is_four_of_a_kind(array<char, 5> hdc) {
    array<int, 13> s{};
    s[get_card_value(hdc[0])]++;
    s[get_card_value(hdc[1])]++;
    s[get_card_value(hdc[2])]++;
    s[get_card_value(hdc[3])]++;
    s[get_card_value(hdc[4])]++;
    for (int i = 0; i < 13; i++) {
        if (s[i] == 4) {
            return true;
        }
    }
    return false;
}

bool is_full_house(array<char, 5> hdc) {
    array<int, 13> s{};
    s[get_card_value(hdc[0])]++;
    s[get_card_value(hdc[1])]++;
    s[get_card_value(hdc[2])]++;
    s[get_card_value(hdc[3])]++;
    vector<int> x;
    s[get_card_value(hdc[4])]++;
    for (int i = 0; i < 13; i++) {
        if (s[i] != 0) x.push_back(s[i]);
    }
    if (x.size() >= 2 && (x[0] == 3 && x[1] == 2) || (x[0] == 2 && x[1] == 3)) {
        return true;
    }
    return false;
}

bool is_three_of_a_kind(array<char, 5> hdc) {
    array<int, 13> s{};
    s[get_card_value(hdc[0])]++;
    s[get_card_value(hdc[1])]++;
    s[get_card_value(hdc[2])]++;
    s[get_card_value(hdc[3])]++;
    vector<int> x;
    s[get_card_value(hdc[4])]++;
    for (int i = 0; i < 13; i++) {
        if (s[i] != 0) x.push_back(s[i]);
    }
    if (x.size() >= 3 && (x[0] == 3 || x[1] == 3 || x[2] == 3)) {
        return true;
    }
    return false;
}

bool is_two_pairs(array<char, 5> hdc) {
    array<int, 13> s{};
    s[get_card_value(hdc[0])]++;
    s[get_card_value(hdc[1])]++;
    s[get_card_value(hdc[2])]++;
    s[get_card_value(hdc[3])]++;
    vector<int> x;
    s[get_card_value(hdc[4])]++;
    for (int i = 0; i < 13; i++) {
        if (s[i] != 0) x.push_back(s[i]);
    }
    if (x.size() >= 3 && ((x[0] == 2 && x[1] == 2) || (x[0] == 2 && x[2] == 2) || (x[1] == 2 && x[2] == 2))) {
        return true;
    }
    return false;
}

bool is_one_pair(array<char, 5> hdc) {
    array<int, 13> s{};
    s[get_card_value(hdc[0])]++;
    s[get_card_value(hdc[1])]++;
    s[get_card_value(hdc[2])]++;
    s[get_card_value(hdc[3])]++;
    s[get_card_value(hdc[4])]++;
    vector<int> x;
    for (int i = 0; i < 13; i++) {
        if (s[i] != 0) x.push_back(s[i]);
    }
    for (int i = 0; i < x.size(); i++) {
        if (x[i] == 2) {
            return true;
        }
    }
    return false;
}

int get_hand_value(array<char, 5> hdc) {
    if (is_five_of_a_kind(hdc)) return 0;
    if (is_four_of_a_kind(hdc)) return 1;
    if (is_full_house(hdc)) return 2;
    if (is_three_of_a_kind(hdc)) return 3;
    if (is_two_pairs(hdc)) return 4;
    if (is_one_pair(hdc)) return 5;
    return 6;
}

int main() {
    string l;
    ifstream f("practice.txt");
    vector<tuple<array<char, 5>, int, int> > hds;

    while (getline(f, l)) {
        array<char, 5> hdc{};
        array<char, 4> n{};
        hdc[0] = l[0];
        hdc[1] = l[1];
        hdc[2] = l[2];
        hdc[3] = l[3];
        hdc[4] = l[4];
        if (l.length() > 6) {
            n[0] = l[6];
            n[1] = '\0';
        }
        if (l.length() > 7) {
            n[1] = l[7];
            n[2] = '\0';
        }
        if (l.length() > 8) {
            n[2] = l[8];
            n[3] = '\0';
        }
        hds.push_back(make_tuple(hdc, stoi(n.data()), get_hand_value(hdc)));
    }

    for (int i = 0; i < hds.size(); i++) {
        for (int j = i + 1; j < hds.size(); j++) {
            if (get<2>(hds[i]) < get<2>(hds[j])) {
                swap(hds[i], hds[j]);
            } else if (get<2>(hds[i]) == get<2>(hds[j])) {
                for (int k = 0; k < 5; k++) {
                    if (get_card_value(get<0>(hds[i])[k]) != get_card_value(get<0>(hds[j])[k])) {
                        if (get_card_value(get<0>(hds[i])[k]) > get_card_value(get<0>(hds[j])[k])) {
                            swap(hds[i], hds[j]);
                        }
                        break;
                    }
                }
            }
        }
        cout << "Hand: ";
        for (auto c: get<0>(hds[i])) {
            cout << c;
        }
        cout << " is rank " << i + 1 << endl;
    }

    int g = 0;
    for (int i = 0; i < hds.size(); i++) {
        g += get<1>(hds[i]) * (i + 1);
    }
    cout << g << endl;
    return 0;
}
