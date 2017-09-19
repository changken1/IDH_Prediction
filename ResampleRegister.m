%Add MatlabScripts Folder to Path
addpath(genpath('/home/MatlabScripts'))

%Specify Patient Directory
%Patient directory should be organized with a folder for each patient.
%Within each patient folder, there should be a folder for each MR modality
%with its respective dicom: FLAIR, T2, T1, T1post. In addition, there
%should be a nrrd file with the tumor segmentation mask named
%FLAIRmask.nrrd
patientdir='/home/Patients/';
cd(patientdir)
patients=dir;
patients=patients(3:end);

for i = 1:length(patients)
    
    basedir=strcat(patientdir,patients(i).name)
    cd(basedir)
    
    FLAIRmask = nrrdread('FLAIRmask.nrrd');
    cd(strcat(basedir,'/FLAIR'))
    firstimagename=dir;
    firstimagename=firstimagename(3).name;
    [sData] = readDICOMdir(pwd,0);
    FLAIR = sData{2}.scan.volume;
    info = dicominfo(firstimagename);
    x_FLAIR = info.PixelSpacing(1);
    y_FLAIR = info.PixelSpacing(2);
    z_FLAIR = info.SliceThickness(1);
    FLAIR = imresize3D(FLAIR,[],[round(double(size(FLAIR,1))*x_FLAIR),...
        round(double(size(FLAIR,2))*y_FLAIR),round(double(size(FLAIR,3))*z_FLAIR)],'cubic','fill');
    FLAIRmask = imresize3D(FLAIRmask,[],[round(double(size(FLAIRmask,1))*x_FLAIR),...
        round(double(size(FLAIRmask,2))*y_FLAIR),round(double(size(FLAIRmask,3))*z_FLAIR)],'cubic','fill');
    
    cd(strcat(basedir,'/T2'))
    [sData] = readDICOMdir(pwd,0);
    T2 = sData{2}.scan.volume;
    firstimagename=dir;
    firstimagename=firstimagename(3).name;
    info = dicominfo(firstimagename);
    x_T2 = info.PixelSpacing(1);
    y_T2 = info.PixelSpacing(2);
    z_T2 = info.SliceThickness(1);
    T2 = imresize3D(T2,[],[round(double(size(T2,1))*x_T2),...
        round(double(size(T2,2))*y_T2),round(double(size(T2,3))*z_T2)],'cubic','fill');
    
    cd(strcat(basedir,'/T1'))
    [sData] = readDICOMdir(pwd,0);
    T1 = sData{2}.scan.volume;
    firstimagename=dir;
    firstimagename=firstimagename(3).name;
    info = dicominfo(firstimagename);
    x_T1 = info.PixelSpacing(1);
    y_T1 = info.PixelSpacing(2);
    z_T1 = info.SliceThickness(1);
    T1 = imresize3D(T1,[],[round(double(size(T1,1))*x_T1),...
        round(double(size(T1,2))*y_T1),round(double(size(T1,3))*z_T1)],'cubic','fill');
    
    cd(strcat(basedir,'/T1post'))
    [sData] = readDICOMdir(pwd,0);
    T1post = sData{2}.scan.volume;
    firstimagename=dir;
    firstimagename=firstimagename(3).name;
    info = dicominfo(firstimagename);
    x_T1post = info.PixelSpacing(1);
    y_T1post = info.PixelSpacing(2);
    z_T1post = info.SliceThickness(1);
    T1post = imresize3D(T1post,[],[round(double(size(T1post,1))*x_T1post),...
        round(double(size(T1post,2))*y_T1post),round(double(size(T1post,3))*z_T1post)],'cubic','fill');
    
    %Register images to T1post
    [optimizer,metric] = imregconfig('multimodal');
    Rfixed  = imref3d(size(T1post),1,1,1);
    optimizer.InitialRadius = optimizer.InitialRadius/100000;
    
    Rmoving = imref3d(size(FLAIR),1,1,1);
    tform1 = imregtform(FLAIR,Rmoving,T1post,Rfixed,'similarity',optimizer,metric);
    FLAIR_reg = imwarp(FLAIR,tform1,'cubic','OutputView',Rfixed);
    FLAIRmask_reg = round(imwarp(FLAIRmask,tform1,'cubic','OutputView',Rfixed));
    
    Rmoving = imref3d(size(T1),1,1,1);
    tform2 = imregtform(T1,Rmoving,T1post,Rfixed,'similarity',optimizer,metric);
    T1_reg = imwarp(T1,tform2,'cubic','OutputView',Rfixed);
    
    Rmoving = imref3d(size(T2),1,1,1);
    tform3 = imregtform(T2,Rmoving,T1post,Rfixed,'similarity',optimizer,metric);
    T2_reg = imwarp(T2,tform3,'cubic','OutputView',Rfixed);
    
    cd(basedir)
    %Save registered and resampled MR images and mask in nifti format
    FLAIR_nii = make_nii(FLAIR_reg);
    save_nii(FLAIR_nii, 'FLAIR.nii')
    T2_nii = make_nii(T2_reg);
    save_nii(T2_nii, 'T2.nii')
    T1post_nii = make_nii(T1post);
    save_nii(T1post_nii, 'T1post.nii')
    T1_nii = make_nii(T1_reg);
    save_nii(T1_nii, 'T1.nii')
    FLAIRmask_nii = make_nii(FLAIRmask_reg);
    save_nii(FLAIRmask_nii, 'FLAIRmask.nii')
    
end

