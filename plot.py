import matplotlib.pyplot as plt

# Data
sizes = list(range(16, 41))
blocking_sets = [
    0, 0, 0, 0, 0, 0, 0, 15, 135, 591, 1356, 1978, 2165, 1773, 1403, 1246, 1174, 1045, 979, 947, 756, 303, 124, 22, 5
]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(sizes, blocking_sets, marker='o', linestyle='-', color='b')

# Adding titles and labels
plt.title('Blocking Sets Found by Size')
plt.xlabel('Size')
plt.ylabel('Number of Blocking Sets Found')

# Display the plot
plt.grid(True)
plt.show()
