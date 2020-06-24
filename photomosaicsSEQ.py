'''
This file contains code for the sequential version of the program.
There are 4 main steps corresponding to the first 4 functions
'''
from PIL import Image
from createRGBDataset import createDataset
import time

'''
If the width of the input image is set to 100 pixels - or blocks,
then calculate the ratio between height and width of that image
and set number of pixels of height as that ratio * real height

@return: new image that is divided into blocks
'''
def rescaleToPixels(inputImg):
    numPixelsWidth = 100      # WHERE THE SAMPLE SIZE WILL CHANGE
    pixelRatio = (numPixelsWidth / float(inputImg.size[0]))
    numPixelsHeight = int((float(inputImg.size[1]) * float(pixelRatio)))
    newImg = inputImg.resize((numPixelsWidth, numPixelsHeight), Image.ANTIALIAS)
    return newImg


'''
Get RGB values of pixels/ blocks that
the input image is divided into

@return: [[R,G,B,a],...]
'''
def getPixelsOfPic(img):
    width, height = img.size
    pixels = []
    for j in range(0, height):
        for i in range(0, width):
            pixels.append([i,j,img.getpixel((i, j))])
    return pixels


'''
Compare the RGB values of each block of the input image
to those of each Pokemon picture cropped from the database picture.

Each index will store the location of the block and the Pokemon picture most similar
@return: [[x,y of a block, Pokemon picture that will replace that block]..]
'''
def calculateBestColorFit(imgPixels, datasetPics):
    result = []

    for eachPix in imgPixels:
        x = eachPix[0]
        y = eachPix[1]
        rgb = eachPix[2]
        if rgb[3] <= 150:   #To remove the color edges
            rgb = (255,255,255,255)

        minDifference = 9999

        for i in range(len(datasetPics)):
            diff = 0
            diff += abs(rgb[0] - int(datasetPics[i][1][0]))
            diff += abs(rgb[1] - int(datasetPics[i][1][1]))
            diff += abs(rgb[2] - int(datasetPics[i][1][2]))

            if diff < minDifference:
                pic = datasetPics[i][2]
                minDifference = diff

        result.append([x,y,pic])

    return result

'''
Using the array from the above function,
this function runs through each block of the input image
and replace it with the corresponding Pokemon pictures

@return: the final output - a full photomosaics
'''
def createFinalPic(colorFitList, img, widthOfEach, heightOfEach):
    width, height = img.size
    finalImg = Image.new("RGB", (width * round(widthOfEach), height * round(heightOfEach)), color = "black")

    for i in range(0, len(colorFitList)):
        finalImg.paste(colorFitList[i][2],
                       (colorFitList[i][0] * round(widthOfEach), colorFitList[i][1] * round(heightOfEach)))

    finalImg.save("finalImg2.png")
    # finalImg.show()
    return finalImg

'''
To check if the final image from the parallel versions are correct,
this function returns the RGB values of each pixel from the output image
'''
def checkFinalImg(finalImg):
    correctResult = getPixelsOfPic(rescaleToPixels(finalImg))
    return correctResult


def main():
    print("\n ----- SEQ -----")

    processedData = createDataset()
    dataset = processedData[0]
    widthOfEach = processedData[1]
    heightOfEach = processedData[2]


    # inputImg = input("Name of picture to convert into Photomosaics:  ")
    inputImg = 'lorsan.png'
    inputImage = Image.open(inputImg).convert("RGBA")

    s1 = time.perf_counter()
    rescaledInputImg = rescaleToPixels(inputImage)
    f1 = time.perf_counter()
    print(f'RescaleToPixels finished in {round(f1-s1, 2)} second(s)')

    s2 = time.perf_counter()
    pixelsList = getPixelsOfPic(rescaledInputImg)
    f2 = time.perf_counter()
    print(f'getPixelsOfPic finished in {round(f2-s2, 2)} second(s)')

    s3 = time.perf_counter()
    colorFitList = calculateBestColorFit(pixelsList, dataset)

    f3 = time.perf_counter()
    print(f'CalculateBestColorFit finished in {round(f3-s3, 2)} second(s)')

    s4 = time.perf_counter()
    finalImg = createFinalPic(colorFitList, rescaledInputImg, widthOfEach, heightOfEach)
    f4 = time.perf_counter()
    print(f'CreateFinalPic finished in {round(f4-s4, 2)} second(s)')

    global correctResult
    correctResult =  checkFinalImg(finalImg)

main()
