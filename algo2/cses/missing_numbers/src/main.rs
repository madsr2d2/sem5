use std::io;

fn find_missing_number(n: usize, array: Vec<usize>) -> usize {
    // Calculate the sum of all numbers from 1 to n
    let total_sum = n * (n + 1) / 2;

    // Calculate the sum of the numbers in the input array
    let array_sum: usize = array.iter().sum();

    // The missing number is the difference between the two sums
    total_sum - array_sum
}

fn main() {
    // Step 1: Read input
    let mut input = String::new();

    // Read the first line (which contains the integer n)
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
    let n: usize = input.trim().parse().expect("Please provide a valid number");

    // Step 2: Read the second line (which contains n-1 numbers)
    input.clear(); // Clear the buffer to read the second line
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    // Parse the second line into a vector of integers
    let array: Vec<usize> = input
        .trim()
        .split_whitespace() // Split the input into whitespace-separated parts
        .map(|num| num.parse().expect("Please provide valid numbers")) // Parse each part into usize
        .collect();

    // Step 3: Find the missing number
    let missing_number = find_missing_number(n, array);

    // Step 4: Print the result
    println!("{}", missing_number);
}
