pip3 uninstall virtualenv

pip3 install virtualenv

virtualenv -p python3 ~/python-env/caring-people

source ~/python-env/caring-people/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

deactivate
