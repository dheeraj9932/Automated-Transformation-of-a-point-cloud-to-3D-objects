@echo off

echo "Script running..."

set ImportFilePath1="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\tv_0.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\tv_1.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\tv_2.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\chair_3.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\laptop_4.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\potted_plant_5.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\potted_plant_6.ply"

set ImportFilePath2="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\poisson_reconstruction_wo_objs.ply"

set ExportFilePath="F:\crnt\Development\fraunhofer_project\ANYTHING_PYTHON\pipeline_1\cc_output.ply"

set CloudCompareExe="%ProgramFiles%\CloudCompare\CloudCompare.exe"

%CloudCompareExe% -AUTO_SAVE OFF -O tv_0.ply -O tv_1.ply -O tv_2.ply -O chair_3.ply -O laptop_4.ply -O potted_plant_5.ply -O potted_plant_6.ply -O poisson_reconstruction_wo_objs.ply  -MERGE_MESHES -M_EXPORT_FMT PLY  -PLY_EXPORT_FMT ASCII -SAVE_MESHES FILE "C:\Users\Dheeraj\Desktop\output_8th_apr.ply"

echo "Script complete."
