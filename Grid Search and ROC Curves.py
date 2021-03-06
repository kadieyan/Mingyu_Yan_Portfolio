# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""1. download the "biddings.csv.zip" data from https://www.kaggle.com/zurfer/rtb and use the first 50,000 data as Dataframe(The entire dataset is too large)."""

#mounting drive
from google.colab import drive
drive.mount('/content/drive')

!ls /content/drive/'My Drive'/'biddings.csv'
#import dataset
df = pd.read_csv("/content/drive/My Drive/biddings.csv")

biddings = df[0:50001]

# biddings.head()
biddings.dropna()

"""2. Standardize all the 88 columns except "convert" (hint:
from sklearn.preprocessing import StandardScaler, RobustScaler)
"""

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler

import matplotlib.pyplot as plt
import seaborn as sns
def plot(data, title):
  f, ax = plt.subplots()
  sns.set_style("dark")
  ax.set(ylabel="frequency")
  ax.set(xlabel="height(blue) / weight(green)")
  ax.set(title=title)
  sns.distplot(data[:, 0:1], color="blue")
  sns.distplot(data[:, 1:2], color="green")
  plt.savefig(title + ".png")
  plt.show()

robust_scaler_data = preprocessing.RobustScaler().fit_transform(biddings.iloc[:,2:4])
standard_scaler_data = preprocessing.StandardScaler().fit_transform(biddings.iloc[:,2:4])
sd_plot = plot(standard_scaler_data, "StandardScaler")
rb_plot = plot(robust_scaler_data, "RobustScaler")

robust_scaler_data = preprocessing.RobustScaler().fit(biddings.iloc[:,0:88])
stdize = robust_scaler_data.transform(biddings.iloc[:,0:88])

biddings_1 = biddings.copy()
stdize_df = pd.DataFrame(stdize)
biddings_1 = pd.concat([stdize_df, biddings_1["convert"]], axis =1)
biddings_1.head()

"""3. Use K-folder Cross Validation to split dataset into 5 folders and print training and testing datasets for each folder"""

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

X = biddings_1.iloc[:,0:88]
y = biddings_1.iloc[:,88]
# X.head()

cv = StratifiedKFold(n_splits=5)
for train_index, test_index in cv.split(X,y):
    print("Train Index: ", train_index, "\n")
    print("Test Index: ", test_index)

"""4. Undersample the data to create a new dataset "new_df" which has equal numbers of the "click" and "not click" data"""

biddings_1 = biddings_1.sample(frac=1)

click_df = biddings_1.loc[biddings_1['convert'] == 1]
not_click_df = biddings_1.loc[biddings_1['convert'] == 0][:92]

normal_distributed_df = pd.concat([click_df, not_click_df])

# Shuffle dataframe rows
new_df = normal_distributed_df.sample(frac=1, random_state=42)

new_df.index = range(0,184)

new_df.shape
new_df[0:10]
# new_df["convert"]

"""5. Use PCA and T-SNE to decrease the dimension of the "new_df" to n=2, and plot the scatter plotting."""

#PCA
from sklearn.decomposition import PCA

pca = PCA(n_components=2, random_state=42)
df_pca = pca.fit_transform(new_df.iloc[:,0:88])

df_pca_1 = pd.concat([pd.DataFrame(df_pca), new_df["convert"]], axis = 1)

plt.scatter(df_pca_1[0][df_pca_1["convert"] == 0], df_pca_1[1][df_pca_1["convert"] == 0], color = "orange", label = "convert = 0")
plt.scatter(df_pca_1[0][df_pca_1["convert"] == 1], df_pca_1[1][df_pca_1["convert"] == 1], color = "red", label = "convert = 1")
plt.ylabel('Convert')
plt.xlabel('Biddings')
plt.title("PCA")
# plt.xlim(-15, 15)
# plt.ylim(-15, 15)

plt.legend(loc=(1, 0))

plt.show()

#T-SEN
from sklearn.manifold import TSNE

tsen = TSNE(n_components=2, init='pca', random_state=42)
df_tsen = tsen.fit_transform(new_df.iloc[:,0:88])

df_tsen_1 = pd.concat([pd.DataFrame(df_tsen), new_df["convert"]], axis =1)

plt.scatter(df_tsen_1[0][df_tsen_1["convert"] == 0], df_tsen_1[1][df_tsen_1["convert"] == 0], color = "orange", label = "convert = 0")
plt.scatter(df_tsen_1[0][df_tsen_1["convert"] == 1], df_tsen_1[1][df_tsen_1["convert"] == 1], color = "red", label = "convert = 1")
plt.ylabel('Convert')
plt.xlabel('Biddings')
plt.title("TSEN")
# plt.xlim(-15, 15)
# plt.ylim(-15, 15)

plt.legend(loc=(1, 0))

plt.show()

"""6. Split "new_df" into train and test datasets(test_size=0.2, random_state=42). Then calculate the cross validation scores for Logistic Regression,SVC, KNeighbors and desicion trees models."""

from sklearn.model_selection import train_test_split

X_cv, y_cv = new_df.iloc[:,0:88], new_df.iloc[:, 88]

