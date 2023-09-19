# 1. Guidelines for Creating Anaconda Virtual Environments
## 1. Purpose
- To use an environment compatible with the cover_trader system server
- To use an environment that is compatible with both Windows and Ubuntu

## 2. Principles
- Use conda for creating virtual environments
- Choose one of the following methods:
    - Install packages using conda only
    - Use conda only for installing Python and install all remaining packages using pip

## 3. Creating a Virtual Environment Using Pip
- Requirement to be compatible to fta system
    - pandas==2.0.0
    - pyarrow==9.0.0
    - fastparquet==2023.2.0
    - lightgbm==3.3.5
    - tensorflow==2.10.0
    - pyod==1.0.9
    - gymnasium==0.28.1
    - stable-baselines3[extra]==2.0.0



- Update conda as needed:
```
conda update -n base -c defaults conda
```
- Install Python3.10.8, other packages written in py310pip_pkgs.yml
  and upgrade pip as needed.
```
conda env create --name py310pip_base --file py310pip_base.yml
conda create --name finclient --clone py310pip_base
conda activate finclient
pip install --upgrade pip
conda deactivate
conda env update --name finclient --file py310pip_finclient.yml
```