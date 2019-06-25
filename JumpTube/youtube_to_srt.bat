set PHYPATH=D:\Projects\git_clones\JumpTube\JumpTube\python_env_for_autosub\Python27
set PATH=%PHYPATH%;%PHYPATH%\Scripts;%PATH%
D:\Projects\git_clones\JumpTube\JumpTube\python_env_for_autosub\youtube-dl.exe --id --recode-video mp4  https://www.youtube.com/watch?v=%1
python D:\Projects\git_clones\JumpTube\JumpTube\python_env_for_autosub\Python27\Scripts\autosub_app.py  -S iw -D iw %1.mp4


