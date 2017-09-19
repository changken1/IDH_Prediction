import os
import nibabel as nib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

#Load a spreadsheet with patient ID in the first column, IDH status in the second column, and age in the third column
xl = pd.ExcelFile('/home/spreadsheet.xlsx')
df = np.asarray(xl.parse("Sheet1"))
patient_IDH=df[:,[0,2]]
patient_age=df[:,[0,1]]

basedir = '/home/patients/'
os.chdir(basedir)
patients=next(os.walk('.'))[1]

desired_size=[142,142]

slices_FLAIR = np.empty([len(patients)*3, desired_size[0], desired_size[1], 3])
slices_T2 = np.empty([len(patients)*3, desired_size[0], desired_size[1], 3])
slices_T1 = np.empty([len(patients)*3, desired_size[0], desired_size[1], 3])
slices_T1post = np.empty([len(patients)*3, desired_size[0], desired_size[1], 3])
labels = np.empty(len(patients)*3)
age = np.empty(len(patients)*3)
        
def zoompad(array, desired_size):
    array = cv2.resize(array,(desired_size[0],desired_size[1]))
    return array

for p in range(len(patients)):
    
    print(p, patients[p])
    patient_dir = basedir + patients[p] + '/'
    
    idx_idh=np.asarray(np.where((patient_IDH[:,0].astype(str))==str(patients[p])))
    curr_idh = patient_IDH[idx_idh,1]
    idx_age=np.asarray(np.where((patient_age[:,0].astype(str))==str(patients[p])))
    curr_age = patient_age[idx_age,1]
    
    os.chdir(patient_dir)
    FLAIR = np.load('FLAIR_normssn4.npy')
    T2 = np.load('T2_normssn4.npy')
    T1 = np.load('T1_normssn4.npy')
    T1post = np.load('T1post_normssn4.npy')
    FLAIRmask = np.round(nib.load('FLAIRmask.nii').get_data()).astype(FLAIR.dtype)
    FLAIR_m= FLAIR
    T2_m= T2
    T1_m= T1
    T1post_m= T1post
    
    #Find the largest, 75th, and 50th percentile slices in each dimension
    x_sum=np.sum(FLAIRmask,axis=(1,2))
    y_sum=np.sum(FLAIRmask,axis=(0,2))
    z_sum=np.sum(FLAIRmask,axis=(0,1))
    xp100=np.percentile(x_sum[np.nonzero(x_sum)],100,interpolation='nearest')
    xp75=np.percentile(x_sum[np.nonzero(x_sum)],75,interpolation='nearest')
    xp50=np.percentile(x_sum[np.nonzero(x_sum)],50,interpolation='nearest')
    yp100=np.percentile(y_sum[np.nonzero(y_sum)],100,interpolation='nearest')
    yp75=np.percentile(y_sum[np.nonzero(y_sum)],75,interpolation='nearest')
    yp50=np.percentile(y_sum[np.nonzero(y_sum)],50,interpolation='nearest')
    zp100=np.percentile(z_sum[np.nonzero(z_sum)],100,interpolation='nearest')
    zp75=np.percentile(z_sum[np.nonzero(z_sum)],75,interpolation='nearest')
    zp50=np.percentile(z_sum[np.nonzero(z_sum)],50,interpolation='nearest')
    
    x_idx = np.argwhere(x_sum==xp100)[0][0]
    y_idx = np.argwhere(y_sum==yp100)[0][0]
    z_idx = np.argwhere(z_sum==zp100)[0][0]
    
    B = np.argwhere(FLAIRmask[x_idx])
    (xstart_x, ystart_x), (xstop_x, ystop_x) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,y_idx])
    (xstart_y, ystart_y), (xstop_y, ystop_y) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,:,z_idx])
    (xstart_z, ystart_z), (xstop_z, ystop_z) = B.min(0), B.max(0) + 1
    
    FLAIR_x1 = zoompad(np.asarray(FLAIR_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    FLAIR_y1 = zoompad(np.asarray(FLAIR_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    FLAIR_z1 = zoompad(np.asarray(FLAIR_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T2_x1 = zoompad(np.asarray(T2_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T2_y1 = zoompad(np.asarray(T2_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T2_z1 = zoompad(np.asarray(T2_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1_x1 = zoompad(np.asarray(T1_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1_y1 = zoompad(np.asarray(T1_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1_z1 = zoompad(np.asarray(T1_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1post_x1 = zoompad(np.asarray(T1post_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1post_y1 = zoompad(np.asarray(T1post_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1post_z1 = zoompad(np.asarray(T1post_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    x_idx = np.argwhere(x_sum==xp75)[0][0]
    y_idx = np.argwhere(y_sum==yp75)[0][0]
    z_idx = np.argwhere(z_sum==zp75)[0][0]
    
    B = np.argwhere(FLAIRmask[x_idx])
    (xstart_x, ystart_x), (xstop_x, ystop_x) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,y_idx])
    (xstart_y, ystart_y), (xstop_y, ystop_y) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,:,z_idx])
    (xstart_z, ystart_z), (xstop_z, ystop_z) = B.min(0), B.max(0) + 1
    
    FLAIR_x2 = zoompad(np.asarray(FLAIR_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    FLAIR_y2 = zoompad(np.asarray(FLAIR_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    FLAIR_z2 = zoompad(np.asarray(FLAIR_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T2_x2 = zoompad(np.asarray(T2_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T2_y2 = zoompad(np.asarray(T2_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T2_z2 = zoompad(np.asarray(T2_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1_x2 = zoompad(np.asarray(T1_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1_y2 = zoompad(np.asarray(T1_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1_z2 = zoompad(np.asarray(T1_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1post_x2 = zoompad(np.asarray(T1post_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1post_y2 = zoompad(np.asarray(T1post_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1post_z2 = zoompad(np.asarray(T1post_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    x_idx = np.argwhere(x_sum==xp50)[0][0]
    y_idx = np.argwhere(y_sum==yp50)[0][0]
    z_idx = np.argwhere(z_sum==zp50)[0][0]
    
    B = np.argwhere(FLAIRmask[x_idx])
    (xstart_x, ystart_x), (xstop_x, ystop_x) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,y_idx])
    (xstart_y, ystart_y), (xstop_y, ystop_y) = B.min(0), B.max(0) + 1     
    B = np.argwhere(FLAIRmask[:,:,z_idx])
    (xstart_z, ystart_z), (xstop_z, ystop_z) = B.min(0), B.max(0) + 1
    
    FLAIR_x3 = zoompad(np.asarray(FLAIR_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    FLAIR_y3 = zoompad(np.asarray(FLAIR_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    FLAIR_z3 = zoompad(np.asarray(FLAIR_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T2_x3 = zoompad(np.asarray(T2_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T2_y3 = zoompad(np.asarray(T2_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T2_z3 = zoompad(np.asarray(T2_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1_x3 = zoompad(np.asarray(T1_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1_y3 = zoompad(np.asarray(T1_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1_z3 = zoompad(np.asarray(T1_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    T1post_x3 = zoompad(np.asarray(T1post_m[x_idx][xstart_x:xstop_x, ystart_x:ystop_x]), desired_size)
    T1post_y3 = zoompad(np.asarray(T1post_m[:,y_idx][xstart_y:xstop_y, ystart_y:ystop_y]), desired_size)
    T1post_z3 = zoompad(np.asarray(T1post_m[:,:,z_idx][xstart_z:xstop_z, ystart_z:ystop_z]), desired_size)
    
    slices_FLAIR[3*p] = np.stack((FLAIR_x1, FLAIR_y2, FLAIR_z3), axis=2)
    slices_FLAIR[3*p+1] = np.stack((FLAIR_x3, FLAIR_y1, FLAIR_z2), axis=2)
    slices_FLAIR[3*p+2] = np.stack((FLAIR_x2, FLAIR_y3, FLAIR_z1), axis=2)
    slices_T2[3*p] = np.stack((T2_x1, T2_y2, T2_z3), axis=2)
    slices_T2[3*p+1] = np.stack((T2_x3, T2_y1, T2_z2), axis=2)
    slices_T2[3*p+2] = np.stack((T2_x2, T2_y3, T2_z1), axis=2)
    slices_T1[3*p] = np.stack((T1_x1, T1_y2, T1_z3), axis=2)
    slices_T1[3*p+1] = np.stack((T1_x3, T1_y1, T1_z2), axis=2)
    slices_T1[3*p+2] = np.stack((T1_x2, T1_y3, T1_z1), axis=2)
    slices_T1post[3*p] = np.stack((T1post_x1, T1post_y2, T1post_z3), axis=2)
    slices_T1post[3*p+1] = np.stack((T1post_x3, T1post_y1, T1post_z2), axis=2)
    slices_T1post[3*p+2] = np.stack((T1post_x2, T1post_y3, T1post_z1), axis=2)    
    labels[3*p:3*p+3] = curr_idh
    
    del FLAIR, T2, T1, T1post, FLAIRmask, curr_idh

#specify save directory
#save all patient data into numpy files
os.chdir('/home/savedirectory')
np.save('slices_FLAIR.npy', slices_FLAIR)
np.save('slices_T2.npy', slices_T2)
np.save('slices_T1.npy', slices_T1)
np.save('slices_T1post.npy', slices_T1post)
np.save('labels.npy',labels)
np.save('age.npy', age)