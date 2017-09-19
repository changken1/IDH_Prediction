import os
import nipype.interfaces.fsl as fsl
from nipype.interfaces.ants import N4BiasFieldCorrection
import multiprocessing
from joblib import Parallel, delayed

basedir = '/home/patients/'
os.chdir(basedir)
patients=next(os.walk('.'))[1]
patients.sort()

def ssn4(p):
    print(p, patients[p])   
    patient_dir = basedir + patients[p] + '/'
    os.chdir(patient_dir)

    #n4 bias correction
    n4 = N4BiasFieldCorrection(output_image= 'FLAIR_n4.nii')
    n4.inputs.input_image = 'FLAIR.nii'
    n4.inputs.n_iterations = [20,20,10,5]
    n4.run()
    n4 = N4BiasFieldCorrection(output_image= 'T2_n4.nii')
    n4.inputs.input_image = 'T2.nii'
    n4.inputs.n_iterations = [20,20,10,5]
    n4.run()
    n4 = N4BiasFieldCorrection(output_image= 'T1_n4.nii')
    n4.inputs.input_image = 'T1.nii'
    n4.inputs.n_iterations = [20,20,10,5]
    n4.run()
    n4 = N4BiasFieldCorrection(output_image= 'T1post_n4.nii')
    n4.inputs.input_image = 'T1post.nii'
    n4.inputs.n_iterations = [20,20,10,5]
    n4.run()

    #skullstripping
    mybet = fsl.BET()
    result = mybet.run(in_file='FLAIR_n4.nii', out_file='FLAIR_ss_n4.nii', frac=0.4, output_type = 'NIFTI')
    result = mybet.run(in_file='T2_n4.nii', out_file='T2_ss_n4.nii', frac=0.3, output_type = 'NIFTI')
    result = mybet.run(in_file='T1_n4.nii', out_file='T1_ss_n4.nii', frac=0.5, output_type = 'NIFTI')
    result = mybet.run(in_file='T1post_n4.nii', out_file='T1post_ss_n4.nii', frac=0.5, output_type = 'NIFTI')

num_cores = multiprocessing.cpu_count()
Parallel(n_jobs=num_cores)(delayed(ssn4)(p) for p in range(len(patients)))