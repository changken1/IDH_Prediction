import os
import numpy as np
from keras.models import load_model
#Specify which GPU to be used
os.environ["CUDA_VISIBLE_DEVICES"]="1"

seed = 0

os.chdir('/home/savedirectory')
slices_FLAIR = np.load('slices_FLAIR.npy')
slices_T2 = np.load('slices_T2.npy')
slices_T1 = np.load('slices_T1.npy')
slices_T1post = np.load('slices_T1post.npy')
labels_Test = np.load('labels.npy')
age_Test= np.load('age.npy')

#specify directory where models are saved
os.chdir('/home/modeldirectory')
model_FLAIR = load_model('FLAIR_model.h5')
model_T2 = load_model('T2_model.h5')
model_T1 = load_model('T1_model.h5')
model_T1post = load_model('T1post_model.h5')
from sklearn.externals import joblib
logreg = joblib.load('logreg.pkl')

def get_accuracy(all_gt, all_label):
    return len(np.argwhere(all_gt==all_label))/float(len(all_gt))

def get_sensitivity(all_gt, all_label):
    loc = np.where(all_gt==1)
    return len(np.argwhere(all_gt[loc]==all_label[loc]))/float(len(all_gt[loc]))

def get_specificity(all_gt, all_label):
    loc = np.where(all_gt==0)
    return len(np.argwhere(all_gt[loc]==all_label[loc]))/float(len(all_gt[loc]))

from sklearn.metrics import roc_auc_score
from sklearn import linear_model

def get_auc(y_true,y_pred):
    n_bootstraps = 1000
    bootstrapped_scores = []
    np.random.seed(seed)
    for i in range(n_bootstraps):
        indices = np.random.choice(range(0, len(y_pred)), len(y_pred), replace=True)
        if len(np.unique(y_true[indices])) < 2:
            continue
        score = roc_auc_score(y_true[indices], y_pred[indices])
        bootstrapped_scores.append(score)
    
    sorted_scores = np.array(bootstrapped_scores)
    sorted_scores.sort()
    confidence_lower = sorted_scores[int(0.05 * len(sorted_scores))]
    confidence_upper = sorted_scores[int(0.95 * len(sorted_scores))]
    return roc_auc_score(y_true, y_pred), confidence_lower, confidence_upper

full_pred_FLAIR = model_FLAIR.predict_proba(slices_FLAIR,batch_size=16)
full_pred_T2 = model_T2.predict_proba(slices_T2,batch_size=16)
full_pred_T1 = model_T1.predict_proba(slices_T1,batch_size=16)
full_pred_T1post = model_T1post.predict_proba(slices_T1post,batch_size=16)
all_age = age_Test
all_age = np.expand_dims(all_age,1)
full_pred = np.hstack((full_pred_FLAIR,full_pred_T2,full_pred_T1,full_pred_T1post,all_age))
all_gt= labels_Test
Z = logreg.predict_proba(full_pred)
get_accuracy(all_gt,np.round(Z[:,1]))
get_sensitivity(all_gt,np.round(Z[:,1]))
get_specificity(all_gt,np.round(Z[:,1]))
get_auc(all_gt,Z[:,1])

