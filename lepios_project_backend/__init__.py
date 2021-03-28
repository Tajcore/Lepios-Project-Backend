import json
import pickle
from nltk.stem.lancaster import LancasterStemmer
import tflearn
from pathlib import Path
import nltk
nltk.download('punkt')

root = Path('.')

training_data_path = root / "lepios_project_backend" / 'chat_model' / 'assets' /'training_data'
intents_path = root / "lepios_project_backend" / 'chat_model' / 'assets' / 'intents.json'
model_path = root / "lepios_project_backend" / 'chat_model' / 'assets' / 'model.tflearn'

# Load our pickled training dataset
data = pickle.load(open(training_data_path, "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


with open(intents_path) as json_data:
    intents = json.load(json_data)

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
stemmer = LancasterStemmer()

# load our saved model
model.load(model_path)
