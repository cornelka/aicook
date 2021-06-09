# aicook AKA aisommelier

### Public version
https://aisommelier.azurewebsites.net/

### Presentation

### Exploration &model training
See the training folder



## Installation
### A. Use the accompanied docker file

### B. manual deploy
1. git clone https://github.com/cornelka/aicook
2. cd aicook
3. pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt #yoloV5 requirements
(On azure you might see that matplotlib has a too high versin, but this is not an issue for our use-case)
5. pip install -r requirements.txt #front end template requirements
6. pip install torch
7. pip install imgaug
8. pip install tensorflow==2.4.0
9. pip install keras==2.4.3
10. request download pair.zip from google drive for pairing and unpack it under aicook/app/home/backend/pair

## Startup
1. cd aicook
2. python run.py

## Use
http://yourhost:5000/
