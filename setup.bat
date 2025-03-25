@echo off
echo 正在创建项目目录结构...

:: 创建必要的目录
mkdir css 2>nul
mkdir js 2>nul
mkdir assets 2>nul
mkdir assets\images 2>nul
mkdir files 2>nul

echo 目录结构创建完成！
echo.
echo 请将您的附件文件放在 files 文件夹中：
echo - attachment1.pdf
echo - attachment2.pdf
echo - attachment3.pdf
echo - attachment4.pdf
echo - video.mp4
echo.
pause 