# USAGE
# python recognize_video.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import glob
import os

Mainpath = "FaceRecog//"
# construct the argument parser and parse the arguments

def getImages(search_name):
	Minconfidence = 0.5
	embeddingPath = Mainpath+"output/embeddings.pickle"
	face_embeddingPath = Mainpath+"openface_nn4.small2.v1.t7"
	protoPath = Mainpath+"face_detection_model//deploy.prototxt"
	modelPath =Mainpath+"face_detection_model//res10_300x300_ssd_iter_140000.caffemodel"
	LabelPath = Mainpath+"output/le.pickle"
	recognizerPath = Mainpath+"output/recognizer.pickle"
	outputFaceFolder = Mainpath+"/InfectedPerson"
	PersonDetected = 0
	faceCount = 0
	From = 1012020
	To = 2012020
	dirs = glob.glob(Mainpath+"people_search/*.mp4")
	# load our serialized face detector from disk
	returnPaths = {}
	print("[INFO] loading face detector...")
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(face_embeddingPath)


	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open(recognizerPath, "rb").read())
	le = pickle.loads(open(LabelPath, "rb").read())


	# initialize the video stream, then allow the camera sensor to warm up


	# start the FPS throughput estimator


	# loop over frames from the video file stream
	print(dirs)
	for path in dirs:
		print(path)
		currfile = path.split("\\")
		filenam = currfile[len(currfile)-1]
		filenam = filenam.split("_")
		camname = filenam[0]
		viddate = int(filenam[1])	
		print(viddate)
		if (viddate >= From and viddate<=To):
			print("[INFO] starting video stream...")
			vs = cv2.VideoCapture(path)
			framerate = int(vs.get(cv2.CAP_PROP_FPS))
			framecount = 0
			fps = FPS().start()
			while True:
				# grab the frame from the threaded video stream
				suceess,frame = vs.read()
				framecount+=1
				if(suceess==False):
					PersonDetected = 0
					break	
				if framecount==framerate*2:
					framecount = 0
				# resize the frame to have a width of 600 pixels (while
				# maintaining the aspect ratio), and then grab the image
				# dimensions
				#frame = imutils.resize(frame, width=600)
					(h, w) = frame.shape[:2]

					# construct a blob from the image
					
					imageBlob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0),swapRB=True, crop=False)
					# apply OpenCV's deep learning-based face detector to localize
					# faces in the input image
					detector.setInput(imageBlob)
					detections = detector.forward()

					# loop over the detections
					for i in range(0, detections.shape[2]):
						# extract the confidence (i.e., probability) associated with
						# the prediction
						confidence = detections[0, 0, i, 2]

						# filter out weak detections
						if confidence > Minconfidence:
							# compute the (x, y)-coordinates of the bounding box for
							# the face
							box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
							(startX, startY, endX, endY) = box.astype("int")

							# extract the face ROI
							face = frame[startY:endY, startX:endX]
							(fH, fW) = face.shape[:2]

							# ensure the face width and height are sufficiently large
							if fW < 20 or fH < 20:
								continue

							# construct a blob for the face ROI, then pass the blob
							# through our face embedding model to obtain the 128-d
							# quantification of the face
							faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
								(96, 96), (0, 0, 0), swapRB=True, crop=False)
							embedder.setInput(faceBlob)
							vec = embedder.forward()

							# perform classification to recognize the face
							preds = recognizer.predict_proba(vec)[0]
							j = np.argmax(preds)
							proba = preds[j]
							name = le.classes_[j]

							if(name == search_name):

								PersonDetected = 1
							# draw the bounding box of the face along with the
							# associated probability
							
							'''
							text = "{}: {:.2f}%".format(name, proba * 100)
							y = startY - 10 if startY - 10 > 10 else startY + 10
							cv2.rectangle(frame, (startX, startY), (endX, endY),
								(0, 0, 255), 2)
							cv2.putText(frame, text, (startX, y),
								cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

							'''

					if PersonDetected==1:

						for i in range(0, detections.shape[2]):
						# extract the confidence (i.e., probability) associated with
						# the prediction
							confidence = detections[0, 0, i, 2]
							# filter out weak detections
							if confidence > Minconfidence:
								# compute the (x, y)-coordinates of the bounding box for
								# the face
								box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
								(startX, startY, endX, endY) = box.astype("int")

								# extract the face ROI
								face = frame[startY:endY, startX:endX]
								(fH, fW) = face.shape[:2]

								# ensure the face width and height are sufficiently large
								if fW < 20 or fH < 20:
									continue

								# construct a blob for the face ROI, then pass the blob
								# through our face embedding model to obtain the 128-d
								# quantification of the face
								faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
									(96, 96), (0, 0, 0), swapRB=True, crop=False)
								embedder.setInput(faceBlob)
								vec = embedder.forward()

								# perform classification to recognize the face
								preds = recognizer.predict_proba(vec)[0]
								j = np.argmax(preds)
								proba = preds[j]
								name = le.classes_[j]

								if(name=="unknown"):
									imgPath = outputFaceFolder+"//"+camname+"_"+str(faceCount)+".jpg"
									cv2.imwrite(imgPath,face)
									print(imgPath)
									returnPaths[faceCount] = imgPath
									faceCount = faceCount+1
								# draw the bounding box of the face along with the
								# associated probability
								
								'''
								text = "{}: {:.2f}%".format(name, proba * 100)
								y = startY - 10 if startY - 10 > 10 else startY + 10
								cv2.rectangle(frame, (startX, startY), (endX, endY),
									(0, 0, 255), 2)
								cv2.putText(frame, text, (startX, y),
									cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

								'''		
					# update the FPS counter
					PersonDetected = 0
					fps.update()
	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	print ("Total People Writtem" +str(faceCount))
	faceCount = 0
	return returnPaths
	# do a bit of cleanup

