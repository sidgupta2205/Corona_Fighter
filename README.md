# Corona_Fighter
Smart Survellience System Using AI
This system consists of main 4 parts
1. Crowd Detection
2. People and contact search
3. Person tracking across cameras
4. Live view of cameras


To run this project follow the following instructions
Downloading and extract dataset and weights at proper locations

1. Clone the project in your syste
2. Download these test dataset from the following link
3. Extract Test_cities.zip in Smart_survelliance_system folder
4. Extract config.zip and classifier.zip in Smart_survelliance_system folder
5. Extract yolo.zip in Smart_survelliance_system folder
6. Extract  people_search.zip in Smart_survelliance_system/micro_server/FaceRecog folder
7. Extract  people_search_dataset.zip in Smart_survelliance_system/micro_server/FaceRecog folder
8. Extract  dataset.zip in Smart_survelliance_system/micro_server/FaceRecog folder
9. Extract  openface_nn4.small2.v1.zip in Smart_survelliance_system/micro_server/FaceRecog folder 

To run the system follow these instructions(Windows command line)

cd into the project directory of Smart_survelliance_system
python micro_server/FaceRecog/extract_embeddings.py
python micro_server/FaceRecog/train_model.py
python micro_server/people_count.py
python micro_server/REALTIMEMONITOR.py
python micro_server/server.py(Do not close the cmd)


Start a xampp server
open localhost/smart survelliance/html/Live_page.html
