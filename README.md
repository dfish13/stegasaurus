# Stegasaurus #

**TODO** : About section, how to set up the project, plans for the future, etc.

### About



### Supports

Currently, the python module stega.py has functions that support unicode
text injection and extraction to and from PNG image files.
Additionally, this module supports injection and extraction of certain
types of PNG images to and from larger PNG files.
PNG image types that are supported are:

* Grayscale
* RGB (3 channel)
* RGBA (4 channel)

### Limitations

Obviously there are limitations to how much data can be stored inside PNG image files.
The primary steganographic method used is least significant bit (lsb) substitution.
This minimizes the visual change to an image when data is hidden inside it.
The modifications to the image should be subtle enough to not be visible to the naked eye
but this comes at the cost of only being able to squeeze images into images that are
at least 8 times as large.
Another limitation to the lsb substitution method is that if an image has low entropy
its modified version might be significantly larger.
This has to do with the compression methods used by PNG images.

### How to Run

The module stega.py is executable and allows you to test its basic functions.
To run stega.py type
```sh
$ python3 stega.py
```
and hit enter.
You will be presented with a few options and prompted to choose one of the test functions.

***

