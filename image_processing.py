print("Welcome to the python image processor !\n")
filename = input("Enter the name of the file you want to process:\n")
operation = int(input("Choose the operation you want to perform by entering 1 or 2:\n"
                      "1) Average grayscale coloring\n"
                      "2) Convolution operation\n"))


# Function that prints 3D pixel matrix
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


# Find the average grayscale value of areas in the image and color each area with its average grayscale value
if operation == 1:
    ffilename = open(filename, "r")

    file_format = ffilename.readline().strip()
    num_of_columns, num_of_rows = ffilename.readline().split()
    num_of_columns, num_of_rows = int(num_of_columns), int(num_of_rows)
    max_color_val = int(ffilename.readline().strip())
    pixel_value_lst = []
    i = ffilename.readline()
    while i:
        a = i.strip().split()
        pixel_value_lst.extend(a)  # Store all pixel values in a list
        i = ffilename.readline()
    ffilename.close()

    img_matrix = [[[0] for i in range(num_of_columns)] for j in range(num_of_rows)]
    p = 0
    for r in range(num_of_rows):
        for c in range(num_of_columns):
            for cha in range(1):
                img_matrix[r][c][cha] = int(pixel_value_lst[p])  # Place every pixel value in a 3D matrix
                p += 1


    # Function that finds total value of the pixels in a given region surrounded by black pixels
    def total_calc(img, row, column):
        total = 0
        if row < 0 or column < 0 or row >= len(img) or column >= len(img[0]):
            return 0
        if img[row][column][0] == 0 or img[row][column][0] == -1:
            return 0

        total += img[row][column][0]
        img[row][column][0] = -1

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # Move up, down, left and right in the pixel matrix
        for d in directions:
            a = total_calc(img, row + d[0], column + d[1])
            total += a
        return total


    # Function that finds count of the pixels in a given region surrounded by black pixels
    def count_calc(img, row, column):
        count = 0
        if row < 0 or column < 0 or row >= len(img) or column >= len(img[0]):
            return 0
        if img[row][column][0] == 0 or img[row][column][0] == -2:
            return 0

        count += 1
        img[row][column][0] = -2

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for d in directions:
            a = count_calc(img, row + d[0], column + d[1])
            count += a
        return count


    # Function that colors a region with a given grayscale color value
    def rec_img_coloring(img, row, column, color_val):
        if row < 0 or column < 0 or row >= len(img) or column >= len(img[0]):
            return
        if img[row][column][0] != -2:
            return

        img[row][column][0] = color_val

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for d in directions:
            rec_img_coloring(img, row + d[0], column + d[1], color_val)


    # Function that finds regions surrounded by black pixels
    def region_finder(img):
        avg = None
        column = len(img[0])
        row = len(img)
        for r in range(row):
            for c in range(column):
                for cha in range(1):
                    if img[r][c][cha] != 0 and img[r][c][cha] != avg:  # 0 grayscale value means a black pixel, border
                        # Find the total of the grayscale values of the pixels in this region of the PGM image
                        total = total_calc(img, r, c)
                        # Find the count of the pixels in this region
                        count = count_calc(img, r, c)
                        avg = total // count
                        rec_img_coloring(img, r, c, avg)  # Color the region with the average grayscale value
        return img


    img_matrix = region_finder(img_matrix)
    img_printer(img_matrix)

    # Create the modified PGM file
    output_file = open("modified_" + filename, "w")
    output_file.write("P2\n")
    output_file.write(str(num_of_columns) + " " + str(num_of_rows) + "\n")
    output_file.write("255\n")

    for row in range(len(img_matrix)):
        for column in range(len(img_matrix[0])):
            for channel in img_matrix[row][column]:
                output_file.write(str(channel) + " \t")
        output_file.write("\n")

    output_file.close()

