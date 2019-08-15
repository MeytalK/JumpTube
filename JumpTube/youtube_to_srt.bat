#echo on
set PHYPATH=%JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27
set PATH=%PHYPATH%;%PHYPATH%\Scripts;%PATH%
%JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\youtube-dl.exe --id  https://www.youtube.com/watch?v=%1
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.mp4
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.mp3
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.wav
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.mkv
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.m4a
del %1.mp4 -y
del %1.mp3 -y
del %1.wav -y
del %1.mkv -y
del %1.m4a -y
