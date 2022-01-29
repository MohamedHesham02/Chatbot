import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

# Initialize required lists
words=[] # bag of words in dataset
classes = [] 
documents = [] # classifying every sentence by labels 
ignore_words = ['?', '!'] # removed chars

#import our dataset
data_file = open('data.json').read() 
intents = json.loads(data_file) 

# doing morphological analysis of the words to get the base words 
lemmatizer = WordNetLemmatizer()

for intent in intents['intents']:
    for pattern in intent['patterns']:

        #tokenize each word by splitting a piece of text into individual words 
        w = nltk.word_tokenize(pattern)
        #form bag of words 
        words.extend(w)
        #add documents in the corpus
        documents.append((w, intent['tag']))

        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmaztize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

# sorting of words and classes to shuffle the dataset
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# documents = combination between patterns and intents
print (len(documents), "documents")
# classes = intents
print (len(classes), "classes", classes)
# words = all words, vocabulary
print (len(words), "unique lemmatized words", words)

# save words and classes as pkl
pickle.dump(words,open('texts.pkl','wb'))
pickle.dump(classes,open('labels.pkl','wb'))

# create our training data
training = []

# create an empty array for our output as a transaction station to output_row of each example or sentence 
output_empty = [0] * len(classes)

# training set, bag of words for each sentence (looping over every sentence to classify each one by 1 for right class and 0 for other classes) like one hot encoding 
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0) 
    
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    # classify each word by 1 for right class and 0 for other classes
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    # bag is words of specific class in words list but in shape of 1s and 0s
    # output_row represent label in shape of one hot encoding
    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")


# Create basic neural network structure (complex ones are not needed for simple dataset like this to avoid overfitting)
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent for backpropagation with Nesterov accelerated gradient gives good results for this model 
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)
model.save('model.h5', hist)

print("model created")
