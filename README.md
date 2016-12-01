# Stegasaurus #

### Setting Up and Running in a Local Environment
To run the Stegasaurus web app, please refer to our detailed wiki page for information on how to set up and build Stegasaurus locally.

[Setup, Build and Run Wiki](https://github.com/dfish13/stegasaurus/wiki/Setting-Up-and-Running-in-a-Local-Environment#windows)


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

### How to Run Test Suite

The module tests.py is executable and is run through the module manage.py.
To run tests.py ensure you are in the directory with the manage.py module.
```sh
$ python3 manage.py test
```

and hit enter.

You will be presented with an OK message if all tests executed correctly.

