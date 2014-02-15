#!/bin/bash
export txt1="start_freesurfer processing at `date +%H:%M:%S`" 
export txt2="Done!"
./pid.sh "$3" &
#./backend.sh "$1" $2 "$3" &
export SUBJECTS_DIR="$1" export FREESURFER_HOME=/opt/freesurfer && source $FREESURFER_HOME/SetUpFreeSurfer.sh && echo $txt1 > "$3" && recon-all -i $2 -s patient && recon-all -all -s patient && echo $txt2 >>"$3"

