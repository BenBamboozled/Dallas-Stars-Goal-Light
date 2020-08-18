
# Dallas-Stars-Goal-Light

Simple Python program that checks with the NHL API for Dallas Stars hockey games and publishes a message to a mqtt topic when they score or win to light up a LED light I have. This program can work with any given team in NHL. Depending on smart devices you could also modify this program to play goal horns and other things. 
## Prerequisites
- Python 3 and pip installed

## Setup

1. First clone this repository
    
    `git clone https://github.com/BenBamboozled/Dallas-Stars-Goal-Light`

2. Next install all dependencies in requirements.txt in the repo
    
    `pip install -r requirements.txt`

3. Next open dallasStars.py and you can customize to your team. By changing lines 12 and 13 to match your team. You can find your teams info at [https://statsapi.web.nhl.com/api/v1/teams]. You can also make changes to delays so you can get a responsew more or less frequently. You  can also change the file name to matchj your team. 

4. Now you can run the program. Using the new name of your python file.
   
    `python dallasStars.py`

If your team does not have game on the given day, the program will quit. If there is a game it waits until the game is live by checking every minute then get updates for the game every 30 seconds once it is live. this program uses mqtt to trigger my LEDS to light up green, you will need to create your own function or do another event like play music over speaker. 


If everything works correctly the setup is complete. You can now run this file manually any time you want. 


## Optional Automation of program

Personally I do not want to manually start this program every game so I have set it up to run through my crontab on my linux server that is always on. To edit this file enter this command.

    sudo crontab -e  

Most distrubution of linux will open the file in vim other distributions ask which text editor to use like ubuntu wehere you could specify to edit with nano. Now add the schedule for the program.


`0 17 * 10-12 * python location_of_program`

`0 17 * 1-6 * python location_of_program`

This will run the program everyday at 17:00 or 5 PM from October to June the months of hockey season. If there is no game the program will end almost instantly if there  is a game the program will wait until the game satarts then update the scores. 



