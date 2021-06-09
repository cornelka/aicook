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


from imgaug import augmenters as iaa
import torch
import cv2
from werkzeug.utils import secure_filename

y5 = torch.hub.load('ultralytics/yolov5', 'custom', path='app/home/backend/detect/yolov5/aicook.pt',force_reload=True)
y5.conf = 0.6

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#some globals to use in the various front-end sections
recipe_display = ''
pairing_display = ''
presenting_display = ''
filename = ''
top_ingredients_display = ''

def resize(img):
    #resize the image to a square + also scale the bounding boxes
    #we assume that the image is vertically oriented and fill the edge with black pixels

    SIZE= 640    
    prepro = iaa.Sequential([
        iaa.Resize({"height": SIZE, "width": "keep-aspect-ratio"}),
        iaa.CenterPadToFixedSize(height=SIZE, width=SIZE)    

    ], random_order=False)

    return prepro(image=img)


def doDetection(inputfile):
    
    filename = secure_filename(inputfile.filename)
    base_img_path = os.path.join('app/base/static/uploads/', filename)
    inputfile.save(base_img_path)
    
    # resize the original image
    base_img = cv2.imread(base_img_path)    
    scaled_img = resize(base_img)        
    
    scaled_img_path = os.path.join('app/base/static/uploads/', 'scaled_' + filename)    
    cv2.imwrite(scaled_img_path, scaled_img)    
    
    # Inference using YOLOv5 with own aicook weigths
    y5Result = y5(scaled_img_path)
    
    #render boxes on image
    y5Result.render() 
        
    #change image color for correct visualisation
    target_img = cv2.cvtColor( y5Result.imgs[0], cv2.COLOR_BGR2RGB)
    
    #save resulting image (still scaled) with bounding boxes
    cv2.imwrite(base_img_path.replace('/uploads/','/uploads/exp/'),target_img)    
    
    #get the detected labels(ingredients)
    if y5Result.pandas().xyxy[0].empty:
        flash('No ingredients found in this image','detection_result')     
        return filename, '', None
    else:
        top_ingredient_names = y5Result.pandas().xyxy[0].loc[:, ['name']]
        top_ingredient_names.rename(columns={'name': 'food'}, inplace=True) #pairing expects a food column
    
        # visualize the top ingredients with their confidence scores
        top = 50    
        top_ingr = y5Result.pandas().xyxy[0].loc[:top-1, ['confidence','name']]    
        top_ingredients_disp = [top_ingr.to_html(index=False, classes='table tablesorter')]    

        return filename, top_ingredients_disp, top_ingredient_names
    
    
def doPairing(ingr):
    if ingr is None:
        flash('No ingredients supplied','pair')      
        return None,'',''
        
    elif ingr.empty:
        flash('No ingredients supplied','pair')
        return None,'',''
    
    elif ingr.dropna().empty:
        flash('No ingredients supplied','pair')     
        return None,'',''
    
    elif len(ingr['food']) == 0:
        flash('No ingredients supplied','pair')        
        return None,'',''
    
    else:
        dfRecipe, dfWine = getRecipeAndWine(ingr)   
        
        if dfRecipe is not None:        
            
            dfRecipe['top_ingredients'] = dfRecipe['ingredient_top_match'].apply(lambda ttl: ', '.join(ttl))
            dfRecipe.rename(columns={'title': 'recipe'}, inplace=True)
            recipe_display = [dfRecipe.loc[:,['recipe','top_ingredients']].to_html(index=False, classes='table tablesorter')]   
        else:
            recipe_display = [pd.DataFrame(columns=['recipe'], data=[['No recipe found']]).to_html(index=False, classes='table tablesorter')]   
        

        if dfWine is not None:
            dfWine.rename(columns={'title': 'wine'}, inplace=True)            
            pair_display =  [dfWine.loc[:,['wine','country', 'winery', 'variety', 'description']].to_html(index=False, classes='table tablesorter')]   

        else:
            pair_display = [pd.DataFrame(columns=['wine'], data=[['No wine found']]).to_html(index=False, classes='table tablesorter')]   
            
        
        return dfWine, pair_display, recipe_display    
        
        
def dopresenting(wine, context):   

    if wine is None:
        flash('No wine info supplied', 'present')
        return ''
        
    elif wine.empty:
        flash('No wine info supplied', 'present')
        return ''
    
    elif wine.dropna(how='all').empty:
        flash('No wine info supplied', 'present')
        return ''
    
    elif len(wine['description']) == 0:
        flash('No wine info supplied', 'present')
        return ''

    elif wine['description'].values.size == 0:
        flash('No wine info supplied', 'present')
        return ''
        
    else:
        presentation = getSommelier(wine, context)

        return presentation
        

@blueprint.route('/cook', methods=['GET', 'POST'])
def cook():
    global pairing_display, presenting_display, filename, top_ingredients_display,recipe_display
        
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

            filename, top_ingredients_display, _ = doDetection(file)            

            return render_template('cook.html', 
                                   form=aicookF, 
                                   filename= filename, 
                                   top_ingredients= top_ingredients_display,
                                   pairing = pairing_display,
                                   recipe = recipe_display,
                                   presenting = presenting_display
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

            filename, top_ingredients_display, ingr_names = doDetection(file)                    
        
            pairing, pairing_display,recipe_display = doPairing(ingr_names)                    
            
            presenting_display = dopresenting(pairing,True)
            
            return render_template('cook.html', 
                                   form=aicookF, 
                                   filename= filename, 
                                   top_ingredients= top_ingredients_display,
                                   pairing = pairing_display,
                                   recipe = recipe_display,                                   
                                   presenting = presenting_display
                                   )
                                   
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif','detect')
            return redirect(request.url)        


        
        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_display,
                               pairing = pairing_display,
                               recipe = recipe_display,                               
                               presenting = presenting_display
                               )


    elif 'btn_pair' in request.form:        
        if request.form['pair_ingredients'] == '':
            ingr_input = None 
        else:
            ingr_input = pd.DataFrame(request.form['pair_ingredients'].split(','),columns=['food'] )

        _, pairing_display, recipe_display = doPairing(ingr_input)

        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_display,
                               pairing = pairing_display,
                               recipe = recipe_display,                               
                               presenting = presenting_display
                               )

    elif 'btn_present' in request.form:    
        if request.form['present_wine'] == '':
            present_input = None
        else:
            present_input = pd.DataFrame( [request.form['present_wine']] ,columns=['description'] )                
            
        presenting_display = dopresenting(present_input, False)

        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_display,
                               pairing = pairing_display,
                               recipe = recipe_display,                               
                               presenting = presenting_display
                               )

    elif 'btn_reset' in request.form:
        #reset all global variables
        pairing_display = ''        
        recipe_display = ''
        presenting_display = ''
        filename = ''
        top_ingredients_display = ''
        aicookF.pair_ingredients.data = ''
        aicookF.present_wine.data = ''
                
        return render_template('cook.html', 
                               form=aicookF, 
                               filename=filename, 
                               top_ingredients= top_ingredients_display,
                               pairing = pairing_display,
                               recipe = recipe_display,                               
                               presenting = presenting_display
                               )
    
    return render_template('cook.html', form=aicookF, filename= '')


@blueprint.route('/uploads/<filename>')
def display_orig_image(filename):
    return redirect(url_for('static', filename= 'uploads/' +filename), code=301)


@blueprint.route('/uploads/exp/<filename>')
def display_detection_image(filename):
    return redirect(url_for('static', filename= 'uploads/exp/' +filename), code=301)
    
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
     
