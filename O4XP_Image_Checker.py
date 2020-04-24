import pathlib
import glob
import os
import numpy as np
import cv2
import multiprocessing
from multiprocessing import Pool
import time

# Function to check each pixel of a jpg file to identify any pixels that is completely white.
def has_white_rects(img_path):
    img = cv2.imread(img_path)
    w, h, depth = img.shape

    last_rows = []

    for i in range(w):        
        if len(last_rows) > 2:
            r1s, r1e = last_rows[i-2]
            r2s, r2e = last_rows[i-1]

            if ((r2s - r1s) == 0) and ((r2e - r1e) == 0):
                # The last two rows of pixels are white and exactly equal in 
                # length -- this is NOT common in satellite imagery
                return True

        row_start = h
        row_end = 0
        detected_white = False
        
        for j in range(h):
            r = img.item(i, j, 0)
            g = img.item(i, j, 1)
            b = img.item(i, j, 2)
            if r >= 255 and g >= 255 and b >= 255:
                detected_white = True
                if j < row_start:
                    row_start = j
                if j > row_end:
                    row_end = j

        if detected_white:
            last_rows.append((row_start, row_end))

    return False

delete_file = False

# Function to crawl each directory and subdirectory to check each file against has_white_rects function
def work(path):
    print ('PROCESSING IMAGE: ' + str(path))
    if has_white_rects(str(path)):
        # Log the file.
        f = open("checker_log.txt", "a")
        wrt = str(path)+'\n'
        f.write(wrt)
        f.close()
        if delete_file == True:
            os.remove(path)
            print('CORRUPT IMAGE LOGGED & DELETED: ' + str(path))
        if delete_file == False:
            print('CORRUPT IMAGE LOGGED: ' + str(path))


def main():
    acceptable_input_list = ['yes','no']

    cpu_count = int(os.cpu_count())

    user_input_1 = '';
    print ('------------------------------------------------------------------------------------------------------------------------------')
    print ('I have determined there are ' + str(cpu_count) + ' available logical cores.')

    while user_input_1 not in acceptable_input_list:
        user_input_1 = input("Do you wish to use all available cores for maximum performance? (yes/no)").lower()
    if user_input_1 == "yes":
        print ('')
        print ('I will run at full capacity. Other applications may be unusable while I am running.')
        print ('')
        workers = cpu_count
    else:
        workers = round(cpu_count/3)
        print ('')
        print ('I will run at 1/3rd capacity. Using only ' + str(workers) + ' logical cores out of total ' + str(cpu_count))
        print ('This will be slower however other applications can be run without perfoirmance degradation.')
        print ('------------------------------------------------------------------------------------------------------------------------------')
        print ('')

    # Ask the user if they wish to delete the bad jpg also
    user_input_2 = '';
    while user_input_2 not in acceptable_input_list:
        user_input_2 = input("Do you wish to DELETE corrupt jpg files automatically? (yes/no)").lower()
    if user_input_2 == "yes":
        print ('')
        print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print ('Any jpg files containing white space will be deleted without confirmation!')
        print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print ('')
        delete_file = True;
    else:
        print ('')
        delete_file = False;

    # Craft a list of each jpg files to be checked.
    image_files = []
    path = pathlib.Path().absolute()
    for z in path.rglob('*.jpg'):
        image_files.append(z)

    file_count = len(image_files)
    time_estimate = round(((file_count*2.5)/workers)/60)
    if time_estimate <= 0:
        time_estimate = "less than one"

    print ('------------------------------------------------------------------------------------------------------------------------------')
    print ('There are ' + str(file_count) + ' image files to check.')
    print ('This operation will take approximately ' + str(time_estimate) + ' minute(s).')
    print ('Starting in five seconds >>>>>')
    time.sleep(5)

    start = time.time()

    # Set up multiprocessing.
    with Pool(workers) as p:
        p.imap_unordered(work, image_files)
        p.close()
        p.join()
        print("All image files have been checked.")

    end = time.time()
    time_elapsed = round((end - start) / 60)
    if time_elapsed <= 0:
        time_elapsed = "less than one"

    print ('------------------------------------------------------------------------------------------------------------------------------')
    print ('It took ' + str(time_elapsed) + ' minute(s) to check ' + str(file_count) + ' image files.')
    print ('------------------------------------------------------------------------------------------------------------------------------')

if __name__ == "__main__":
    main()
