import cv2

def toGameBoyImage(image):
    firstStep = downScale(image)
    secondStep = toGrayScale(firstStep)
    thirdStep = threShold(secondStep)
    return thirdStep

def toGrayScale(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    result = grayscale
    return result

def toRGB(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return result

def downScale(image):
    height, width = image.shape[:2]
    w, h = (125, 125)
    temp = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
    result = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return result

def threShold(image):
    _, result = cv2.threshold(image, 55, 255, cv2.THRESH_BINARY)
    return result