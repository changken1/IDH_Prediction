# IDH_Prediction
Use of Deep Learning to Predict IDH status of gliomas from MR Imaging

This is a repository for pre-processing of MR images of gliomas.
The input data is assumed to be 4 modality MR imaging (T2 FLAIR, T2, T1 pre-contrast, T1 post-contrast) in dicom format.

The order in which the scripts should be run are
1) ResampleRegister.m - Registration and isotropic resampling
2) n4_skullstrip.py - n4 bias correction and skullstripping
3) normalize_intensity.py - Normalize image intensity by subtracting median and dividing by interquartile range of normal brain
4) compile_patientsamples.py - Extract patient image samples, age, and idh status and compile them into numpy files.
5) predict.py - Predict IDH status using modality network models, combining outputs with age in a logistic regression

Step 1) is a MATLAB script while the others are python scripts. Step 5) is written in Keras (version 1.2.0) with TensorFlow backend. 
The trained models can be downloaded here:
https://www.dropbox.com/sh/enfdwh8qh8x5yro/AADtOMbUqfmUtEGA9SDBwGeja?dl=0
