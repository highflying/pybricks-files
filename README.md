brew install pipx
pipx install pybricksdev
pipx install virtualenv
pipx ensurepath
source ~/.zprofile
virtualenv --python python3.11 venv
source ./venv/bin/activate
pip install pybricks
pip install pybricksdev
