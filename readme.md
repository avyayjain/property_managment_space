# This is an Project about the property management system


## Installation
1. Clone the repository
```commandline
git clone https://github.com/avyayjain/property_managment_space.git
```

2. Install the requirements
```commandline
pip install -r requirements.txt
```
3. run the server
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
``` 
you can also use fastapi cli
```bash
fastapi dev main.py
```
4. you can also build the docker container by running the following command
```bash
docker build -t video_manegement .
```
5. you can run the docker container by running the following command
```bash
docker run -d -p 8000:8000 video_manegement
```

