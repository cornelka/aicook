# bestanden van het gpt-2 model dat ik heb proberen te implementeren

1. het train.py bestand dat ik heb gebruikt om het model te trainen 

2. in de bestanden genaamd negerate_unconditional_samples.py en interactive_conditional_samples.py 
heb ik wat proberen mijn eigen modellen te vervangen met het pre-trained 124M model, door de directory argument 
te veranderen bij 'model_name' (lijn 12 of 13), maar het gebruik van de het enc object (een klasse uit encoder.py)
bleef voor mij te complex om verder te gaan

3. ik kon niet alle bestanden uploaden naar de drive omdat m'n opslagcapaciteit dan vol zou zijn, dus je kan de andere bestanden vinden op
https://github.com/nshepperd/gpt-2

4. het grootste deel van de tijd die ik heb besteed aan gpt-2 bestond uit debuggen, dus zien dat ik tensorflow kon gebruiken 
op mijn computer, de juiste versies weten te installeren van de nodige packages, 
sommige import statements doen werken (zie lijn 72-77 in train.py), 
omgevingsvariabelen in orde brengen om python te kunnen gebruiken in de command line, 
Anaconda 5x installeren tot ik op een magische wijze een 3-tal foutmeldingen niet meer krijg in verband met de virtual env,
dan eens het werkte op mijn PC beseffen dat ik toch GPU nodig zal hebben om geconfronteerd te worden met de foutmelding van Azure,
daarmoest ik cdu installeren, weten te navigeren tussen de bestanden die niet zichtbaar zijn, 
een programma downloaden (FileZilla) om bepaalde bestanden te kunnen uploaden naar Azure die nodig zijn om tensorflow te doen werken,
etc. etc. 

Wanneer ik dan even verder was met het implementeren op Azure was mijn studentenkrediet op en kon ik niet meer aan m'n bestanden 
zonder eerst nieuw krediet te kopen, wat dan nog eens enorm duur was, dus dat was zowat de druppel en ben ik maar beginnen zoeken naar een alternatief