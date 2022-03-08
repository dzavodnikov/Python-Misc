from scipy import ndimage

d1 = [1, 1, 5, 6, 9]
h1 = ndimage.histogram(d1, 1, 10, 5)
print(h1)

# Out of (min, max) are ignired.
d2 = [-1, 1, 1, 5, 6, 9, 11]
h2 = ndimage.histogram(d2, 1, 10, 5)
print(h2)
