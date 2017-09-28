# Instalation

1. Install Selenium-python
```
pip install selenium
```

2. Download driver and place it on same PATH as index.py.

3. Execute and enjoy
```
py index.py
```

4. Available endpoints:
  * `/init` - Start browser
  * `/status` - Give current browser status
  * `/newtab` - Open tab
  * `/switchtab?tab={No.Tab}` - Switch to X tab
  * `/open?site={site as: google.com, yourube.com}` - Open site in current tab

## Important
Beware this example uses Chromium driver by `.Chrome()`
