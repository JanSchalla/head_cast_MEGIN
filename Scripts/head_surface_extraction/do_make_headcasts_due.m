%% Fieldtrip Version 20221223 is working -> more recent not tested
%% Vis of MRI works with matlab 2022b -> with newer version the crosshair does not move
%% Get Started
restoredefaultpath
% Clean Workspace
close all
clear all
clc
% Add Fieldtrip Path
addpath('/home/jan/Jan/998_toolboxes/fieldtrip/fieldtrip-20221223/');
ft_defaults

%% Set Paths and Dirs
% If true creates (from L29 onward) different subfolders
study = false;

% Subject ID (used for generating pathes)
ID = 'HCSFB001';

% Path to one specific dicom file (fildtrip grabs the rest automatically)
% or a nifti
mri_file = '/home/jan/Jan/00_Retune/00_Head_Casts/01_DICOM_data/YW/matcomr016_t1_mpr_sag_07x07x07_13.nii';
% Path to save the .stl at the end
outdir = fullfile('/home/jan/Jan/00_Retune/00_Head_Casts/02_MRI_surface_extraction/', ID);

% path to create subfolders for the later process
project_dir = '/home/jan/Jan/00_Retune/04_HC/';

%% Optional
if study
    % Create BackUp Folder for modeling
    if not(isfolder(fullfile('/home/jan/Jan/00_Retune/00_Head_Casts/03_Meshmixer_Template/BackUpSaves/', ID)))
        mkdir(strcat('/home/jan/Jan/00_Retune/00_Head_Casts/03_Meshmixer_Template/BackUpSaves/', ID))
    end
    
    % Create Final Model folder
    if not(isfolder(fullfile('/home/jan/Jan/00_Retune/00_Head_Casts/04_Head_Surface_Models/', ID)))
        mkdir(fullfile('/home/jan/Jan/00_Retune/00_Head_Casts/04_Head_Surface_Models/', ID))
    end

    % Create Subejct folder
    if not(isfolder(fullfile(project_dir, ID)))
        mkdir(fullfile(project_dir, ID))
    end
    
    % Create Subejct-sub folder
    if not(isfolder(fullfile(project_dir, ID, '/anat')))
        mkdir(fullfile(project_dir, ID, '/anat'))
        
    end
    
    if not(isfolder(fullfile(project_dir, ID, '/LFP')))
        mkdir(fullfile(project_dir, ID, '/LFP'))
    end
    
    if not(isfolder(fullfile(project_dir, ID, '/eyetracker')))
        mkdir(fullfile(project_dir, ID, '/eyetracker'))
    end
    
    if not(isfolder(fullfile(project_dir, ID, '/meg')))
        mkdir(fullfile(project_dir, ID, '/meg'))
    end
    
    if not(isfolder(fullfile(project_dir, ID, '/UPDRS')))
        mkdir(fullfile(project_dir, ID, '/UPDRS'))
    end

    if not(isfolder(fullfile(project_dir, ID, '/beh')))
        mkdir(fullfile(project_dir, ID, '/beh'))
    end
end

%% First phase: construct scalp surface from MRI
% - importing the DICOM images
% Load Nifti with Fieldtrip
mri_orig = ft_read_mri(mri_file);

% Create folder along the workflow, so you don´t have to
if not(isfolder(outdir))
    mkdir(outdir)
end
%% Set landmarks in MRI

% Set RPA, LPA, and Nasion in MRI scan.
% HERE AN INTERACTION IS REQUIRED IN FT_VOLUMEREALIGN

cfg = [];
cfg.coordsys = 'neuromag';
mri_coreg = ft_volumerealign(cfg, mri_orig);

% Here you should check that the axes are pointing in the correct direction according to the CTF coordinate system with
% +x to the right,
% +y to the nose (where the vitamine E capsure is located),
% -y to the back.
% +z to the top.

%ft_determine_coordsys(mri_coreg, 'interactive', false);

%% - segment the scalp surface

cfg = [];
cfg.output = 'scalp';
cfg.spmversion = 'spm12';
cfg.spmmethod = 'new';
% cfg.scalpsmooth = 'no';     % Added by MY
cfg.scalpthreshold = 0.1;   % Added by MY
seg_coreg = ft_volumesegment(cfg, mri_coreg);

% fill the ears
before = sum(seg_coreg.scalp(:)) * abs(det(seg_coreg.transform(1:3,1:3)));
seg_coreg.scalp = imclose(seg_coreg.scalp, strel('sphere',6));
after = sum(seg_coreg.scalp(:)) * abs(det(seg_coreg.transform(1:3,1:3)));
fprintf('added %d ml around the ears\n', round((after-before)/1000));

% Visualise head mask
cfg = [];
cfg.funparameter = 'scalp';
cfg.location = 'center';
ft_sourceplot(cfg, seg_coreg, mri_coreg);

%% - construct the scalp surface

cfg = [];
cfg.method = 'isosurface';
cfg.numvertices = []; % do not retriangulate to a lower number of vertices
scalp_coreg = ft_prepare_mesh(cfg, seg_coreg);

figure
ft_plot_mesh(scalp_coreg);
ft_plot_axes(scalp_coreg);
camlight

%% Save Surface as STL
ft_write_headshape(fullfile(outdir,'/scalp_coreg_t1.stl'), scalp_coreg, 'format', 'stl');
