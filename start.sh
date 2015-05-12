source ./venv/bin/activate

fab create_vm

cd openstax-setup 
fab deploy
cd ..

cd cnx-setup
fab deploy
cd ..
