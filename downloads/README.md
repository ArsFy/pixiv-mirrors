# Downloads
Download all pictures from Pixiv and compress them with Avif.

### Install

- Python3
- ImageMagick (cli)

### Config

1. Edit `./config.py`

```python
cookie = "PHPSESSID=xxxxxxxxxxxx" # Your Pixiv Cookie
db_user = "database username"
db_pass = "database password"
db_host = "database host"
db_name = "database name"
```

2. Edit Start ID `./now`

```
123456
```

### Run

```
pip3 install -r requirements.txt
python3 main.py
```