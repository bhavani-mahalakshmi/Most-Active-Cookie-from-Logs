import argparse
import csv
import sys


class CookieProcessor:
    def __init__(self):
        self.cookies_dict = {}
        self.count_dict = {}

    def get_active_cookies(self, date):
        most_active_cookies = set()
        if date in self.count_dict:
            max_occurrence = max(self.count_dict[date].keys())
            most_active_cookies = self.count_dict[date][max_occurrence]
            for cookie in most_active_cookies:
                print(cookie)
        return most_active_cookies

    def process_file(self, log_path):
        with open(log_path, newline='') as cookie_log:
            log_reader = csv.DictReader(cookie_log)
            for log_row in log_reader:
                self.process_entry(log_row)

    def process_entry(self, row):
        cookie, date = row['cookie'], row['timestamp']
        date = self.get_date(date)
        if date not in self.cookies_dict:
            self.cookies_dict[date] = {cookie: 1}
        else:
            if cookie not in self.cookies_dict[date]:
                self.cookies_dict[date][cookie] = 1
            else:
                self.cookies_dict[date][cookie] += 1
        count = self.cookies_dict[date][cookie]

        if date not in self.count_dict:
            self.count_dict[date] = {count: set([cookie])}
        else:
            if count not in self.count_dict[date]:
                self.count_dict[date][count] = set([cookie])
            else:
                self.count_dict[date][count].add(cookie)
                if count > 1:
                    self.count_dict[date][count - 1].remove(cookie)

    def get_date(self, date):
        return date.split("T")[0]


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='most_active_cookie.py',
        description='Returns the most active cookies on a date, '
                    'given CSV consisting of cookie and timestamp',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument("file_path")
    arg_parser.add_argument("--date", "-d")
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    cookie_processsor = CookieProcessor()
    cookie_processsor.process_file(args["file_path"])
    cookie_processsor.get_active_cookies(args["date"])
