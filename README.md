## Port Scanner
a simply tcp port scanner, both of a specific ip and of specific sites, created completely by me, based on the services configured in the nmap "service" file.

## requisites 🚨
- Python `>= v3.6.0`
- pip `>= 22.0.0`

## installation instructions 📘
#### clone this repository with `git clone` and install the requirements.txt
```shell
git clone https://github.com/PietroLoparco/PortScanner.git
cd pscanner
python -m pip install -r requirements.txt
```

## Usage 💻
#### run the file with the command `python pscanner.py -h` to know all the options
```shell
usage: pscanner.py [options] [options argument]

Host port scanner.

options:
  -h, --help            show this help message and exit
  -ip IP                Set target ip
  -url URL              Set target url
  --start_port START_PORT
                        Set the port where scanning will begin (Default 1)
  --end_port END_PORT   Set the port where scanning will end (Default 1024)

example: pscanner.py -ip <ip> --start_port <start_port> --end_port <end_port>
```
