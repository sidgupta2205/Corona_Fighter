# Corona_Fighter
Smart Survellience System Using AI
This system consists of main 4 parts
1. Crowd Detection
2. People and contact search
3. Person tracking across cameras
4. Live view of cameras

Download Dataset and model from this link - https://drive.google.com/open?id=13dsrlzxqt7jIZ4kb09GW1jHIG-533eYm


- System is already trained for 3 persons
1. shahrukh
2. irfan
3. ayushman 

To run this project follow the following instructions
Downloading and extract dataset and weights at proper locations

1. Clone the project in your syste
2. Download these test dataset from the following link
3. Extract Test_cities.zip in Smart_survelliance_system folder
4. Extract config.zip and classifier.zip in Smart_survelliance_system folder
5. Extract yolo.zip in Smart_survelliance_system folder
6. Extract  people_search.zip in Smart_survelliance_system/micro_server/FaceRecog folder
7. Extract  people_search_dataset.zip in Smart_survelliance_system/micro_server/FaceRecog folder
8. Extract  dataset.zip and face_detection_model in Smart_survelliance_system/micro_server/FaceRecog folder
9. Extract  openface_nn4.small2.v1.zip in Smart_survelliance_system/micro_server/FaceRecog folder 

To run the system follow these instructions(Windows command line)

cd into the project directory of Smart_survelliance_system

python micro_server/people_count.py

python micro_server/REALTIMEMONITOR.py

python micro_server/server.py(Do not close the cmd)

Start a xampp server
open localhost/smart survelliance/html/Live_page.html

To train system with new person 
 - Goto people search in UI
 - Upload zip file with name of person as filename
 - Inside zip there must be a folder which contains all the images of person, folder name must be the name of person
 (Example is available in Smart_survelliance_system\html\uploads)
 - Upload Image , once the zip is uploaded successfully
- Press Train now to train the system with new person images
System is successfully trained for a new person.