rem execute experiment.

@echo off
cd /d %~dp0

rem inform slack
python src/postToSlack.py "experiment start"

rem execute python script
python src/main.py

rem inform slack
python src/postToSlack.py "experiment end"

rem execute matlab script
rem matlab -nosplash -nodesktop -r "/src_m/estimate_TM;exit"