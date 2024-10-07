// The merge_sort function takes a vector of integers and returns a sorted vector of integers.
fn merge_sort(mut array: Vec<i32>) -> Vec<i32> {
    // If the array has 1 or 0 elements, it's already sorted, so return it.
    let length = array.len();
    if length <= 1 {
        return array;
    }

    // Find the middle index of the array to split it into two halves.
    let mid = length / 2;

    // Recursively sort the left half and right half.
    // `array.drain(0..mid).collect()` extracts the first half of the array into a new vector.
    // The remaining part of the array becomes the right half.
    let left_half = merge_sort(array.drain(0..mid).collect());
    let right_half = merge_sort(array);

    // Merge the two sorted halves into a single sorted vector.
    merge(left_half, right_half)
}

// The merge function takes two sorted vectors (left and right) and merges them into a single sorted vector.
fn merge(left: Vec<i32>, right: Vec<i32>) -> Vec<i32> {
    // Create a vector to hold the merged result. We allocate space equal to the combined size of left and right.
    let mut result = Vec::with_capacity(left.len() + right.len());

    // Create iterators for the left and right vectors.
    let (mut left_iter, mut right_iter) = (left.into_iter(), right.into_iter());

    // Get the first elements of each iterator (if any).
    let (mut left_item, mut right_item) = (left_iter.next(), right_iter.next());

    // While both iterators have elements to process, continue merging.
    while let (Some(l), Some(r)) = (left_item, right_item) {
        if l <= r {
            // If the left item is smaller or equal, push it to the result and advance the left iterator.
            result.push(l);
            left_item = left_iter.next();
        } else {
            // If the right item is smaller, push it to the result and advance the right iterator.
            result.push(r);
            right_item = right_iter.next();
        }
    }

    // Append any remaining elements from the left iterator (if any).
    result.extend(left_item.into_iter().chain(left_iter));

    // Append any remaining elements from the right iterator (if any).
    result.extend(right_item.into_iter().chain(right_iter));

    // Return the merged and sorted result.
    result
}

// The main function to test the merge sort implementation.
fn main() {
    // Example array to be sorted.
    let array = vec![12, 11, 13, 5, 6, 7];
    println!("Given array: {:?}", array);

    // Call merge_sort to sort the array.
    let sorted_array = merge_sort(array);
    println!("Sorted array: {:?}", sorted_array);
}
