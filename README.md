# most-active-cookie

### Please install requirements.txt if you are planning to use python 2 instead of python 3.
Usage: pip install -r requirements.txt

## Usage with Examples
The CLI program takes two arguments: 
- The CSV file path
- `-d`, the date argument formatted as YYYY-MM-DD  

`most_active_cookie.py` calculates the most active cookie(s) on a given date (YYYY-MM-DD) from a CSV log file (here, sample_file.csv) provided in the correct format (cookie, timestamp).

Usage: `python3 most_active_cookie.py sample_file.csv -d 2018-12-08`

`most_active_cookie_tester.py` is created with Python's 'unittest' package. The test data is generated using a probabilistic approach, and the random number generators are given by Python's 'random' package. It includes situations where the requested date isn't in the dataset and where all of the most active cookies occur on the same day, separate days, or a combination of the two. Although the probabilistic nature of data production cannot guarantee that a test case will occur, for example, more than one cookie will have the same occurrence, the probability are high enough that certain test cases are **expected** to occur. In practice, there are more huge test cases and a 'test all multiple iter' test that increase the chances of these situations happening, e.g., executing these should make it **extremely likely** that more than one cookie will have the same occurrence. Finally, because the technique is done using a hashmap of dates, the order of dates in the CSV does not necessarily increase over time.

Usage: `python3 most_active_cookie_tester.py`
