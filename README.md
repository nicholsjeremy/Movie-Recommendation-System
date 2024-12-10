The ways to log in the kafka server: tunnel@128.2.204.215
- Use command: ssh -o ServerAliveInterval=60 -L 9092:localhost:9092 tunnel@128.2.204.215 -NTf
- Use password: mlip-kafka

You need Python 3.9 to run the dependencies correctly. Use a conda env:
$ conda create --name mlip17 python=3.9

To activate an existing env,
$ conda activate mlip17

To install requirements:
$ pip install -r requirements.txt

run extract script to create the dataset
- $ python kafka_to_csv.py

run svd model
- $ python svdmodel.py

run knn model
- $ python knn.py
