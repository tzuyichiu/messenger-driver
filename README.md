# Messenger Driver

## Overview

A simple tool using `selenium` which allows to automate message sending 
in any conversation on `messenger.com`. It can be used, for example, to 
customize an autoreply for new incoming messages, or create flooding messages 
to a friend that you don't really like.

Cookies concerning login information will be saved into a pickle file called 
`MessengerCookies.pkl` which will then be loaded for future usage to avoid 
having to login again.

## Prerequisites

```bash
pip install selenium
```

- If you use Firefox, install **geckodriver** from:
https://github.com/mozilla/geckodriver/releases

- If you use Chrome, install **chromedriver** from:
https://chromedriver.chromium.org

Make sure to place the installed driver inside this repository or any directory
in your `$PATH`.

## Usage

```bash
python main.py -b <browser>
```
with `<browser>=(firefox|chrome)`.