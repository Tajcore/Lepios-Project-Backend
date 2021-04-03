import json
import pickle
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
import tflearn
from pathlib import Path
import nltk
from tensorflow.python.framework import ops

nltk.download('punkt')

root = Path('.')

training_data_path = root / "lepios_project_backend" / 'chat_model' /  'assets' / 'chatbot' /'training_data'
intents_path = root / "lepios_project_backend" / 'chat_model' / 'assets' /'chatbot' / 'intents.json'
model_path = root / "lepios_project_backend" / 'chat_model' / 'assets' /'chatbot' / 'model.tflearn'



symptoms_path =  root / "lepios_project_backend" / 'chat_model' / 'assets' /'symptoms_prediction' / 'data.json'
symptoms_model_path = root / "lepios_project_backend" / 'chat_model' / 'assets' / 'symptoms_prediction' / 'model_symptoms.tflearn'
training_data_symptoms = root / "lepios_project_backend" / 'chat_model' / 'assets' / 'symptoms_prediction' / 'training_data_symptoms'

# Load our pickled training dataset
data = pickle.load(open(training_data_path, "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

data_symptoms = pickle.load(open(training_data_symptoms, "rb"))
words_symptoms = data_symptoms['words']
classes_symptoms = data_symptoms['classes']
train_x_symptoms = data_symptoms['train_x']
train_y_symptoms = data_symptoms['train_y']

with open(intents_path) as json_data:
    intents = json.load(json_data)

with open(symptoms_path) as symptoms_data:
    symptoms = json.load(symptoms_data)



stemmer = LancasterStemmer()

ops.reset_default_graph()
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load(model_path)


ops.reset_default_graph()
net_symptom = tflearn.input_data(shape=[None, len(train_x_symptoms[0])])
net_symptom = tflearn.fully_connected(net_symptom, 8)
net_symptom = tflearn.fully_connected(net_symptom, 8)
net_symptom = tflearn.fully_connected(net_symptom, len(train_y_symptoms[0]), activation='softmax')
net_symptom = tflearn.regression(net_symptom)
model_symptoms = tflearn.DNN(net_symptom, tensorboard_dir='tflearn_symptoms_logs')
model_symptoms.load(symptoms_model_path)
