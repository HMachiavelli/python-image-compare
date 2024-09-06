# Python script for image comparison

The `main.py` script iterates through a given folder of images, comparing each one with a given main image. The output is a percentage if similarity and a little feedback.
This script is a variation of https://github.com/rohitanil/Image-Compare, just updated some things so it works properly.

# Running the script

You need 3 things in order to run the script:
1. A folder called `images` containing the files you want to compare with the main image, with any names and/or formats;
2. A file on the same dir as the `main.py` script to be used as the main image;
3. Check `requirements.txt` for a list of libs you need to install beforehand.

Change the name of the main image file on line 14 to match the filename you have created.

When you are set, just run `python main.py`