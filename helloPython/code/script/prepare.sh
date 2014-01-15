#!/bin/bash
export txt1="start_freesurfer processing at `date '+%Y-%m-%d %H:%M:%S'`"
export txt4='D197'
export txt2="Done!"

echo $1
echo $2
echo $3
echo $txt1 >> $3 && echo $txt4 >> $3 && echo $txt2 >> $3


