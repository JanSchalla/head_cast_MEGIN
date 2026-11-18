Head Cast proceedure (AG Florin, University Clinic Duesseldorf)

In the following the proceedure used to create head casts for the Triux MEG system used by AG Florin is described.

1. Get MRI (T1w or T2w). Can be Dicom (should be around ~180 files) or nifti. If you have multiple on a disc/drive you can use the script "check_all_dicom.m" to extrct the Sequence used and nr. of files to select the correct one. 
2. Insert path to dicom or nifti into "do_make_headcasts_due.m" (adjust other pathes accordingly) and run the script step by step. Only the "ft_volumerealign" needs manual input, where you specify Nasion, LPA & RPA. In out experience, this does not need to be very accurate, it just helps fieldtrip to find the right orientation. If you flip LPA and RPA, then the model will later be turned "inside out" -> Fix for that in the Workflow (see below). Rest of the script, gives you some quality checks and at the end it exports a .stl file. 
3. Load .stl file into meshmixer and process accordingly as described in HeadCast_Workflow_AGFlorin.pdf. 
3.1. Some extra notes on the workflow: Step 4: The example head is a loose orientation, also the support structures can be moved accordingly to suit the needs best -> just to use it as a first orientation. Step 6: In our clinical MRIs the heads were cut below the nose. This makes the later print more difficult, thus we decided to take the neck from the example head and adjust it to fit the participants head as best as possible (reduce the overhangs in the model as good as possible, but some are ok, the printer can handle them mostly). Step 7: Make sure the "earcanals" are completely inside the head surface at the edges, otherwise you will get small pockets, where the foam will be annoying.
4. Prepare 3D Print using slicer (Cura). These settings are specific to the 3D printer we use (Creality K1Max) may need to be tested with your settings. We recommend some test prints, to check the "performance of your printer (e. g. create a 10x10mm cube, print it and check the dimesnions, as well if the edges bulge, also this one [https://www.thingiverse.com/thing:2656594] is good to test your overhangs). 
4.1. We do not need support, normally the 3D printers are able to print some overhangs. 
5. For creating the head casts, some example pictures are attached. The printed head needs to be pushed down, otherwise the foam will push it back up! Stones & clamps on the sides are not necessary, this was one of our first testings ;), the clamps pushing down are enough. Otherwise follow the "Molding_workflow_AG_Florin.pdf".

To create the mold:
We used the .step file to create the mold. 
triux_extended_00mm.mix: Meshmixer file of triux model loaded in combined with a meshmixer model to make solid.
triux_solid_mold_0mm.mix: Raw mold -> would still need to be cut in half and support structures (like feet, screw holes and so on) need to be inserted)
triux_solid_mold_0.25mmE.mix: Same as above but enlarges by 0.25mm -> making the head casts tighter inside the MEG and allowing for less movement (BUT also making the process of getting in and out more difficult).
left / right_triux_mold_0.25mmE.mix: Left and right side of the modl respectively, with all support structures we used (basically ready for printing). 

For the print settings we used really thick walls 10-15mm (Infill of about 30%) and a not so fast print speed to assure a good quality. Took days and ~3kg of filament to print each half. These we also printed with supports (!) to stabilise the print (but the inside was facing up, so there no support was generated!).

To verify movement params:
Measure with cHPI activated. We adapted our cHPI Frequencies to >900 Hz and used a sampling rate of 5000 Hz to be sure not to hide real brain signals by the cHPI frequencies. 
To extract movement from the HPI's you need MNE. The scripts supplied can help, but the most important functions are "mne.chpi.amplitude", mne.chpi.compute_chpi_loc" (here you get the raw movements for each coil -> output is a dictionary where the 'rrs' subfield contains the coordinates for each timepoint), "mne.chpi.compute_head_pos" (calculated the position of the head center).
To check the accuracy of ending up in the same position on a second session, you can extract the HPI locations at the beginning from the measuremnt by loading the metadata and extract the coordinate for each coil.
