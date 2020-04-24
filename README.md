# Ortho4XPImageChecker

Have you ever downloaded and converted gigabytes worth of ortho images only to find out that some of them had white pixels? You then find yourself looking thru hundreds of ortho image files to figure out which ones have white pixels so that you can re-download them. This script can help you locate and delete (if you chose) those bad ortho image files. White pixel problem with Ortho4XP occurs when there is a network connection problem and Ortho4XP cannot download the entire image file. When that happens, it simply adds white pixels to those sections of the image file. Easy way to fix the file is to find it, delete it and let Ortho4XP re-download it. Assuming the network connectivity is ok for the second time, the entire image file then should download without an issue.

## Setting Up

* You need minimum Python3 to run this script. There are many documentation online how to get and install it for all the operating systems. So, get Python3 first.
* This script depends on couple libraries. There are two ways to install those libraries:
1. Using pip (python package manager) is the easiest method. Simply run the following command using command line or terminal (depending your operating system) within the root folder `Ortho4XPImageChecker`
`pip install -r requirements`
1. You can also install required libraries manually. If you wish to do so, just look at the requirements.txt file within where you can find the list of requirements.

## Running
Running this script is quite straight forward. The script is already configured to look for ortho jpg files within the folder it resides.
1. Copy and paste the `O4XP_Image_Checker.py` file into the root orthophoto folder `X:\Ortho4XP\Orthophotos`. Orthophotos folder is located within the Ortho4XP root directory and contains all orthophoto images that Ortho4XP downloads before converting them.
1. Execute the following in comand line or terminal (depending your operating system) in the Orthophotos folder where you just copied the script file to.
`python O4XP_Image_Checker.py`
1. Then simply follow the in screen instructions.

## Performance
The script uses parallel processes to check as many images as quickly as possible. Thus, it will attempt to use all logical cores in your CPU. The advantage of this is that it will ran very fast. The disadvantage however it will bog down your system enough where you wont be able to use any other application while you are running this script. Thus you have two options selecting the performance settings:

The script will show you the number of logical cores it identified, and ask you if you wish to run it at full capacity meaning using all the available CPU cores. You can say yes or no. If you say yes, it will use all available logical cores. If you say no, it will use 1/3 of the available cores, thus leaving some CPU bandwith for other applications to run. If you want to use your computer while this script is running, then do not run it at full capacity.

On average, it takes about 2.5 seconds to check one file. So if the script determined, lets say, you have 8 logical cores, then you expect to check about 8 total files in 2.5 second window.

## Logging
The script will generate a log file, `checker_log.txt` within the same folder it is executed. The log file will only contain the path of images that contain white pixels. Good image files are not logged to this file to prevent confusion.

## Deleting Image Files
The script can delete bad image files as it finds them. It will prompt you to make that choice in the very beggining. If you do not chose to delete the files, you can then locate them later using the paths recorded in the log file. Please be aware that the script will only delete the ortho image file, not the DDS file. If you wish to also delete the corrospanding DDS file, you will have to do that manually.

## Contributors
* Eray Yilmaz - https://github.com/erayymz
* Beau Albiston - https://github.com/beauzo
