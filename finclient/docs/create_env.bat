@echo off

:: Update Conda
call conda update -n base -c defaults conda -y

:: Clone the virtual environment named py310pip_base and create a virtual environment named finclient
call conda create --name finclient --clone py310pip_base -y

:: Activate the finclient environment
call conda activate finclient

:: Upgrade pip
call pip install --upgrade pip

:: Activate the base environment
call conda activate base

:: Update the finclient environment using py310pip_finclient.yml
call conda env update -n finclient -f py310pip_finclient.yml

:: Display a message when all operations are completed
echo Anaconda configuration is complete.
