# TessOCR
An automated python script to OCR images and PDF for DF/eDiscovery professional. 
This is a script that leverage Tesseract OCR to extract words from Images/PDF recursively inside a folder. 
The current supported formats are: 
(1) PDF 
(2) TIFF 
(3) JPEG 
(4) JPG 
(5) PNG 
(6) GIF 
(7) BMP 
(8) PMM. 
The script is only working in Windows. Please use this with caution. If a linux support is required, please contact me for additional feature request. 

# Prerequisite
(1) Install the relevant binaries: 
- Download Windows Tesseract: https://digi.bib.uni-mannheim.de/tesseract/ and install this under C:\Program Files\tesseract-ocr (I used tesseract-ocr-w64-setup-5.3.3.20231005.exe for testing.) 
- Download Windows Poppler: https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.11.0-0. Extract the zip files into C:\Program Files\poppler

(2) Install the relevant python library: 
```pip install -r requirements.txt```

# Usage 
```
usage: Tesseract_OCR.py [-h] [-d [File Directory]] [-o [Output Folder]]

Welcome to TessOCR. This is a script that leverage Tesseract OCR to extract words from Images/PDF recursively inside a
folder. The current supported formats are: (1) PDF (2) TIFF (3) JPEG (4) JPG (5) PNG (6) GIF (7) BMP (8) PMM. The
script is only working in Windows. Please use this with caution and install the relevant binaries before starting.
Tesseract Download Link: https://digi.bib.uni-mannheim.de/tesseract/. Poppler download link:
https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.11.0-0 and put these files into C:\Program
Files\Tesseract-OCR\ and C:\Program Files\poppler\Library\bin respectively.

options:
  -h, --help           show this help message and exit
  -d [File Directory]  Directory of your files
  -o [Output Folder]   This is optional. Specify the directory where the output should write to. If nothing is
                       specify, an output folder will be created inside the OCR folder.
 ```

Example to OCR a PDF and a PNG image under Z:\OCR_Folder\Test. (The sample documents are uploaded to the github as well under the folder Test.) All the OCR text output will be saved in Z:\OCR_Folder\Test\Output
```
python Tesseract_OCR.py -d Z:\OCR_Folder\Test

 ```
# References 
https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
