# Messenger Driver

## Overview

A simple tool using `selenium` which allows to automate message sending 
in any conversation on `messenger.com`. It can be used, for example, to 
customize an automatic response for new incoming messages, or create 
overflowing messages to a friend that you don't really like.

Cookies concerning login information will be saved into a pickle file called 
`MessengerCookies.pkl` which will then be loaded for future usage to avoid 
having to login again.

## Prerequisites

```bash
pip install selenium
```

## Usage

```bash
python main.py
```
