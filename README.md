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

User Instructions to run the programme with minimal error:
1) Form Designs should:
    - Have corner markers at each corner (mandatory)
        a) Markers should be filled
    - Only have OMR (A, B, C, D, E, ...) and/or Numerical Questions (0-9, __digits)
    - Have bubbles with the shape of a
        a) rectangle
        b) square
        c) circle
        d) oval
    - Have bubbles of the same shape and size
    - Have bubbles with considearble thick outline (that will not be broken when scanned)
    - Have bubbles that are NOT in contact with the Numbers and Alphabets within
    - Have regular spacings between bubbles
        -E.g. Reponses (i.e. A, B, C, D, E)
        -E.g. Question in a group of OMR (i.e. 1-5)
        -E.g. Digits within a numerical question


2) Instructions for candidates (either in the OMR sheet or other sheets of paper) should include:
    - The correct way of shading the OMR bubbles
        a) OMR
        b) Numerical
    - DO NOT draw/write/scribble anything on any of the undesignated areas of the OMR sheet

3) Scanned Images should
    - Be clear
    - Only have minimal rotation
    - Only have minimal offset
    - Only have minimal scaling
    - NOT be crumpled with crease lines
    - NOT be distorted

4) Selection of Region of Interest (ROI):
    - ROI should only contain bubbles
    - The spacing of bubbles in the ROI should be regular (both horizontal and vertical)
        - Otherwise, Optimisation Function of the program will regard it as 'Optimisation Error!'
        - If spacing is not regular, select the bubbles as few separate ROIs that satisfy the condition
    - The parameters required for ROI are as follow:
        - Type of reponses
        - Orientation
        - No. of questions
        - No. of Responses


