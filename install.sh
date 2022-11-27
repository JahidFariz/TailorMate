#!/bin/bash

clear;

echo "> sudo apt update";
sudo apt update;
echo;

apt list --upgradable -a;
echo;

echo "> sudo apt install python3 python3-pip python3-tk python3-venv xtitle";
sudo apt install python3 python3-pip python3-tk python3-venv;
echo;

echo "> sudo apt autoremove";
sudo apt autoremove;
echo;

if [ -f "./requirements.txt" ]; then
	python3 -m pip install -r ./requirements.txt;
	echo;
fi

if [ -f "./private.py" ]; then
  isort ./private.py
  black ./private.py
  echo;
fi

if [ -f "./__main__.py" ]; then
	isort ./__main__.py;
	black ./__main__.py;
	echo;

	pyinstaller __main__.py -Fy -n="TailorMate" --add-data="./assets/*:./assets/" --add-data="./LICENSE:./" \
	--add-data="./venv/lib/python3.*/site-packages/pyfiglet/fonts/*:./pyfiglet/fonts/";
  	echo;
fi

if [ -d "./build" ]; then
	rm -r -v build;
	echo;
fi

if [ -f "./TailorMate.spec" ]; then
	rm -f -v TailorMate.spec;
	echo;
fi

if [ -f "./dist/TailorMate" ]; then
	./dist/TailorMate;
fi

exit;
