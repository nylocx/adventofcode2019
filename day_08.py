import numpy as np
import matplotlib.pyplot as plt

with open("day_08.input", "r") as input_data:
    data = np.fromiter(input_data.readline().strip(), int).reshape(-1, 6, 25)

min_zero_layer = np.argmin((data == 0).sum(axis=(1,2)))
print(f"Part 1: checksum for the layer with fewest zeros is: "
      f"{(data[min_zero_layer] == 1).sum() * (data[min_zero_layer] == 2).sum()}")

print("Part 2:")
plt.imshow(np.apply_along_axis(lambda x: x[x < 2][0], axis=0, arr=data))
plt.show()