# Apply convolution operation to the image using a kernel
elif operation == 2:
    filter_filename = input("Enter the name of the filter file:\n")
    stride = int(input("Stride size:\n"))
    ffilename = open(filename, "r")
    file_format = ffilename.readline().strip()
    num_of_columns, num_of_rows = ffilename.readline().split()
    num_of_columns, num_of_rows = int(num_of_columns), int(num_of_rows)
    max_color_val = ffilename.readline().strip()
    rest = ffilename.readlines()
    ffilename.close()

    # Store value of every pixel in a list
    try:
        pixel_val_lst = []
        for i in rest:
            a = i.strip().split("\t")
            pixel_val_lst.extend(a)
        pass
    except:
        pixel_val_lst = []
        for i in rest:
            pixel_val_lst.append(i.strip())
        pass

    a = 0
    img_matrix = [[[0, 0, 0] for i in range(num_of_columns)] for j in range(num_of_rows)]
    draft_img_matrix = [[[0, 0, 0] for i in range(num_of_columns)] for j in range(num_of_rows)]
    for r in range(num_of_rows):
        for c in range(num_of_columns):
            for cha in range(len(img_matrix[0][0])):
                tmp_lst = pixel_val_lst[a].split()  # Store rgb values of a single pixel in a temporary list
                img_matrix[r][c][cha] = int(tmp_lst[cha])
                draft_img_matrix[r][c][cha] = int(tmp_lst[cha])
            a += 1


    # Function that creates a new matrix
    def matrix_creator():
        global pixel_val_lst
        a = 0
        new_matrix = [[[0, 0, 0] for i in range(num_of_columns)] for j in range(num_of_rows)]
        for r in range(num_of_rows):
            for c in range(num_of_columns):
                for cha in range(len(new_matrix[0][0])):
                    tmp_lst = pixel_val_lst[a].split()
                    new_matrix[r][c][cha] = int(tmp_lst[cha])
                a += 1
        return new_matrix


    ffilter = open(filter_filename, "r")
    rest2 = ffilter.readlines()
    ffilter.close()
    filter_vals = [j.split() for j in rest2]

    filter_matrix = [[[0] for i in range(len(filter_vals[0]))] for j in range(len(filter_vals))]
    for r in range(len(filter_vals)):
        for c in range(len(filter_vals[0])):
            filter_matrix[r][c][0] = float(filter_vals[r][c])

    filter_len = len(filter_matrix)
    lost_len = (filter_len - 1) // 2  # Output dimensions may be smaller than the original image due to filter size


    # Function that applies convolution operation to a given image matrix
    def rec_convolution(img, row, column, channel, starting_r, starting_c, length, kernel_r, kernel_c, draft):
        global filter_matrix
        total = 0
        if row < starting_r - length or column < starting_c - length or row > starting_r + length or column > starting_c + length:
            return 0
        if draft[row][column][channel] == -2:  # Indicates that this location has already been visited for convolution
            return 0
        total += img[row][column][channel] * filter_matrix[kernel_r][kernel_c][0]
        draft[row][column][channel] = -2

        directions = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        for d in directions:
            a = rec_convolution(img, row + d[0], column + d[1], channel, starting_r, starting_c, length,
                                kernel_r + d[0], kernel_c + d[1], draft)
            total += a
        return total


    new_new_img_pixels = []
    kernel_center = (filter_len - 1) // 2
    for r in range(lost_len, num_of_rows - lost_len, stride):
        new_img_pixels = []
        for c in range(lost_len, num_of_columns - lost_len, stride):
            new_val_lst = []
            # Do the convolution operation for all rgb channels separately
            for cha in range(len(img_matrix[0][0])):  # Channel is reg, green or blue
                a = rec_convolution(img_matrix, r, c, cha, r, c, lost_len, kernel_center, kernel_center,
                                    draft_img_matrix)
                if a < 0:
                    a = 0
                elif a > 255:
                    a = 255
                new_val_lst.append(int(a))
            new_img_pixels.append(new_val_lst)
            draft_img_matrix = matrix_creator()  # Restore the modified matrix back into its original form
        new_new_img_pixels.append(new_img_pixels)  # Final image matrix after the convolution operation

    img_printer(new_new_img_pixels)

    # Create the modified PPM file
    output_file = open("modified_" + filename, "w")
    output_file.write("P3\n")
    row_len = len(new_new_img_pixels)
    column_len = len(new_new_img_pixels[0])
    output_file.write(str(row_len) + " " + str(column_len) + "\n")
    output_file.write("255\n")

    for row in range(len(new_new_img_pixels)):
        for column in range(len(new_new_img_pixels[0])):
            for channel in new_new_img_pixels[row][column]:
                output_file.write(str(channel) + " ")
            output_file.write("\t")
        output_file.write("\n")

    output_file.close()
