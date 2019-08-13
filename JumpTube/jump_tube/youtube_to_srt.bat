set PHYPATH=%JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27
set PATH=%PHYPATH%;%PHYPATH%\Scripts;%PATH%
%JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\youtube-dl.exe --id --recode-video mp4  https://www.youtube.com/watch?v=%1
python %JUMPTUBE_ROOT_DIR%\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S %2 -D %2 %1.mp4
del %1.mp4 -y



