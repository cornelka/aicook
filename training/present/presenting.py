from random import randint
from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

#front-end interface
def getSommelier(recipeInfo, context=True):
    if recipeInfo.empty:
        tmptxt = 'This bottle is empty'
    else:    
        tmptxt =  generate_review(recipeInfo,context)
    return tmptxt


# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# generate a sequence from a language model
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
	result = list()
	in_text = seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		# truncate sequences to a fixed length
		encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
		# predict probabilities for each word
		yhat = model.predict_classes(encoded, verbose=0)
		# map predicted word index to word
		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break
		# append to input
		in_text += ' ' + out_word
		result.append(out_word)
	return ' '.join(result)

	
def generate_review(df,context):

    # writing standard text
    if df.empty:
        text = 'No input received'
    else:
                    
        df2 = df.iloc[0] # limit to 1 row
        
        #
        if context:
        #df2['variety_display'] = df2['variety_list'].apply(lambda ttl: ', '.join(ttl))
            df2['wineclass_display'] = ', '.join(df2['wineclass_list'] )
            if df2['designation'] is None:
                text = f"We can recommend a {df2['wineclass_display']} wine priced at about ${df2['price']}. Made with {df2['variety']} grapes from {df2['country']} it is a perfect beverage to accompany your dish."
            else:
                text = f"We can recommend {df2['designation']}, a {df2['wineclass_display']} wine priced at about ${df2['price']}. Made with {df2['variety']} grapes from {df2['country']} it is a perfect beverage to accompany your dish."
        else:
            text=''
            
        #print(string)
    
        seq_length = 50
        
        basepath = 'app/home/backend/present/'
        
        # load the model
        model = load_model(basepath + 'model_prop_8k_100x.h5')
    
        # load the tokenizer
        tokenizer = load(open(basepath + 'tokenizer.pkl', 'rb'))
    
        # select a seed text
        #seed_text = ' '.join(df2['description'].str.split(' ').str[0:5])
        #seed_text = df2['description'].astype(str)
        seed_text = ' '.join(df2['description'].split()[:5])
        
        text += ' ' + seed_text
        #print(seed_text + '\n')
    
        # generate new text
        generated = generate_seq(model, tokenizer, seq_length, seed_text, 50)
        text += ' ' + generated
        #print(generated)
    
    return text
