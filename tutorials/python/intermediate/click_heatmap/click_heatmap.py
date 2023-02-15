import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import scipy.ndimage.filters as filters


def plot(data, title, image_path, save_path=None):
    colors = [(0, 0, 0, 0), (0, 1, 1), (0, 1, 0.75), (0, 1, 0), (0.75, 1, 0),
              (1, 1, 0), (1, 0.8, 0), (1, 0.7, 0), (1, 0, 0)]

    img = plt.imread(image_path)
    img = np.flipud(img)  # Flip the image vertically
    
    # Create a figure with subplots
    fig, ax = plt.subplots(figsize=(w/100, h/100))

    # Plot the heatmap on top of the background image
    ax.imshow(img, extent=[0, w, 0, h])
    cm = LinearSegmentedColormap.from_list('sample', colors)

    plt.imshow(data, cmap=cm, alpha=0.5)
    plt.colorbar()
    plt.title(title)
    if save_path:
        plt.savefig(save_path)


w = 1869
h = 933
data = np.zeros(h * w)
data = data.reshape((h, w))

# This code is used to change the brightness of the pixels in the area of the image between 780 and 820 in the x-direction and 430 and 470 in the y-direction. 
# The brightness of the pixels is set to 100.
for x in range(780, 820):
    for y in range(430, 470):
        data[y][x] = 100

# This code applies a gaussian filter to an image
data = filters.gaussian_filter(data, sigma=15)

plot(data, 'Sample plot', "webpage.png")