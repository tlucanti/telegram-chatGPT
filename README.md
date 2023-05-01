# telegram-chatGPT

### use gpt chat directly from telegram
## Features:
 - multiple users
 - role selection
 - temperature selection
 - gpt instance reset
 - logging system

# commands:
### start
```
/start
```
Start conversation

### temp
```
/temp
```
Command opens menu to select temperature hyperparameter for gpt. Use low value for formal proofs, solving tasks and
other technical questions. Use high value for more creative answers and non technical questions, like
introductions and conclusions for articles and other places when you need more words. For more info
you can ask gpt itself. 

### role
```
/role
```
Command asks to provede a new role in next message for gpt assistant. You can use roles like
'you are an article writing assistant' to help with article writing, or 'you are an interesting companion'
for chatting, or even 'you are an pirate' to get pirate styled messages

### reset
```
/reset
```
Reset gpt instance and start conversation from begining

### help
```
/help
```
Prints help message with brief description for all commands

# install and run
#### dependencies
- `python3`
- `pip3`
#### python modules
- `openai`
- `python-telegram-bot`

before first launch run `install.sh` script to install needed modules for python:
```shell
sh install.sh
```
## tokens
you need to place your openai token to file `.openai.token` and telegram token to file `.simplebot.token` in the root of repo

### lauch
you can lauch bot simply by
```shell
python3 SimpleGPTbot.py
```
and it will write all logs to stdout
### daemon
if you want to run bot as daemon - run `daemon.sh` script:
```shell
sh daemon.sh
```
it will disconnect process from current shell (and you can close it) and write all logs to `log.txt` file.


To stop daemon just find process with `px aux` and `kill` it:
```shell
ps aux | grep 'python3 SimpleGPTbot.py'
kill 130822
```
