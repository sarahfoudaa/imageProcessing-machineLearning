import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
#size of window
cap.set(3,1280)
cap.set(4,720)
#defult is 0.5 but we want it 0.8 to increase accurency so we dont press on wrong letter
detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "del"]]

finalText = ""
#create class

def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # create rectangles/button
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        # put text in the rectangle we just created                         size                thickness
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)
    return img
class Button():
    #def= method= function (depend on language)
    #the paramets in this method are staying the same in all the buttons we will create...
    def __init__(self,pos,text,size=[85,85]):
        #OOP lma kona bn3ml this. 34an n2olo ano da hwa da
        #self. is equivilat to this.
        self.pos =pos
        self.size = size
        self.text = text
#...so the drawing steps will be put in a methos because we are drawing alot of rectangles


        #            # create rectangles/button
#            cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 255), cv2.FILLED)
#            # put text in the rectangle we just created
#            cv2.putText(img, "Q", (115, 180), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        # create rectangles/button
     #   cv2.rectangle(img, self.pos, self.size, (255, 0, 255), cv2.FILLED)
        # put text in the rectangle we just created
      #  cv2.putText(img, self.text, (self.pos[0]+25 , self.pos[1]+25), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

#call for the button
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
#myButton = Button([100,100],"Q")
#myButton1 = Button([200,100],"W")
#myButton2 = Button([300,100],"E")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    #find the hands
    img=detector.findHands(img)
    #find the landmarks in the hands
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)
    # delete
 #   cv2.rectangle(img, (750, 350), (900, 450), (175, 255, 175), cv2.FILLED)
    # put text in the rectangle we just created                         size                thickness
  #  cv2.putText(img, "del", (760, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    #img = myButton.draw(img)
    #img = myButton1.draw(img)
    #img = myButton2.draw(img)
    #to know the exact location of the button to then check if the finger is in that button or not
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            #check if the finger is in the range of that button
            #                x                      y
            if x < lmList[8][0]<x+w and y<lmList[8][1]<y+h :
                #changing the color
                # create rectangles/button
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                # put text in the rectangle we just created                         size                thickness
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                #to fint the distance between the index finger and the middle finger
                l ,_ ,_ = detector.findDistance(8,12,img,draw=False)
                print(l)
                #to activate the click
                if l < 50:
                    # changing the color
                    # create rectangles/button
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    # put text in the rectangle we just created                         size                thickness
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if button.text=="del":
                        print("del")
                        finalText = finalText[:-1]
                    else:
                        finalText += button.text
                    sleep(0.2)

    #place holder for the text we will write
    # create rectangles/button
    cv2.rectangle(img, (30,350), (700,450), (175,0,175), cv2.FILLED)
    # put text in the rectangle we just created                         size                thickness
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)


    cv2.imshow("Image", img)
    cv2.waitKey(1)