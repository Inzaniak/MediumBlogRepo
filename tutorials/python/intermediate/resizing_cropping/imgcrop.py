from PIL import Image

im = Image.open("./images/pexels-inchs-12092806.jpg")

desired_size = (1280,720)
im_size = im.size
new_size = im.size

# Check if the image is vertical or horizontal
if im_size[0] >= im_size[1]:
    # Check if the image is already the desired size
    if im_size[1] > desired_size[1]:
        x_axis = int(desired_size[1] / im_size[1] * im_size[0])
        y_axis = desired_size[1]
elif im_size[1] > im_size[0]:
    # Check if the image is already the desired size
    if im_size[0] > desired_size[0]:
        x_axis = desired_size[0]
        y_axis = int( desired_size[0] / im_size[0] * im_size[1])
new_size = (x_axis, y_axis)
im_resized = im.resize(new_size)

# Find the center of the image
left = int(im_resized.size[0]/2 - desired_size[0]/2)
upper = int(im_resized.size[1]/2 - desired_size[1]/2)
right = left + desired_size[0]
lower = upper + desired_size[1]

# Crop and save the image
im_cropped = im_resized.crop((left, upper,right,lower))
im_cropped.save("./images/thumbnail.jpeg")