X_train, X_test, y_train, y_test =train_test_split(X_cv, y_cv, test_size=0.2, random_state=42, stratify=y_cv)

X_train[0:10]

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

names = ["LogisticRegression", "SVM", "Decision Tree", "Nearest Neighbors"]

classifiers = [
              LogisticRegression(),
               SVC(kernel="linear", C=1, probability = True),
               DecisionTreeClassifier(max_depth=5),
               KNeighborsClassifier(5)
     ]

for name, clf in zip(names, classifiers):
  clf.fit(X_train, y_train)
  score = clf.score(X_test, y_test)
  print(name, score)

from sklearn.model_selection import cross_val_score

for name, clf in zip(names, classifiers):
  scores = cross_val_score(clf, new_df.iloc[:,0:88], new_df.iloc[:, 88], cv=5)
  print(name, scores)

"""7. Use GridSearch to find the best parameters for the four models, recalculate the cross validation scores and plot ROC curves."""

from sklearn.model_selection import GridSearchCV

#FOR LOGISTIC
penalty = ['l1', 'l2']
C = np.logspace(0, 4, 10)


#FOR SVC
param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

#FOR DECISION TREE
sample_split_range = list(range(1, 50, 1))
max_depth = list(range(1,4,1))

param_grid = [
              {"penalty": penalty, "C": C},
{'C': param_range, 'gamma': param_range, 'kernel': ['linear', 'rbf']},          
{"max_depth": max_depth, "min_samples_split": sample_split_range},
{"n_neighbors": [3,5,11,19], "weights": ["uniform", "distance"], "metric": ["euclidean", "manhattan"]}]

a = []

for name, clf, paramater in zip(names, classifiers, param_grid):
  gs = GridSearchCV(estimator=clf, param_grid=paramater, cv=10, refit=True, n_jobs=-1)
  gs = gs.fit(X_train, y_train)
  print(name, gs.best_score_)
  print(name, gs.best_params_)
  scores = cross_val_score(clf, new_df.iloc[:,0:88], new_df.iloc[:, 88], cv=5)
  print(name, "Cross Validation Scores:", scores)
  a.append(gs.best_estimator_)

from sklearn.model_selection import cross_val_predict

log_reg_pred = cross_val_predict(a[0], X_cv, y_cv, cv=5,
                             method="decision_function")

svc_pred = cross_val_predict(a[1], X_cv, y_cv, cv=5,
                             method="decision_function")

knears_pred = cross_val_predict(a[2], X_cv, y_cv, cv=5)

tree_pred = cross_val_predict(a[3], X_cv, y_cv, cv=5)

from sklearn.metrics import roc_auc_score

print('Logistic Regression: ', roc_auc_score(y_cv, log_reg_pred))
print('KNears Neighbors: ', roc_auc_score(y_cv, knears_pred))
print('Support Vector Classifier: ', roc_auc_score(y_cv, svc_pred))
print('Decision Tree Classifier: ', roc_auc_score(y_cv, tree_pred))

from sklearn.metrics import roc_curve, auc
log_fpr, log_tpr, log_thresold = roc_curve(y_cv, log_reg_pred)
knear_fpr, knear_tpr, knear_threshold = roc_curve(y_cv, knears_pred)
svc_fpr, svc_tpr, svc_threshold = roc_curve(y_cv, svc_pred)
tree_fpr, tree_tpr, tree_threshold = roc_curve(y_cv, tree_pred)


def graph_roc_curve_multiple(log_fpr, log_tpr, knear_fpr, knear_tpr, svc_fpr, svc_tpr, tree_fpr, tree_tpr):
    plt.figure(figsize=(16,8))
    plt.title('ROC Curve \n Top 4 Classifiers', fontsize=18)
    plt.plot(log_fpr, log_tpr, label='Logistic Regression Classifier Score: {:.4f}'.format(roc_auc_score(y_cv, log_reg_pred)))
    plt.plot(knear_fpr, knear_tpr, label='KNears Neighbors Classifier Score: {:.4f}'.format(roc_auc_score(y_cv, knears_pred)))
    plt.plot(svc_fpr, svc_tpr, label='Support Vector Classifier Score: {:.4f}'.format(roc_auc_score(y_cv, svc_pred)))
    plt.plot(tree_fpr, tree_tpr, label='Decision Tree Classifier Score: {:.4f}'.format(roc_auc_score(y_cv, tree_pred)))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([-0.01, 1, 0, 1])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    plt.annotate('Minimum ROC Score of 50% \n (This is the minimum score to get)', xy=(0.5, 0.5), xytext=(0.6, 0.3),
                arrowprops=dict(facecolor='#6E726D', shrink=0.05),
                )
    plt.legend()
    
graph_roc_curve_multiple(log_fpr, log_tpr, knear_fpr, knear_tpr, svc_fpr, svc_tpr, tree_fpr, tree_tpr)
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# ROC Curves - LogisticRegression
from scipy import interp
from sklearn.pipeline import make_pipeline

pipe_lr = make_pipeline(PCA(n_components=2),
                        LogisticRegression(penalty='l1', 
                                           random_state=0,
                                           solver='liblinear',
                                           C=21.544346900318832))
