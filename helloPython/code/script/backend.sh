#!/bin/bash
export SUBJECTS_DIR="$1" export FREESURFER_HOME=/opt/freesurfer && source $FREESURFER_HOME/SetUpFreeSurfer.sh && echo $txt1 > "$3" && recon-all -i $2 -s patient && recon-all -all -s patient && echo $txt2 >>"$3"
