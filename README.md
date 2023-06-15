# Image Processing

Python program that applies two different kinds of image processing operations to a given image.

## How It Works

Python program starts by taking the name of the image file to be processed from the user. The user then chooses

which of the two operations to apply to the image by typing it in the console.

### Operation 1: Average Grayscale Coloring

PGM files are used for this operation. The aim of this operation is to find the average grayscale color value of

each region and color that region with this average color value. The program searches for regions in the image

seperated by borders which are represented by black pixels. After choosing a region recursive functions are called

in order to calculate the total value of the pixel values of that region, the amount of pixels and finds an average

color value by dividing these two. After this another recursive function is called which colors each pixel in this

region with the average color.

### Operation 2: Convolution Operation Using Filters

This operation uses PPM files. The user is further asked for a filter file name and a stride value which states

how many steps the filter is going to move in each step of the convolution operation. After this a recursive

function is called which performs the convolution operation by multiplying the values of the filter and values

in the corresponding cells of the image matrix, moving the kernel by an amount of the stride and eventually

forming a new 3D matrix that contains the pixels of the convoluted image. 

### Prerequisites

An IDE or text editor to run the python code.

## Running the tests

The program starts by taking an image file to work on. The user will enter the name of the image file which should

be located inside the same folder as the source code and choose one of the two operations stated in the console.

If operation 1 is selected, no more user input will be necessary. If operation 2 is selected, user should enter

the name of the filter which will be used for the convolution operation and a stride size stating how many steps

the filter is going to move with each calculation. After each operation final pixel values of the modified image

will be both shown in the terminal and saved in a file with the same name as the original one added "modified_"

to the beginning of its name.

Example input and output (terminal) cases are given in the repository.

Three kinds of kernels, original and modified pgm and ppm files are also provided.
