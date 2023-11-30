# Setup
Run `python ./src/utils/setup.py`
Edit the session.cookie newly created file with your session cookie to auto-download inputs. To find it on Chrome: right-click, inspect, Application tab, Storage, Cookies, session.
Edit the ./src/utils/config.py file with the year you want to work on

## Creating a new solution

Run `python ./src/utils/new_solution.py` creates a new file for today, it checks for the files in `src/` and creates the "next int" one. On the first run it will create `01.py`, later `02.py`, and so on.

A new solution is initialized as follows: 
```
from utils.api import get_input

input_str = get_input(1)

# WRITE YOUR SOLUTION HERE
```
The `get_input` function takes a day and returns the content of the input for that day, this internally makes a request to obtain the input if it is not found on disk. 

## Running a new solution

From the main directory, run `python src/<DAY>.py`.
