import os
import shutil
import tensorflow as tf
import pyqtgraph as pg

import tensorflow.keras.utils
import pickle
from tensorflow.keras import losses
import numpy as np
import pandas as pd
import ftfy
import nltk
import re
from nltk import PorterStemmer
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Conv1D, Dense, Input, Embedding, Dropout, Activation, MaxPooling1D, Flatten
from tensorflow.keras.models import load_model
import json
from collections import Counter
from PyQt5.QtCore import Qt, QThread, pyqtSignal




class Neural_Network():
    def __init__(self,optimizer='nadam',filters=250,batch_size = 40,epochs = 10,path_to_dataset="dataset.csv",train_distributaion=80,max_sequence_length=140,max_nb_words=12500,embedding_dim=400):
        """
        initialize an instance of the neural network class
        :param max_nb_words: Number of unique words in tokenizer
        :param path_to_dataset: the path to the current dataset we use
      """
        self.path_to_dataset=path_to_dataset
        self.train_distributaion=train_distributaion
        self.max_sequence_length = max_sequence_length # Max tweet size
        self.max_nb_words = max_nb_words
        self.embedding_dim = embedding_dim
        self.epochs = epochs
        self.filters = filters
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.model=None


    def __load_data_set(self):
        """
        load the csv file to a pandas object and treeming unnecessary column
        """
        self.tweets = pd.read_csv(self.path_to_dataset)
        self.tweets.drop(['Unnamed: 0'], axis=1, inplace=True)

    def load_model(self, model_name = "default"):
        path = "neural_network/" + model_name +"/"+model_name
        self.model = load_model(path +".h5")
        with open(path + ".pkl", 'rb') as handle:
            self.clean_tweets_dict = pickle.load(handle)
        with open(path+'.txt') as json_file:
            temp_dict = json.load(json_file)
            self.batch_size = temp_dict['params'][0]['batch_size']
            self.epochs = temp_dict['params'][0]['epochs']
            self.filters = temp_dict['params'][0]['filters']
            self.optimizer = temp_dict['params'][0]['optimizer']

    def save_model(self, model_name = "default"):
        dir= "neural_network/" + model_name
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        path = "neural_network/" + model_name +"/"+model_name
        self.model.save(path +".h5")
        with open(path+".pkl", 'wb') as handle:
            pickle.dump(self.clean_tweets_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            to_json={}
            to_json['params']=[]
            to_json['params'].append({
                'batch_size' : self.batch_size,
                'epochs' : self.epochs,
                'filters' : self.filters,
                'optimizer' : self.optimizer
            })
        with open(path+'.txt','w') as json_file:
            json.dump(to_json,json_file)

    def __pre_processing(self, data_set= False):
        """
        pre preocessing dataset
        """
        df = pd.read_csv("contractions.csv", usecols=['col1', 'col2'])
        contractions_dict = dict(zip(list(df.col1), list(df.col2)))
        self.message_list , self.label_list = [] , []
        c_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
        def expand_contractions(text, c_re=c_re):
            def replace(match):
                return contractions_dict[match.group(0)]
            return c_re.sub(replace, text)

        self.word2vec = KeyedVectors.load_word2vec_format("word2vec_twitter_tokens.bin", unicode_errors='ignore',
                                                          binary=True)

        count = Counter()
        for message , label in zip(self.tweets['message'] , self.tweets['label']):
            if re.match("(\w+:\/\/\S+)", message) == None:
                # remove hashtag, @mention, emoji and image URLs
                message = ' '.join(
                    re.sub("(@[A-Za-z0-9]+)|(\#[A-Za-z0-9]+)|(<Emoji:.*>)|(pic\.twitter\.com\/.*)", " ", message).split())

                #message = re.sub('(.*?)http.*?\s?(.*?)'," ", message)

                # fix weirdly encoded texts
                message = ftfy.fix_text(message)

                # expand contraction
                message = expand_contractions(message)

                # remove punctuation
                message = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", message).split())

                # stop words
                stop_words = set(stopwords.words('english'))
                word_tokens = nltk.word_tokenize(message)
                filtered_sentence = [w for w in word_tokens if not w in stop_words and w in self.word2vec.vocab]
                count.update(filtered_sentence)

                self.message_list.append(filtered_sentence)
                self.label_list.append(label)
        if(data_set):
            self.clean_tweets_dict = {j[0]: i for i, j in enumerate(count.most_common(12000))}
            self.clean_tweets_dict['UNK'] = 12001
            self.clean_tweets_dict['PAD'] = 12002

    def pre_processing(self,input):
        def deEmojify(inputString):
            return inputString.encode('ascii', 'ignore').decode('ascii')
        df = pd.read_csv("contractions.csv", usecols=['col1', 'col2'])
        contractions_dict = dict(zip(list(df.col1), list(df.col2)))
        self.message_list , self.label_list = [] , []
        c_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
        def expand_contractions(text, c_re=c_re):
            def replace(match):
                return contractions_dict[match.group(0)]
            return c_re.sub(replace, text)

        self.input_to_NN=[]
        for elm in input:
            tweet=elm[0]
            tweet = deEmojify(tweet)
            tweet = re.sub(r'http\S+', '', tweet)
            tweet = re.sub(r'#\S+', '', tweet)
            tweet = re.sub(r'@\S+', '', tweet)
            tweet.lower()
            tweet = expand_contractions(tweet)
            self.input_to_NN.append(tweet.split())


    def __embeddings(self):

        self.embedding_matrix = np.zeros((len(self.clean_tweets_dict)+1, self.embedding_dim))

        for (word, idx) in self.clean_tweets_dict.items():
                self.embedding_matrix[idx] = self.word2vec.word_vec(word)
        self.embedding_matrix[len(self.embedding_matrix)-1] = [0]*400 #add to pad

        print(self.embedding_matrix.shape)


    def __split_data(self):
        """
        spliting the dataset into training data and testing data by user's choice
        """
        total_tweets = len(self.tweets.index)
        self.train_dataset,self.train_dataset_label,self.test_dataset,self.test_dataset_label  = [],[],[],[]
        for i in range(0, len(self.message_list)):
            if np.random.uniform(0, 1) < (self.train_distributaion/100):
                self.train_dataset.append(self.message_list[i])
                self.train_dataset_label.append(self.label_list[i])
            else:
                self.test_dataset.append(self.message_list[i])
                self.test_dataset_label.append(self.label_list[i])

    def build_model(self,plot_losses):
        self.__load_data_set()
        self.__pre_processing(True)
        self.__embeddings()
        self.__split_data()

        self.__build_model()
        self.model.compile(loss=losses.mean_squared_error, optimizer=self.optimizer, metrics=['acc'])

        train_message_list_vector=[]
        for list in self.train_dataset:
            temp_list=[]
            for word in list:
                temp_list.append(self.clean_tweets_dict.get(word , 12001 ))
            for i in range(0 , (self.max_sequence_length - len(temp_list))):
                temp_list.append(self.clean_tweets_dict['PAD'])
            train_message_list_vector.append(temp_list)

        test_message_list_vector=[]
        for list in self.test_dataset:
            temp_list=[]
            for word in list:
                temp_list.append(self.clean_tweets_dict.get(word , 12001 ))
            for i in range(0 , (self.max_sequence_length - len(temp_list))):
                temp_list.append(self.clean_tweets_dict['PAD'])
            test_message_list_vector.append(temp_list)


        self.hist = self.model.fit(np.array(train_message_list_vector), np.array(self.train_dataset_label), \
                              validation_data=(np.array(test_message_list_vector), np.array(self.test_dataset_label)), \
                              epochs=int(self.epochs), batch_size=int(self.batch_size), shuffle=True, \
                              callbacks=[plot_losses])

        print(self.model.summary())

    def __build_model(self):
        self.model = Sequential()
        # Embedded layer
        self.model.add(Embedding(len(self.embedding_matrix), self.embedding_dim, weights=[self.embedding_matrix],
                            input_length=self.max_sequence_length, trainable=False))
        # Dropout Layer

        self.model.add(Dropout(0.2))
        # Convolutional Layer
        self.model.add(Conv1D(filters=int(self.filters), kernel_size=3, padding='same', activation='relu'))
        # Max pooling layer
        self.model.add(MaxPooling1D(pool_size=3))
        # Dropout Layer
        self.model.add(Dropout(0.2))
        # Dense Layer
        self.model.add(Dense(250,activation='relu'))
        self.model.add(Flatten())
        # Dense Layer
        self.model.add(Dense(1,activation='sigmoid'))#softmax?
        #plot_model(self.model, to_file='test.png')
        print(self.model.summary())


    class buildNeuralNetwork(QThread):
        taskFinished = pyqtSignal()
        update = pyqtSignal()
        def __init__(self,graphWidget_build_model,logger,optimizer='nadam',filters=250,batch_size = 40,epochs = 10):
            super(Neural_Network.buildNeuralNetwork, self).__init__()
            self.outter=Neural_Network(optimizer,filters,batch_size,epochs)
            self.plot_losses = Neural_Network.PlotLosses(logger,graphWidget_build_model)
        def run(self):
            self.outter.build_model(self.plot_losses)
            self.taskFinished.emit()


    class predict(QThread):
        taskFinished = pyqtSignal()
        def __init__(self,model_name,input):
            super(Neural_Network.predict, self).__init__()
            self.outter = Neural_Network()
            self.outter.load_model(model_name = model_name)
            self.outter.pre_processing(input)

        def run(self):
            message_list_vector=[]
            for tweet in self.outter.input_to_NN:
                temp=[]
                for word in tweet:
                    temp.append(self.outter.clean_tweets_dict.get(word , 12001 ))
                message_list_vector.append(temp)
            for tweet in message_list_vector:
                for i in range(0, (self.outter.max_sequence_length - len(tweet))):
                    tweet.append(self.outter.clean_tweets_dict['PAD'])
            message_list_vector_nparry=np.array(message_list_vector)
            print(message_list_vector_nparry.shape)
            self.result=self.outter.model.predict([message_list_vector_nparry])
            print(self.result)
            self.taskFinished.emit()


    class PlotLosses(tf.keras.callbacks.Callback):
        update = pyqtSignal()
        def __init__(self, logger,graphWidget_build_model):
            self.logger=logger
            self.graphWidget_build_model=graphWidget_build_model
            self.epoch=[]
            self.loss=[]
            self.val_loss=[]

        def on_epoch_begin(self, epoch, logs={}):
            line= 'starting epoch number: {}\n\n'.format(epoch+1)
            self.logger.appendPlainText(line)
            self.logger.horizontalScrollBar().setSliderDown(True)

        def on_epoch_end(self, epoch, logs={}):
            print(logs)
            self.epoch.append(epoch)
            self.loss.append(logs['loss'])
            self.val_loss.append(logs['val_loss'])
            self.graphWidget_build_model.clear()
            self.graphWidget_build_model.plot(self.epoch, self.loss,name="loss",pen=pg.mkPen(color=(0,0,0), width=2))
            self.graphWidget_build_model.plot(self.epoch, self.val_loss,name="val loss",pen=pg.mkPen(color=(10,25,200), width=2))
            self.graphWidget_build_model.setEnabled(True)

        def on_batch_end(self,batch, logs={}):
            line= 'loss is:{:.4f}   acc is {:.4f}\n'.format(logs['loss'],logs['acc'])
            self.logger.appendPlainText(line)


        def on_train_end(self,logs={}):
            self.logger.appendPlainText("Finished!")



