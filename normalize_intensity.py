import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_dilation, binary_erosion
from copy import deepcopy
from nipy import labs
import multiprocessing
from joblib import Parallel, delayed
from scipy.stats import iqr

basedir = '/home/patients/'
os.chdir(basedir)
patients=next(os.walk('.'))[1]

def normalize(p):

    print(p, patients[p])
    patient_dir = basedir + patients[p] + '/'
    os.chdir(patient_dir)

    FLAIR = np.round(nib.load('FLAIR_n4.nii').get_data())
    T2 = np.round(nib.load('T2_n4.nii').get_data())
    T1 = np.round(nib.load('T1_n4.nii').get_data())
    T1post = np.round(nib.load('T1post_n4.nii').get_data())
    FLAIR_ss = np.round(nib.load('FLAIR_ss_n4.nii').get_data())
    T2_ss = np.round(nib.load('T2_ss_n4.nii').get_data())
    T1_ss = np.round(nib.load('T1_ss_n4.nii').get_data())
    T1post_ss = np.round(nib.load('T1post_ss_n4.nii').get_data())
    FLAIRmask = np.round(nib.load('FLAIRmask.nii').get_data())
    
    #normalize image intensity values relative to normal brain
    idx_mask = np.where(FLAIRmask==0)
    idx_nz = np.nonzero(FLAIR_ss[idx_mask])
    median = np.median(FLAIR_ss[idx_mask][idx_nz])
    curr_iqr = iqr(FLAIR_ss[idx_mask][idx_nz])
    FLAIR_normssn4 = deepcopy(FLAIR_ss)
    FLAIR_normssn4[np.nonzero(FLAIR_ss)] = (FLAIR_normssn4[np.nonzero(FLAIR_ss)]-median)/curr_iqr
    idx_nz = np.nonzero(T2_ss[idx_mask])
    median = np.median(T2_ss[idx_mask][idx_nz])
    curr_iqr = iqr(T2_ss[idx_mask][idx_nz])
    T2_normssn4 = deepcopy(T2_ss)
    T2_normssn4[np.nonzero(T2_ss)] = (T2_normssn4[np.nonzero(T2_ss)]-median)/curr_iqr
    idx_nz = np.nonzero(T1_ss[idx_mask])
    median = np.median(T1_ss[idx_mask][idx_nz])
    curr_iqr = iqr(T1_ss[idx_mask][idx_nz])
    T1_normssn4 = deepcopy(T1_ss)
    T1_normssn4[np.nonzero(T1_ss)] = (T1_normssn4[np.nonzero(T1_ss)]-median)/curr_iqr   
    idx_nz = np.nonzero(T1post_ss[idx_mask])
    median = np.median(T1post_ss[idx_mask][idx_nz])
    curr_iqr = iqr(T1post_ss[idx_mask][idx_nz])
    T1post_normssn4 = deepcopy(T1post_ss)
    T1post_normssn4[np.nonzero(T1post_ss)] = (T1post_normssn4[np.nonzero(T1post_ss)]-median)/curr_iqr              
                
    os.chdir(patient_dir)
    np.save('FLAIR_normssn4.npy',FLAIR_normssn4)
    np.save('T2_normssn4.npy',T2_normssn4)
    np.save('T1_normssn4.npy',T1_normssn4)
    np.save('T1post_normssn4.npy',T1post_normssn4)
    FLAIRmask_final = nib.Nifti1Image(FLAIRmask, np.eye(4))
    nib.save(FLAIRmask_final, os.path.join(patient_dir,'FLAIRmask_final.nii.gz'))

num_cores = multiprocessing.cpu_count()
Parallel(n_jobs=num_cores)(delayed(normalize)(p) for p in range(len(patients)))