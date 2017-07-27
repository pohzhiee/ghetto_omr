Language: Python 2.7 (C++/python3 port if possible)
Dependencies: Gtk 3.0, OpenCV 3.2 and their respective dependencies

Current contributors are only hobbyists, so anybody is welcome to contribute :)

Aim:
To develop a working optical mark reading software capable of:
1) reading the answer of multiple choice questions (i.e. A B C D E)
2) reading the answer of shaded numerical answers (i.e. 345)
3) Provide necessary GUI such that it is user friendly

*OMS refers to Optical Mark Sheet
Methodology:
1) Select a blank OMS sheet
2) Select multiple regions of interest in a blank OMS as template
3) Specify each region (i.e. number of questions & answers, position marker, etc.)
4) Outlining regions with questions
5) Detect contours
6) find valid contours and make it into a matrix
7) Get absolute coordinates of each element in matrix (to match that of answer later)
8) Select output folder
9) Select input folder
10) Process all image files in input folder by perspective transforming each one based on surface markers
11) Save output to output folder




