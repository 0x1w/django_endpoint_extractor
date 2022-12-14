## django_endpoint_extractor
A simple python script to get all endpoints from django 404 page with debug information presented


## Installation
```commandline
git clone https://github.com/0x1w/django_endpoint_extractor
cd django_endpoint_extractor
pip3 install -r requirements.txt
```

## Usage
```commandline
python3 main.py https://example.com/404
python3 main.py -o output.txt https://example.com/404
python3 main.py -o output.txt --delay 0.2 https://example.com/404
```
