import os
import csv
from matplotlib import pyplot as plt
import sys

class gui_services():

    def __init__(self):
        pass

    def extract_files_to_list(self):
        """
        insert files paths to self.models_folder_list
        """
        path = "neural_network"
        models_folder_list = [f.name for f in os.scandir(path) if f.is_dir()]
        return models_folder_list

    def append_dict_as_row(self, dict):
        """
        :param dict: insert to csv file
        """
        with open("analyze_results.csv", 'a+', newline='') as file:
            field_names = ["timestamp", "twitter_username", "tweets_amount", "avg", "model_name", "graph_x",
                           "graph_y"]
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writerow(dict)
    def plot(self,tmp_lst,twt_lst):
        lst_x = tmp_lst[0]
        lst_y = tmp_lst[1]
        #erasing "[,]" brackets
        lst_x = lst_x.replace("[", "").replace("]", "")
        split_x = lst_x.split(",")
        self.split_x_lst = []
        for i in split_x:
            self.split_x_lst.append(float(i) + 1)
        lst_y = lst_y.replace("[", "").replace("]", "")
        split_y = lst_y.split(",")
        self.split_y_lst = []
        for i in split_y:
            self.split_y_lst.append(float(i))
        plt.title("Depression severity per tweet: {}".format(twt_lst))
        plt.xlabel("Tweets")
        plt.ylabel("Depression Severity")
        plt.plot(self.split_x_lst, self.split_y_lst)
        plt.show()

    def save_model_summary(self, model, name):
        """
        saving model summary as external file
        :param model: created model
        :param name: the name of the new model on file
        """
        orig_stdout = sys.stdout
        f = open("model_history/" + name + ".txt", 'w')
        sys.stdout = f
        print(model.summary())
        sys.stdout = orig_stdout
        f.close()