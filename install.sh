clear;
python3 -m pip install -r requirements.txt;
python3 -m isort __main__.py;
python3 -m black __main__.py;
pyinstaller __main__.py -n="TailorMate" -Dy;
./dist/TailorMate/TailorMate;
exit;