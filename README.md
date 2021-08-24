# Precision_AG_Thesis
It is a plant health monitoring system

Process for running cloudside tests
<!-- Serverside -->
cd Cloud_loop
python3 cloudside.py
python3 SNR_logging.py

<!-- Edgeside -->
ssh nordluft_xaviernx@192.168.120.50
pwd = nordluft12

python3 jetson_statslogger.py
python3 edgeside.py
exit

Process for running edgeside tests
cd Edge_loop
python3 edgeloop.py
python3 jetson_statslogger.py
