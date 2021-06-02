# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound


###################################################################################################
from app.home.backend.pair.pairing import getRecipeAndWine
from app.home.backend.present.presenting import getSommelier


from flask import flash
import os
from app.home.forms import AIcookForm
import pandas as pd


# aicook
# import sys
# sys.path.insert(0, './yolov5')
# #sys.path.insert(0,'/cook/backend/detect/yolov5')
# #sys.path.insert(0,'\AIcook\backend\detect\yolov5')
# import backend.detect.yolov5.detect_aicook as detect_aicook

import torch
import cv2
y5 = torch.hub.load('ultralytics/yolov5', 'custom', path='app/home/backend/detect/yolov5/aicook.pt',force_reload=True)

y5.conf = 0.6



from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#some globals to use in the various front-end sections
pairing_txt = ''
presenting_txt = ''
filename = ''
top_ingredients_txt = [pd.DataFrame().to_html(index=False, classes='table tablesorter')]


def doDetection(inputfile):
    top = 50
    filename = secure_filename(inputfile.filename)
    base_img = os.path.join('app/base/static/uploads/', filename)
    inputfile.save(base_img)
                
    # Inference
    y5Result = y5(base_img)
    
    #render boxes on image
    y5Result.render() 
    
    target_img =   cv2.rotate(cv2.cvtColor( y5Result.imgs[0], cv2.COLOR_BGR2RGB), cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    cv2.imwrite(base_img.replace('/uploads/','/uploads/exp/'),target_img)    
    
    top_ingredient_names = y5Result.pandas().xyxy[0].loc[:, ['name']].to_string()           
    top_ingr = y5Result.pandas().xyxy[0].loc[:top-1, ['confidence','name']]
    top_ingredients_display = [top_ingr.to_html(index=False, classes='table tablesorter')]    

    return filename, top_ingredients_display, top_ingredient_names
    
    
def doPairing(ingr):
    if ingr:
        return getRecipeAndWine(ingr)        
    else:
        flash('No ingredients supplied','pair')
    
        
def dopresenting(menu):
    if menu:
        return getSommelier(menu)
    else:
        flash('No menu supplied', 'present')
    


@blueprint.route('/cook', methods=['GET', 'POST'])
def cook():
    global pairing_txt, presenting_txt, filename, top_ingredients_txt
        
    aicookF = AIcookForm(request.form)
    
    
    if 'btn_detect' in request.form:

        if 'detect_image' not in request.files:
            flash('No file part', 'detect')
            return redirect(request.url)
        
        file = request.files['detect_image']
        
        if file.filename == '':
            flash('No image selected for uploading...', 'detect')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):

            filename, top_ingredients_txt, _ = doDetection(file)            

            return render_template('cook.html', 
                                   form=aicookF, 
                                   filename= filename, 
                                   top_ingredients= top_ingredients_txt,
                                   pairing = pairing_txt,
                                   presenting = presenting_txt
                                   )
                                   
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif','detect')
            return redirect(request.url)        

    elif 'btn_all' in request.form:        
        
        if 'detect_image' not in request.files:
            flash('No file part', 'detect')
            return redirect(request.url)
        
        file = request.files['detect_image']
        
        if file.filename == '':
            flash('No image selected for uploading...', 'detect')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):

            filename, top_ingredients_txt, ingr_names = doDetection(file)            
            
            pairing_txt = doPairing(ingr_names)        
            
            presenting_txt = dopresenting(pairing_txt)
            
            return render_template('cook.html', 
                                   form=aicookF, 
                                   filename= filename, 
                                   top_ingredients= top_ingredients_txt,
                                   pairing = pairing_txt,
                                   presenting = presenting_txt
                                   )
                                   
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif','detect')
            return redirect(request.url)        


        
        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_txt,
                               pairing = pairing_txt,
                               presenting = presenting_txt
                               )


    elif 'btn_pair' in request.form:        

        pairing_txt = doPairing(request.form['pair_ingredients'])

        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_txt,
                               pairing = pairing_txt,
                               presenting = presenting_txt
                               )

    elif 'btn_present' in request.form:    
        presenting_txt = dopresenting(request.form['present_menu'])

        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_txt,
                               pairing = pairing_txt,
                               presenting = presenting_txt
                               )

    elif 'btn_reset' in request.form:
        #reset all global variables
        pairing_txt = ''
        presenting_txt = ''
        filename = ''
        top_ingredients_txt = [pd.DataFrame().to_html(index=False, classes='table tablesorter')]
        
        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_txt,
                               pairing = pairing_txt,
                               presenting = presenting_txt
                               )
    
    return render_template('cook.html', form=aicookF, filename= '')


@blueprint.route('/uploads/<filename>')
def display_orig_image(filename):
    #flash('display_image filename: ' + filename)
    return redirect(url_for('static', filename= 'uploads/' +filename), code=301)
    #return redirect(request.url)  


@blueprint.route('/uploads/exp/<filename>')
def display_detection_image(filename):
    #flash('display_image filename: ' + filename)
    return redirect(url_for('static', filename= 'uploads/exp/' +filename), code=301)
    #return redirect(request.url)  
    
###################################################################################################



@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
     
