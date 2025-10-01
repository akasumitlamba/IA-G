#include<bits/stdc++.h> // Include necessary libraries
#include<numeric>
#include<math.h>
using namespace std;
const int INF = 1e9; // Initialize a constant for infinity
const int N = 1e7+3;
int main()
{
    int n, m; 
    cin >> n >> m; // Input the values of n and m

    int arr[m], k = 0; // Initialize an array to store the Fibonacci series and a variable k
    for(int i=0; i<n-1; i++)
        arr[i] = 0; // Initialize the first n-1 elements of the array to 0
    arr[n-1] = 1; // Set the nth element of the array to 1 (Fibonacci series starting point)
    int curr_sum = 1; // Initialize the current sum

    for(int i=n; i<=m; i++){
        arr[i] = curr_sum; // Set the next element in the Fibonacci series
        curr_sum += arr[i]; // Update the current sum
        curr_sum -= arr[k]; // Subtract the element that is n steps back
        k++; // Increment k to track the current position
    }
    for (int i = 0; i < m; i++)
    {
        cout << arr[i] << " "; // Output the Fibonacci series
    }
    return 0;
}
 // Approach of the program :
    // 1. Initialize the array with zeros for the first n-1 elements.
    // 2. Set the nth element of the array to 1, which is the starting point of the Fibonacci series.
    // 3. Initialize a variable curr_sum to 1.
    // 4. Loop from n to m to generate the Fibonacci series.
    //    a. Set the next element in the Fibonacci series to curr_sum.
    //    b. Update curr_sum by adding the newly calculated element.
    //    c. Subtract the element that is n steps back to maintain the sliding window of size n.
    //    d. Increment the variable k to keep track of the current position in the array.
    // 5. Print the generated Fibonacci series.
