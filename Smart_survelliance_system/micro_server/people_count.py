# read video
import cv2
import numpy as np
import glob
import traceback

confid = 0.5
thresh = 0.5
dirs = glob.glob("..\\Test_cities\\*.mp4")


def calibrated_dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + 550 / ((p1[1] + p2[1]) / 2) * (p1[1] - p2[1]) ** 2) ** 0.5


def isclose(p1, p2):
    c_d = calibrated_dist(p1, p2)
    calib = (p1[1] + p2[1]) / 2
    if 0 < c_d < 0.15 * calib:
        return 1
    elif 0 < c_d < 0.2 * calib:
        return 2
    else:
        return 0



count = 0 
maxcount = 4
maxhighcount = 3
checkcount = 0
mintest = 3
label = "HEAVY CROWD!!!!!"
labelsPath = "../yolo/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")
np.random.seed(42)
weightsPath = "../yolo/yolov3.weights"
configPath = "../yolo/yolov3.cfg"
fl = 0
q = 0
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

for path in dirs:
    cap = cv2.VideoCapture(path)
    framerate = int(cap.get(cv2.CAP_PROP_FPS))
    framecount = 0
    count = 0
    currfile = path.split("\\")
    filenam = currfile[len(currfile)-1]
    filenam = filenam.split("_")
    camname = filenam[0]
    filenam = filenam[1]
    print("reading path "+filenam)
    while(True):
        # Capture frame-by-frame
        success, frame = cap.read()
        framecount += 1
        #print ("reading image")
        # Check if this is the frame closest to 10 seconds
        if framecount == (framerate * 10):
            framecount = 0
            try:
                (H, W) = frame.shape[:2]
                print(H)
                print(W)
                q = W
                frame = frame[0:H, 200:q]
                
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                            swapRB=True, crop=False)
                net.setInput(blob)
                detections = net.forward(ln)
                
                print ("DETECTING")

                boxes = []
                confidences = []
                classIDs = []

                for output in detections:
                    for detection in output:
                        scores = detection[5:]
                        classID = np.argmax(scores)
                        confidence = scores[classID]
                        if LABELS[classID] == "person":
                            #print (confidence)
                            if confidence>confid:
                                box = detection[0:4] * np.array([W, H, W, H])
                                (centerX, centerY, width, height) = box.astype("int")

                                x = int(centerX - (width / 2))
                                y = int(centerY - (height / 2))

                                boxes.append([x, y, int(width), int(height)])
                                confidences.append(float(confidence))
                                classIDs.append(classID)
                            #print(idx);

                idxs = cv2.dnn.NMSBoxes(boxes, confidences, confid, thresh)


                if len(idxs) > 0:

                    status = list()
                    idf = idxs.flatten()
                    close_pair = list()
                    s_close_pair = list()
                    center = list()
                    dist = list()
                    for i in idf:
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])
                        center.append([int(x + w / 2), int(y + h / 2)])

                        status.append(0)
                    
                    for i in range(len(center)):
                        for j in range(len(center)):
                            g = isclose(center[i], center[j])

                            if g == 1:

                                close_pair.append([center[i], center[j]])
                                status[i] = 1
                                status[j] = 1
                            elif g == 2:
                                s_close_pair.append([center[i], center[j]])
                                if status[i] != 1:
                                    status[i] = 2
                                if status[j] != 1:
                                    status[j] = 2

                    total_p = len(center)
                    low_risk_p = status.count(2)
                    high_risk_p = status.count(1)
                    safe_p = status.count(0)


                if total_p>=maxcount:
                    checkcount = checkcount +1
                elif high_risk_p >=maxhighcount:
                    checkcount = checkcount +1    
                else :
                    checkcount = 0     
                
                print(checkcount)
                if checkcount >= mintest:
                    print("Heavy crowd detected in area")
                    times =cap.get(cv2.CAP_PROP_POS_MSEC)
                    
                    with open("../shared_file/shared.txt", "r+") as f:
                        d = f.readlines()
                        f.seek(0)
                        for i in d: 
                            linesplit = i.split(" ")
                            if linesplit[0] != camname:
                                f.write(i)
                        f.truncate()

                    with open("../shared_file/shared.txt", "a+") as f:
                        print(camname+" "+filenam+" "+ str(times))
                        f.write(camname+" "+filenam+" "+ str(times)+" \n")                
                    #cv2.putText(image, label, (0, 100),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255),thickness=3)
                    #cv2.imshow("Output", image)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows() 
                        
            except Exception as e:
                traceback.print_exc()

                break
        # Check end of video
            print("Total people Count "+ str(total_p))
            count = 0
        
    # When everything done, release the capture
    # capture frame from video
    # count people in video
    # output if people are more than mentioned