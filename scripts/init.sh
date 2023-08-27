# Script to Initialize the project
pyenv local 3.9.12
bash scripts/createAllUtilsSymlink.sh
checks_dir=src/checks/
pip install --upgrade pip
find $checks_dir -name requirements.txt -exec pip install -r {} \;