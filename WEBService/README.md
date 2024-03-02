# Neurogeometry WEB-section

The easiest way to set and run local server is to run an executable build file (only for Windows)

LinuxOC requires a more individual approach. 

## Set up and run on Windows
```
build.bat
```

## Just run on Windows 
```
build.bat run
```

## Short instruction for LinuxOC
1) Clone this repository
2) Create virtual environment at ./WEBService and install packages from requirements.txt
3) Install npm, if you don't. Then install @vue/cli-service
4) Go to frontend folder and run ```vue build``` (create folders at ./WEBService `static` and `templates`, if it needs)
5) Change path to `algorithm` in ./WEVService/main/wrapper.py
6) Run `python3 manage.py runserver`