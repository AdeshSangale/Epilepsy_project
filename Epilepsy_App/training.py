import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import nolds  # For DFA
import pyeeg
import warnings
from time import sleep
from joblib import dump
from sklearn.model_selection import train_test_split
import seaborn as sbn

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

# Import each and every file

dirB = "./Datasets/setB/"
tempB = sorted([os.path.join(dirB, file) for file in os.listdir(dirB)])  # class: 1 val: -1

dirC = "./Datasets/setC/"
tempC = sorted([os.path.join(dirC, file) for file in os.listdir(dirC)])  # class: 2 val: 0

dirE = "./Datasets/setE/"
tempE = sorted([os.path.join(dirE, file) for file in os.listdir(dirE)])  # class: 3 val: 1

def load_data(temp):
    data_list = []
    for i, file in enumerate(temp):
        x = pd.read_table(file, header=None)
        x.columns = [f'A{i}']
        data_list.append(x)
    return data_list

tb = load_data(tempB)
tc = load_data(tempC)
te = load_data(tempE)

def table(table):
    big_table = pd.concat(table, axis=1)
    return big_table

bigB = table(tb)
bigC = table(tc)
bigE = table(te)

head = bigB.columns.values
a = len(bigB.columns)
print(a)

b = bigB.head(10)
print(b)

# Create a matrix
def create_mat(mat):
    matx = np.zeros((len(mat), len(head)))
    for i in range(len(head)):
        matx[:, i] = mat[head[i]]
        sleep(0.01)
    return matx

matB = create_mat(bigB)
matC = create_mat(bigC)
matE = create_mat(bigE)

matB = np.nan_to_num(matB)
matC = np.nan_to_num(matC)
matE = np.nan_to_num(matE)

# Plotting the data
hl, = plt.plot(matB[0], label='healthy')
trans, = plt.plot(matC[0], label='Inter-ictal')
seizure, = plt.plot(matE[0], label='seizures')
plt.legend(handles=[hl, trans, seizure])
plt.savefig("fig1.png")

# Feature extraction
def features(mat):
    Kmax = 5
    Tau = 4
    DE = 10
    M = 10
    R = 0.3
    Band = np.arange(1, 86)
    Fs = 173
    DFA = nolds.dfa(mat)
    HFD = pyeeg.hfd(mat, Kmax)  # Assuming pyeeg has this function
    SVD_Entropy = pyeeg.svd_entropy(mat, Tau, DE)
    Fisher_Information = pyeeg.fisher_info(mat, Tau, DE)
    PFD = pyeeg.pfd(mat)
    sleep(0.01)

    return (DFA, HFD, SVD_Entropy, Fisher_Information, PFD)

# Create features for each class
def create_features(mat, label):
    f1 = np.zeros((100, 1))
    f2 = np.zeros((100, 1))
    f3 = np.zeros((100, 1))
    f4 = np.zeros((100, 1))
    f5 = np.zeros((100, 1))
    cl = np.full((100, 1), label)

    for i in range(100):
        [f1[i, 0], f2[i, 0], f3[i, 0], f4[i, 0], f5[i, 0]] = features(mat[:, i])
    
    return np.concatenate([f1, f2, f3, f4, f5, cl], axis=1)

MftB = create_features(matB, 1)    # Class 1
MftC = create_features(matC, 0)    # Class 0
MftE = create_features(matE, -1)    # Class -1

# Creating DataFrames
FCM_B = pd.DataFrame(MftB, columns=['f1', 'f2', 'f3', 'f4', 'f5', 'class'])
FCM_C = pd.DataFrame(MftC, columns=['f1', 'f2', 'f3', 'f4', 'f5', 'class'])
FCM_E = pd.DataFrame(MftE, columns=['f1', 'f2', 'f3', 'f4', 'f5', 'class'])

FCM_B.to_csv('FCM_B.csv', index=False)
FCM_C.to_csv('FCM_C.csv', index=False)
FCM_E.to_csv('FCM_E.csv', index=False)

c = FCM_B.head(4)
print(c)

TotalDataset = pd.concat([FCM_B, FCM_C, FCM_E], ignore_index=True)
visDat = TotalDataset.copy(deep=True)
visDat['class'] = visDat['class'].map({1: 'healthy', 0: 'transition', -1: 'seizure'})
d = visDat.head(5)
print(d)

sbn.set(style="whitegrid", palette="muted")
sbn.pairplot(visDat, hue='class', palette="husl")
plt.savefig("fig2.png")

plt.plot(visDat['f1'], '--o')

# Splitting the dataset
X = TotalDataset[['f1', 'f2', 'f3', 'f4', 'f5']]
y = TotalDataset[['class']]
X = np.asarray(X)
y = np.asarray(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)

# Classifiers
names = ["Linear SVM"]
classifiers = [SVC()]
clf_score = []

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for name, clf in zip(names, classifiers):
        clf.fit(X_train, y_train.ravel())
        score = clf.score(X_test, y_test)
        clf_score.append([score, name])

acc = clf_score
print(acc)

# Save the model
dump(clf, "new_model.joblib")
print("Model saved as new_model.joblib")
