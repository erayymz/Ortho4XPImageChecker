import pathlib
import glob
import os
from PIL import Image
import multiprocessing
from multiprocessing import Pool
import time

# Function to check each pixel of a jpg file to identify any pixels that is completely white.
def has_white_rects(img_path):
	img = Image.open(img_path).convert('RGB')
	w,h = img.size

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
			r,g,b = img.getpixel((i,j))
			if r >= 255 and g >= 255 and b >= 255:
				detected_white = True
				if j < row_start:
					row_start = j
				if j > row_end:
					row_end = j

		if detected_white:
			last_rows.append((row_start, row_end))

	return False

# Function to crawl each directory and subdirectory to check each file against has_white_rects function
def work(path):
	print ('Processing file: ' + str(path))
	if has_white_rects(path):
		if delete_file: print('----------FOUND BAD JPEG | DELETED ----------')
		else: print('----------FOUND BAD JPEG | LOGGED ----------')
		print (path)
		print('---------------------------------****-------')
		if delete_file: os.remove(path)
		# Also to log file paths of each bad jpegs.
		f = open("checker_log.txt", "a")
		wrt = str(path)+'\n'
		f.write(wrt)
		f.close()

def main():
	# Ask the user if they wish to delete the bad jpg also
	user_input = '';
	acceptable_input_list = ['yes','no']
	while user_input not in acceptable_input_list:
		user_input = input("Do you wish to DELETE corrupt jpg files automatically? (yes/no)").lower()

	if user_input == "yes":
		print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print ('Any jpg files containing white space will be deleted without confirmation!')
		print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		time.sleep(5)
		delete_file = 1;
	else:
		delete_file = 0;

	# Craft a list of each jpg files to be checked.
	image_files = []
	path = pathlib.Path().absolute()
	for z in path.rglob('*.jpg'):
		image_files.append(z)

	print ('All corrupt jpg files will be listed in checker_log.txt file.')
	time.sleep(5)

	# Set up multiprocessing to be equal of the logical CPU unit count for better effeciency.
	workers = int(os.cpu_count())
	with Pool(workers) as p:
		p.imap_unordered(work, image_files)
		p.close()
		p.join()
		print("ALL FILES CHECKED.")


if __name__ == "__main__":
	main()
