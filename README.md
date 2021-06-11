# aicook AKA aisommelier

## Presentation
See the presentation folder. The presentation contains all links to external sources (youtube, wandb,roboflow,docker,github,...)

## Exploration & model training
See the training folder. This is devided into the 3 main application parts: 
- detect (vision: ingredient detection)
- pair (NLP/NER : food, wine and their pairing)
- present (text generation: Sommelier text)

## Application 
This consists of all the other files and folders. The customised part is primarily situated under /app/home/
- routes.py that handles the main page logic
- a backend folder with subfolders for the 3 parts detect, pair and present
- in the pair directory datafiles are needed which can be found at https://drive.google.com/file/d/1IfobqPeQ0n1STARLhlwXOca-AO2iNHAm/view?usp=sharing

## Live version
https://aisommelier.azurewebsites.net/

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

### Startup
1. cd aicook
2. python run.py

### Use
http://yourhost:5000/
