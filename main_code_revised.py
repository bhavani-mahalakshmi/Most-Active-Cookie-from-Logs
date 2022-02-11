import sys, argparse, csv

class CookieProcessor:
    def __init__(self) -> None:
        self.cookies_dict = {}
        self.count_dict = {}

    def process_file(self, file_path):
        with open(file_path, newline='') as contents:
            logs = csv.DictReader(contents)
            for log in logs:
                self.process_log(log)

    def process_log(self, log):
        cookie, date = log["cookie"], log["timestamp"]
        date = self.process_date(date)

        #update cookie dict
        if date not in self.cookies_dict:
            self.cookies_dict[date] = {cookie: 1}
        else:
            if cookie not in self.cookies_dict[date]:
                self.cookies_dict[date][cookie] = 1
            else:
                self.cookies_dict[date][cookie] += 1
        
        #update count dict
        count = self.cookies_dict[date][cookie]
        if date not in self.count_dict:
            self.count_dict[date] = {count: set([cookie])}
        else:
            if count not in self.count_dict[date]:
                self.count_dict[date][count] = set([cookie])
            else:
                if count>1:
                    self.count_dict[date][count-1].remove(cookie)
                self.count_dict[date][count].add(cookie)

    def process_date(self, date):
        date_parts = date.split("T")
        return date_parts[0]

    def find_active_cookies(self, date):
        if date in self.count_dict:
            max_occurence = max(self.count_dict[date].keys())
            return set(self.count_dict[date][max_occurence])
        return set()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog= 'new.py',
        usage='find the most active cookie on a given date',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # arg_parser.print_help()
    arg_parser.add_argument("file_path")
    arg_parser.add_argument("--date", "-d")
    # print(arg_parser.parse_args(["test.py"]))
    # print(arg_parser.parse_args(["test.py", "--date", "2021"]))
    # print(arg_parser.parse_args(["test.py", "--d", "2022"]))
    cmd_args = (sys.argv[1:])
    args = vars(arg_parser.parse_args(cmd_args))
    # print(cmd_args, args)
    cp = CookieProcessor()
    cp.process_file(args["file_path"])
    active_cookies = cp.find_active_cookies(args["date"])
    print(active_cookies)