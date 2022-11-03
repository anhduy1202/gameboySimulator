# Gameboy Simulator
> Desktop app to simulate gameboy image style [WIP]

> Made with PyQt5 and openCV

# Screenshots

<img width="640" alt="Screen Shot 2022-09-25 at 7 22 58 PM" src="https://user-images.githubusercontent.com/58461444/192181497-7a517a3f-1565-4bfe-9783-8f14d5672e3b.png">

<img width="640" alt="Screen Shot 2022-11-03 at 1 19 49 AM" src="https://user-images.githubusercontent.com/58461444/199675276-871e4a60-2af9-49b5-a2fd-52a00bcec19d.png">


# Requirements
* Python v3.0 >=
* Text Editor ( highly recommend PyCharm )
* [Qt Creator](https://www.qt.io/download) - Mac user only


# Getting Started
1. Clone this repo

``` git clone https://github.com/anhduy1202/gameboySimulator.git```

2. Install Pipenv 

``` pip install --user pipenv ``` or ``` pip3 install --user pipenv ``` 

3. Activate Pipenv

``` pipenv shell ```

4. Install packages from Pipfile.lock

``` pipenv sync ```

5. Run the program

``` python main.py ```

# Contributing
## Check [CONTRIBUTING.MD](https://github.com/anhduy1202/gameboySimulator/blob/master/CONTRIBUTING.md) to contribute to the project

# Files Description

**main.py** : Main file of the program that store logic of the dekstop app

**webcamMode.py** : File for Webcam mode option

**imageProcessing.py** : File contains gameboy image converting algorithm

**window.ui** : Design file that's created from Qt Creator to build the UI of the desktop app

**requirements.txt** : Requirements file to help downloading Python packages
