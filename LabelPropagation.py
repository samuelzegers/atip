import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import torch
from tqdm import tqdm

class LabelPropagation:
    def __init__(self, adj_matrix, labels):
        self.norm_adj_matrix = self.matnorm(adj_matrix)
        self.n_nodes = adj_matrix.shape[0]
        self.labels_unwrapped = None 
        self.n_cats = int(np.max(labels) + 1)
        self.labels = labels
        self.predictions = None
    
    '''calculating the matrix we want to multiply with in the algorithm'''
    def matnorm(self, adj_matrix):
        deg = adj_matrix.sum(axis=1)
        deg[deg == 0] = 1
        return adj_matrix/deg[:, None]
    
    '''implementing the label propagation step'''
    def labprop(self):
        self.predictions = np.matmul(self.norm_adj_matrix, self.predictions)
        self.predictions[self.labels>0, :] = 0
        self.predictions[self.labels>0, self.labels[self.labels>0].astype(int)] = 1
        self.predictions[self.labels==0, :] = 0
        self.predictions[self.labels==0, self.labels[self.labels==0].astype(int)] = 1

    def unwrap(self, labels):
        self.labels_unwrapped = np.zeros((self.n_nodes, self.n_cats))
        self.labels_unwrapped[np.nonzero(labels), labels[np.nonzero(labels)].astype(int)] = 1
        self.labels_unwrapped[labels==-1, :] = 0
        self.labels_unwrapped[labels==0, labels[labels==0].astype(int)] = 1

    def fit(self, labels, max_iter, error):
        self.unwrap(labels)
        self.predictions = np.copy(self.labels_unwrapped)
        prevstep = np.zeros((self.n_nodes, self.n_cats))
        for i in tqdm(range(max_iter)):
            dif = np.sum(np.absolute(self.predictions-prevstep))
            if dif < error:
                print(f"The method stopped after {i} iterations with error={dif:.4f}.")
                break
            prevstep = np.copy(self.predictions)
            self.labprop()

    def prediction(self):
        return np.argmax(self.predictions, axis=1)