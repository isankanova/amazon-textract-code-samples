import boto3
from trp import Document
from PIL import Image, ImageDraw
import os

# Document
documentPath = "/Users/novait/Documents/Bill Simple Project/Caterplus_Invoic_Sample_JPG/"
documentName = "000aad25-9d60-43a4-916f-b094009ac873.jpg"
outputPath = "/Users/novait/Documents/Bill Simple Project/Caterplus_Invoic_Sample_JPG/Output/"
fullPath = os.path.join(documentPath, documentName)

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(fullPath, "rb") as document:
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

# Redact document
img = Image.open(fullPath)

width, height = img.size

if(doc.pages):
    page = doc.pages[0]
    for field in page.form.fields:
        if(field.key and field.value and "gst" in field.key.text.lower()):
        #if(field.key and field.value):
            print("Redacting => Key: {}, Value: {}".format(field.key.text, field.value.text))
            
            x1 = field.value.geometry.boundingBox.left*width
            y1 = field.value.geometry.boundingBox.top*height-2
            x2 = x1 + (field.value.geometry.boundingBox.width*width)+5
            y2 = y1 + (field.value.geometry.boundingBox.height*height)+2

            draw = ImageDraw.Draw(img)
            draw.rectangle([x1, y1, x2, y2], fill="Black")

img.save(outputPath + "/redacted-{}".format(documentName))
