#!/bin/bash -e
clear;
echo "> sudo apt update";
sudo apt update;
echo;
apt list --upgradable -a;
echo;
echo "> sudo apt install python3 python3-pip python3-tk python3-venv -y";
sudo apt install python3 python3-pip python3-tk python3-venv -y;
echo;
echo "> sudo apt autoremove -y";
sudo apt autoremove -y;
echo;
python3 -m venv venv;
if [ -f "./venv/bin/activate" ]; then
  source ./venv/bin/activate;
fi
python3 -m pip install --upgrade pip;
if [ -f "./requirements.txt" ]; then
	python3 -m pip install -r ./requirements.txt;
	echo;
fi
if [ -f "./__main__.py" ]; then
	python3 -m isort ./__main__.py;
	python3 -m black ./__main__.py;
	echo;
    pyinstaller __main__.py -n="TailorMate" -Dy;
    echo;
fi
deactivate;
rm -r -v build
rm -f -v TailorMate.spec
echo;
./dist/TailorMate/TailorMate;
exit;
