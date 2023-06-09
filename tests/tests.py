import pandas as pd

data = [
    [100,110,120,130,140,150],
    [0,1,0,1,1,1],
    [0,1,0,0,3,0],
    [0,1,0,1,2,1],
    [0,1,0,0,4,0],
    [0,1,0,0,3,0],
    [0,2,0,0,4,0],
    [0,1,0,0,1,1],
    [1,2,0,0,3,1],
    [0,0,1,1,0,3],
    [1,0,0,1,1,1],
    [1,4,0,0,5,1],
    [0,3,0,0,3,0],
    [0,0,2,0,0,3],
    [0,0,0,2,0,3],
    [0,1,1,2,1,5],
    [1,4,0,4,5,4],
    [1,2,0,0,3,0],
    [1,2,3,4,3,9],
    [0,1,0,1,1,2],
    [0,0,1,1,0,3],
    [0,0,1,2,0,3],
    [0,6,1,1,6,2],
    [1,3,1,0,4,1]
]
df_transaction_dataset = pd.DataFrame(data[1:], columns=data[0])


unique_combinations = set()

# Dictionary to store combination counts
combination_counts = {}


# Iterate over the dataset
for index, row in df_transaction_dataset.iterrows():
    # Iterate over the columns
    for col in df_transaction_dataset.columns:
        # Check if the column is a 3-digit number
        value = row[col]
        # Check if the value is not 0
        if value != 0:
            combination_key = (col,value)
            # Check if the combination exists in the set
            if combination_key in unique_combinations:
                # Increment the count for the combination
                combination_counts[combination_key] += 1
            else:
                # Add the new combination to the set and initialize its count to 1
                unique_combinations.add(combination_key)
                combination_counts[combination_key] = 1

# Print the combination counts
for combination, count in combination_counts.items():
    print(f"Combination: {combination}, Count: {count}")