X_cv_nd = X_cv.values

cv_lst = list(StratifiedKFold(n_splits=3).split(X_cv_nd, y_cv))

fig = plt.figure(figsize=(7, 5))

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv_lst):
    probas = pipe_lr.fit(X_cv_nd[train], y_cv[train]).predict_proba(X_cv_nd[test])

    fpr, tpr, thresholds = roc_curve(y_cv[test], probas[:, 1], pos_label=1)
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,
             tpr,
             label='ROC fold %d (area = %0.2f)'
#                    % (i+1, roc_auc))

plt.plot([0, 1],
         [0, 1],
         linestyle='--',
         color=(0.6, 0.6, 0.6),
         label='Random guessing')

mean_tpr /= len(cv_lst)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
plt.plot([0, 0, 1],
         [0, 1, 1],
         linestyle=':',
         color='black',
         label='Perfect performance')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend(loc="lower right")

plt.tight_layout()
# plt.savefig('images/06_10.png', dpi=300)
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# ROC Curves - SVM
pipe_lr = make_pipeline(PCA(n_components=2),
                        SVC(kernel="linear", C=0.01, gamma=0.0001, probability = True))
X_cv_nd = X_cv.values

cv_lst = list(StratifiedKFold(n_splits=3).split(X_cv_nd, y_cv))

fig = plt.figure(figsize=(7, 5))

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv_lst):
    probas = pipe_lr.fit(X_cv_nd[train], y_cv[train]).predict_proba(X_cv_nd[test])

    fpr, tpr, thresholds = roc_curve(y_cv[test], probas[:, 1], pos_label=1)
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,
             tpr,
             label='ROC fold %d (area = %0.2f)'
#                    % (i+1, roc_auc))

plt.plot([0, 1],
         [0, 1],
         linestyle='--',
         color=(0.6, 0.6, 0.6),
         label='Random guessing')

mean_tpr /= len(cv_lst)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
plt.plot([0, 0, 1],
         [0, 1, 1],
         linestyle=':',
         color='black',
         label='Perfect performance')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend(loc="lower right")

plt.tight_layout()
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# ROC Curves - Decision Tree
pipe_lr = make_pipeline(PCA(n_components=2),
                        DecisionTreeClassifier(max_depth=4, min_samples_split=41))
X_cv_nd = X_cv.values

cv_lst = list(StratifiedKFold(n_splits=3).split(X_cv_nd, y_cv))

fig = plt.figure(figsize=(7, 5))

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv_lst):
    probas = pipe_lr.fit(X_cv_nd[train], y_cv[train]).predict_proba(X_cv_nd[test])

    fpr, tpr, thresholds = roc_curve(y_cv[test], probas[:, 1], pos_label=1)
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,
             tpr,
             label='ROC fold %d (area = %0.2f)'
#                    % (i+1, roc_auc))

plt.plot([0, 1],
         [0, 1],
         linestyle='--',
         color=(0.6, 0.6, 0.6),
         label='Random guessing')

mean_tpr /= len(cv_lst)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
plt.plot([0, 0, 1],
         [0, 1, 1],
         linestyle=':',
         color='black',
         label='Perfect performance')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend(loc="lower right")

plt.tight_layout()
# plt.savefig('images/06_10.png', dpi=300)
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# ROC Curves - Nearest Neighbors
pipe_lr = make_pipeline(PCA(n_components=2),
                        KNeighborsClassifier(n_neighbors = 3, weights = "uniform", metric = "manhattan"))
X_cv_nd = X_cv.values

cv_lst = list(StratifiedKFold(n_splits=3).split(X_cv_nd, y_cv))

fig = plt.figure(figsize=(7, 5))

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv_lst):
    probas = pipe_lr.fit(X_cv_nd[train], y_cv[train]).predict_proba(X_cv_nd[test])

    fpr, tpr, thresholds = roc_curve(y_cv[test], probas[:, 1], pos_label=1)
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,
             tpr,
             label='ROC fold %d (area = %0.2f)'
#                    % (i+1, roc_auc))

plt.plot([0, 1],
         [0, 1],
         linestyle='--',
         color=(0.6, 0.6, 0.6),
         label='Random guessing')

mean_tpr /= len(cv_lst)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
plt.plot([0, 0, 1],
         [0, 1, 1],
         linestyle=':',
         color='black',
         label='Perfect performance')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend(loc="lower right")

plt.tight_layout()
# plt.savefig('images/06_10.png', dpi=300)
plt.show()

"""Confusion matixes"""

from collections import Counter
from sklearn.metrics import confusion_matrix
import random

X_raw_train, X_raw_test, y_raw_train, y_raw_test =train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

RBF_SVM = SVC(kernel="linear", C=0.01, gamma=0.0001, probability = True)
svc_fit = RBF_SVM.fit(X_raw_train, y_raw_train)
y_raw_pred = RBF_SVM.predict(X_raw_test)

conf_under = confusion_matrix(y_true=y_raw_test, y_pred=y_raw_pred)
print('Confusion matrix:\n', conf_under)
