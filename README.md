# Stegasaurus #

About

TODO: what image formats we support, what the limitations are, how to set up the project, how to run the steg code etc.

Currently, the python module stega.py has functions that support unicode text injection and extraction to and from PNG image files.
Additionally, this module supports injection and extraction of certain types of PNG images to and from larger PNG files. PNG image types that are supported are Grayscale, RGB (3 channel), and RGBA (4 channel).
Obviously there are limitations to how much data can be stored inside PNG image files. The primary steganographic method used is least significant bit (lsb) substitution. This minimizes the visual change to an image when data is hidden inside it. If you disregard the size of the data header and the possiblity that you are dealing with two different types of PNG images with different numbers of channels then you can safely assume that you will be able to store <image 1> in <image 2> as long as <image 2> is atleast 8 times the size of <image 1>. The modifications to the image should be subtle enough to not be visible to the naked eye.
Another limitation to the lsb substitution method is that if an image has low entropy its modified version might be significantly larger. This has to do with the compression methods used by PNG images.

The module stega.py is executable and allows you to test its basic functions.
To run stega.py type

$ python3 stega.py

and hit enter.
You will be presented with a few options and prompted to choose one of the test functions.


