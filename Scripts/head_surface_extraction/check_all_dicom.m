%% Dicom to Nifti import with SPM% Script collects DICOM images from participant folders and converts the

% Import SPM
addpath('/home/jan/Jan/998_toolboxes/lameg_SPM/spm12')

% Folder with dicoms
folders_dir = '/media/jan/2026-05-04-11-28-12-00/dicom/00008b78/aa07fbf3/aa2e55ba/';
dicom_folders = dir(folders_dir);
dicom_folders = {dicom_folders.name};


for iFolder = 1:length(dicom_folders)-2

    % Dicom Folder
    dicom_folder = fullfile(folders_dir,dicom_folders{iFolder+2});
    
    % Grab Dicom Files in Folder
    dicom_files = dir(dicom_folder);
    dicom_files = {dicom_files.name};
    
    P = [];
    for K = 1:length(dicom_files)-2
        P{K} = fullfile(dicom_folder,dicom_files{K + 2});
    end
    
    % Load Dicom Head Information
    hdr = spm_dicom_headers(P);
    
    % Printd
    display('---')
    display(['Folder No: ',num2str(iFolder)])
    display(['Folder Name: ',dicom_folders{iFolder+2}])
    display(['Dicom Count: ',num2str(length(dicom_files))])
    display(hdr{1,1}.SeriesDescription)
    display(['---'])

end
