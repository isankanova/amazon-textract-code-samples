import boto3
from trp import Document
import numpy as np
import csv
import os


def read_all_files_in_folder(folder_path):
    all_file_names = []
    files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg'):
            pdf_path = os.path.join(folder_path, filename)
            all_file_names.append(pdf_path)
            files.append(filename)
    
    all_file_names = np.array(all_file_names)
    files = np.array(files)
    return all_file_names, files


# Document
folderPath = "/Users/novait/Documents/Bill Simple Project/Caterplus_Invoic_Sample_JPG/"
documentName = "000aad25-9d60-43a4-916f-b094009ac873.jpg"

allFiles, fileNames = read_all_files_in_folder(folderPath)
print()
print(fileNames)


for file, fPath in zip(fileNames, allFiles): 
# Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    with open(fPath, "rb") as document:
        response = textract.analyze_document(
            Document={
                'Bytes': document.read(),
            },
            FeatureTypes=["TABLES"])

    #print(response)

    doc = Document(response)
    line_items = []
    for page in doc.pages:
        # Print tables
        for table in page.tables:
            for r, row in enumerate(table.rows):
                row_items = []
                for c, cell in enumerate(row.cells):
                    row_items.append(cell.text)
                    #print("Table[{}][{}] = {}".format(r, c, cell.text))
                    #print()
                #row_items = np.array(row_items)
                line_items.append(row_items)

    # Find the length of the longest list
    #max_length = max(len(item) for item in line_items)
    #print(max_length)

    # Pad shorter lists with None (or another placeholder)
    #line_items  = [item + [None] * (max_length - len(item)) for item in line_items]

    #line_items = np.array(line_items)

    #print(line_items)

    csv_file_path = '/Users/novait/Documents/GitHub/Output/Caterplus_Invoic_Sample/' + str(os.path.splitext(file)[0]+ ".csv")
    with open(csv_file_path, mode='w', newline='') as file:
       writer = csv.writer(file)
       writer.writerows(line_items)


