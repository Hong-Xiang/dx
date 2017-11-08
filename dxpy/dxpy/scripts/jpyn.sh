#/usr/bin/env zsh
echo 'Starting Jupyter Notebook Server...'
cwd=`pwd`
cd ~/Workspace/jpyn
echo `pwd`
nohup jupyter notebook &
echo 'Done'
cd $cwd
