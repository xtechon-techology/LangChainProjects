cp -R /apps/ids/drax-fastgs /apps/
echo "Copied fastgs folder"
cd /apps/drax-fastgs
echo "Moved to fastgs folder"
python3.9 -m venv fastgs_env_v3
echo "Virtual environment created"
source fastgs_env_v3/bin/activate
echo "Virtual environment activated"
#install packages from requirements.txt
pip3.9 install -r requirements.txt
echo "Packages installed"
cd /apps/
echo "Moved to apps folder"
chomd 777 /apps/drax-fastgs
chomd 777 /apps/drax-fastgs/*
echo "Permissions granted"
nohup /apps/drax-fastgs/fastgs_env_v3/bin/python3.9 /apps/drax-fastgs/fastgs_env_v3/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
echo "Fastgs started"
