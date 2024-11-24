#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <iomanip>
#include <numeric>
#include <functional>

using namespace std;

// Function to calculate the number of steps
template<typename T>
size_t countSteps(const T& container, function<void(T&)> sortAlgorithm) {
    T copy = container;
    size_t steps = 0;
    sortAlgorithm(copy, [&steps]() { steps++; });
    return steps;
}

// QuickSort implementation
template<typename T>
void quickSort(T& container, int left, int right) {
    if (left < right) {
        int pivotIndex = left + (right - left) / 2;
        int i = left;
        int j = right;
        int pivot = container[pivotIndex];

        while (i <= j) {
            while (container[i] < pivot) {
                i++;
            }
            while (container[j] > pivot) {
                j--;
            }
            if (i <= j) {
                swap(container[i], container[j]);
                i++;
                j--;
            }
        }

        quickSort(container, left, j);
        quickSort(container, i, right);
    }
}

// HeapSort implementation
template<typename T>
void heapify(T& container, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && container[left] > container[largest])
        largest = left;

    if (right < n && container[right] > container[largest])
        largest = right;

    if (largest != i) {
        swap(container[i], container[largest]);
        heapify(container, n, largest);
    }
}

template<typename T>
void heapSort(T& container) {
    int n = container.size();

    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(container, n, i);

    for (int i = n - 1; i > 0; i--) {
        swap(container[0], container[i]);
        heapify(container, i, 0);
    }
}

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, numeric_limits<int>::max());

    cout << fixed << setprecision(3);

    cout << "# QUICKSORT VERSUS HEAPSORT:" << endl;
    cout << "#Número promedio de Mpasos (millones de pasos de programa)" << endl;
    cout << "#Número de repeticiones (vectores de enteros): 30" << endl;
    cout << endl;
    cout << "# \t   VECTORES ALEATORIOS | VECTORES ORDENADOS | VECTORES ORDENADOS INVERSAMENTE" << endl;
    cout << "# \t   ----------------------------------------------------------------------" << endl;
    cout << "# Tamaño   QuickSort  HeapSort | QuickSort  HeapSort | QuickSort HeapSort" << endl;
    cout << "#==============================================================================" << endl;

    for (int exp = 15; exp <= 20; exp++) {
        size_t size = size_t(pow(2, exp));
        vector<int> vq(size), vh(size), vqInversa(size), vhInversa(size);

        generate(vq.begin(), vq.end(), [&]() { return dis(gen); });
        vh = vq;
        vqInversa = vq;
        vhInversa = vq;

        double pasosQuickSortAleatorios = 0;
        double pasosHeapSortAleatorios = 0;
        double pasosQuickSortOrdenados = 0;
        double pasosHeapSortOrdenados = 0;
        double pasosQuickSortInvOrdenados = 0;
        double pasosHeapSortInvOrdenados = 0;

        for (int repeticion = 0; repeticion < 30; repeticion++) {
            pasosQuickSortAleatorios += countSteps(vq, [&](auto& c) { quickSort(c, 0, c.size() - 1); });
            pasosHeapSortAleatorios += countSteps(vh, heapSort<decltype(vh)>);
            pasosQuickSortAleatorios += countSteps(vq, [&](auto& c) { quickSort(c, 0, c.size() - 1); });
            pasosHeapSortAleatorios += countSteps(vh, heapSort<decltype(vh)>);

            sort(vq.begin(), vq.end());
            sort(vh.begin(), vh.end());

            pasosQuickSortOrdenados += countSteps(vq, [&](auto& c) { quickSort(c, 0, c.size() - 1); });
            pasosHeapSortOrdenados += countSteps(vh, heapSort<decltype(vh)>);

            reverse(vqInversa.begin(), vqInversa.end());
            reverse(vhInversa.begin(), vhInversa.end());



            pasosQuickSortInvOrdenados += countSteps(vqInversa, [&](auto& c) { quickSort(c, 0, c.size() - 1); });
            pasosHeapSortInvOrdenados += countSteps(vhInversa, heapSort<decltype(vhInversa)>);
        }

        cout << size << "\t" << std::flush;
        cout << (pasosQuickSortAleatorios / 30) / 1000000 << "     " << (pasosHeapSortAleatorios / 30) / 1000000 << "        ";
        cout << (pasosQuickSortOrdenados / 30) / 1000000 << "     " << (pasosHeapSortOrdenados / 30) / 1000000 << "        ";
        cout << (pasosQuickSortInvOrdenados / 30) / 1000000 << "     " << (pasosHeapSortInvOrdenados / 30) / 1000000 << endl;
    }

    return 0;
}