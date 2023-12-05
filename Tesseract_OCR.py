import os
import platform 
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import shutil
import argparse
import sys
from PIL import Image

def find_file(path): 
    img_file = []
    for dp, dn, filenames in os.walk(path):
        for f in filenames:
        
            if f[-4:] in ('.png', '.jpeg', '.jpg', 'tiff', 'gif', 'bmp', 'pmm') or f[-4:] in ('.PNG', '.JPEG', '.JPG', '.TIFF', '.GIF', '.BMP', '.PMM'):
                img_file.append(os.path.join(dp, f))
    return img_file           

def find_file_pdf(path):
    pdf_file = []
    for dp, dn, filenames in os.walk(path):
        for f in filenames:
            if  f[-4:]=='.pdf' or f[-4:] == '.PDF':
                pdf_file.append(os.path.join(dp, f))
    return pdf_file      
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def file_processing(OCR_path,outputfolder): 
    output = pd.DataFrame(columns=['Filename', 'Extracted_Text']) 
    img_file = find_file(OCR_path)
    pdf_file = find_file_pdf(OCR_path) 
    outputtemppath = OCR_path + '\\temp'


    if img_file: 
# Simple image to string
        create_dir(outputtemppath)
        create_dir(outputfolder)
        for i in img_file: 
            try: 
                text_output = pytesseract.image_to_string(i, lang='eng')
                text_output_file = outputfolder + '\\'+ i.split('\\')[-1] + '_output.txt'
                with open(text_output_file, 'w+') as output_file:
                    output_file.write(text_output)
                output.loc[len(output.index)] = [i, text_output]
                print(f'[+] {i} is procesed.') 
            except Exception as e:
                print(f'[-] Error: {e}')
                pass

    

    if pdf_file:
        create_dir(outputtemppath)
        create_dir(outputfolder)
        for i in pdf_file:
                image_file_list = []
                filetextoutput = ''
                folderpathtemp  = outputtemppath + '\\' + i.split('\\')[-1] 
                create_dir (folderpathtemp) 
                pdf_pages = convert_from_path(i, 600, poppler_path=path_to_poppler_exe)
                for page_enumeration, page in enumerate(pdf_pages, start=1): 
                    filename = f"{folderpathtemp}\page_{page_enumeration:03}.jpg"
                    page.save(filename,"JPEG") 
                    image_file_list.append(filename)
                text_output = outputfolder +'\\' +  i.split('\\')[-1] + '_output.txt'
                with open(text_output, 'a+') as output_file:
                    for image_file in image_file_list:
                      try:
                          text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                          text = text.replace("-\n", "")
                          output_file.write(text)
                          filetextoutput = filetextoutput + text
                      except Exception as e:
                          print(f'[-] Error: {e}')
                          pass
                 
                output.loc[len(output.index)] = [i, filetextoutput]
                print(f'[+] {i} is processed.') 
            
    output.to_csv(outputfolder + '\\' + 'output_files_all.csv', header=True, index=False)
    print(f'[+] Removing the temp. folder now.....')
    shutil.rmtree(outputtemppath)
    print(f'[+] {outputfolder}\\output_files_all.csv is saved. Process completed.')

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="""Welcome to TessOCR. This is a script that leverage Tesseract OCR to extract words from Images/PDF recursively inside a folder. The current supported formats are: (1) PDF (2) TIFF (3) JPEG (4) JPG (5) PNG (6) GIF (7) BMP (8) PMM. The script is only working in Windows. Please use this with caution and install the relevant binaries before starting.
    Tesseract Download Link: https://digi.bib.uni-mannheim.de/tesseract/. Poppler download link: https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.11.0-0 and put these files into C:\Program Files\Tesseract-OCR\tesseract.exe and C:\Program Files\poppler\Library\\bin respectively. """)
    parser.add_argument('-d', nargs='?',metavar="File Directory", help='Directory of your files')
    parser.add_argument('-o', nargs='?',metavar="Output Folder", help='This is optional. Specify the directory where the output should write to. If nothing is specify, an output folder will be created inside the OCR folder.')
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    
    if args.d is not None:
        if args.d[-1] == '\\':
            args.d = args.d[:-2] 
            
    if args.d is None:
        print('[+] Setting the OCR folder path to the current directory...')
        args.d = os.path.abspath(os.getcwd())
        
    OCR_path = args.d
    print(f'[+] OCR path set to {OCR_path}')
    print(f'[+] Checking if poppler and Tesseract are installed.')
    if os.path.isfile(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        print(f'[+] Tesseract is installed.')
    else:
        print(f'[+] Plese install Tesseract.  Tesseract Download Link: https://digi.bib.uni-mannheim.de/tesseract/ and install this into C:\Program Files\Tesseract-OCR ')
    if os.path.isdir(r'C:\Program Files\poppler\Library\bin'):
        print(f'[+] Poppler is installed.')
    else:
        print(f'[+] Plese install Poppler.Poppler download link: https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.11.0-0 and put these files into C:\Program Files\poppler ')
        sys.exit()
    if platform.system()!='Windows':
        print(f'[+] This script only runs in Windows.') 
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        path_to_poppler_exe =r'C:\Program Files\poppler\Library\bin'
    if args.o is not None:
        if args.o[-1] == '\\':
            args.o = args.o[:-2]
            outputfolder = args.o + '\\output'
    if args.o is None:
        outputfolder = OCR_path + '\\output'
        
    print(f'[+] Setting the output folder to {outputfolder}')
    
    file_processing(OCR_path, outputfolder)

        

    
    

