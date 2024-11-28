import numpy as np
from scipy.ndimage import label

def label_individual_segments(image_array):
    unique_values = np.unique(image_array)
    labeled_array = np.zeros_like(image_array)
    label_count = 1

    for value in unique_values:
        if value != 0:  # Assuming 0 is the background value and should not be labeled
            temp_array = np.where(image_array == value, 1, 0)
            labeled_temp_array, num_features = label(temp_array)

            for feature_num in range(1, num_features + 1):
                labeled_array[labeled_temp_array == feature_num] = label_count
                label_count += 1

    return labeled_array

# Example usage
image_array = np.array([
    [1, 1, 0, 2, 2],
    [1, 0, 0, 2, 2],
    [3, 3, 0, 4, 4],
    [3, 3, 0, 4, 4]
])

# Label the segments
labeled_array = label_individual_segments(image_array)
print("Labeled Array:")
print(labeled_array)

