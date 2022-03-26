# AnimationCutterSettingsGenerator
Generate settings for [AnimationCutter](https://github.com/Mebebonk/AnimationCutterPublic)

If you are using other OS than Windows you can run or build this application by yourself

## First run
You will need [Python](https://www.python.org/) to run this application. On different OS python command may look different(python, python3)
* Create directory
* Open command line in this directory and execute following command:
```commandline
git clone https://github.com/Mebebonk/AnimationCutterSettingsGenerator.git .
```
* After downloading project execute next command:
```commandline
python -m venv venv
```
* Next command would be:
```commandline
cd venv/Scripts
```
* Then enter this:
```commandline
activate
```
* Now you need to return to top level by following command:
```commandline
cd ../..
```
* Then you need to install all requirements:
```commandline
pip install -r requirements.txt
```
* Now you can run by typing:
```commandline
python src/main.py
```

## Repeat run
* Open command line in directory with AniamtionCutter Settings Generator and execute following commands:
```commandline
cd venv/Scripts
activate
cd ../..
python src/main.py
```

# Build
Application already using [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/usage.html) if you want executable file you can build it.
