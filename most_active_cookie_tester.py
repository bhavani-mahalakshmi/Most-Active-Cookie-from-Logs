from datetime import datetime, timezone
import unittest, math, csv
from string import ascii_letters
from most_active_cookie import CookieProcessor
from random import choice, randint

class DataGenerator:
    def generate_cookies(self, num_unique=10):
        cookie_list = []
        valid_chars = list(ascii_letters)
        valid_chars.extend([0,1,2,3,4,5,6,7,8,9])
        for _ in range(num_unique):
            cookie = "".join(
                str(choice(valid_chars)) for _ in range(30)
            )
            cookie_list.append(cookie)
        return cookie_list

    def generate_random_date(self, dummy_date=False):
        if dummy_date:
            year, month, date = 9999, 9, 9
        year, month, date = randint(2000,2021), randint(1,12), randint(1,28)
        hour, minute, second = randint(1,23), randint(1,59), randint(1,59)

        d = datetime(year, month, date, hour, minute, second, tzinfo=timezone.utc)
        return d.strftime("%Y-%m-%dT%H:%M:%S%z")

    def generate_count_mask(self, num_unique, num_cookies, max_same_date):
        count_list = []
        cookies_left = num_cookies
        for i in range(num_unique):
            if i < num_unique - 1:
                add_amount = randint(1, math.ceil(num_cookies//num_unique))
            else:
                if max_same_date:
                    add_amount = randint(1, math.ceil(num_cookies//num_unique))
                else:
                    add_amount = cookies_left
            count_list.append(add_amount)
            cookies_left -= add_amount
        return count_list

    def generate_date_mask(self, num_dates, count_mask, max_same_date):
        date_mask = []
        max_count = max(count_mask)
        max_occurences = count_mask.count(max_count)
        #if same date should have all active cookies, max query day count will be max occurences
        # cos max query day count number of dates should have the most active cookies, if not
        # max query day count can be any one of the max occurences dates 
        if not max_same_date:
            max_query_day_count = randint(1, max_occurences)
        else:
            max_query_day_count = max_occurences
        
        # for other dates, the count can be one among the diff btw total dates and max occurences or 0
        if num_dates - max_occurences > 0:
            other_query_day_count = randint(1, num_dates - max_occurences)
        else:
            other_query_day_count = 0
        
        query_date_index = randint(1, num_dates-1)
        excluded_list = list(range(num_dates))
        excluded_list.pop(query_date_index)

        for count in count_mask:
            if count == max_count:
                if max_query_day_count > 0:
                    date_mask.append(query_date_index)
                    max_query_day_count -= 1
                else:
                    date_mask.append(choice(excluded_list))
            else:
                if other_query_day_count > 0:
                    date_mask.append(query_date_index)
                    other_query_day_count -= 1
                else:
                    date_mask.append(choice(excluded_list))
        return date_mask, query_date_index                
            
    def write_csv(self, data):
        with open("test_data.csv", "w") as test_file:
            csv_writer = csv.writer(test_file)
            csv_writer.writerow(["cookie","timestamp"])
            for row in data:
                csv_writer.writerow(row)

    def generate_test_data(self, exists=True, max_same_date=False, num_unique_cookies=10, num_cookies=20, num_dates=10):
        cookies = self.generate_cookies(num_unique_cookies)
        dates = [ self.generate_random_date() for _ in range(num_dates) ]
        count_mask = self.generate_count_mask(num_unique_cookies, num_cookies, max_same_date)
        max_count = max(count_mask)

        date_mask, query_date_index = self.generate_date_mask(num_dates, count_mask, max_same_date)

        if exists:
            query_date = dates[query_date_index]
        else:
            query_date = self.generate_random_date(True)
        
        test_data, test_solutions = [], set()
        for cookie_i in range(num_unique_cookies):
            rows = []
            cookie = cookies[cookie_i]
            count = count_mask[cookie_i]
            date = dates[date_mask[cookie_i]]
            for _ in range(count):
                rows.append([cookie, date])
            test_data.extend(rows)

            if count == max_count and date == query_date:
                test_solutions.add(cookie)
        self.write_csv(test_data)
        return query_date.split("T")[0], test_solutions

class CookieProcessorTester(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.data_generator = DataGenerator()

    def perform_test(self, test_date, solutions):
        cp = CookieProcessor()
        cp.process_file("test_data.csv")
        computed_result = cp.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_result)

    def test_non_existent(self):
        date, solutions = self.data_generator.generate_test_data(
            exists=False
        )
        self.perform_test(date, solutions)

    def test_same_day_max(self):
        date, solutions = self.data_generator.generate_test_data(
            max_same_date=True, num_dates=2
        )
        self.perform_test(date, solutions)

    def test_mixed_days(self):
        date, solutions = self.data_generator.generate_test_data()
        self.perform_test(date, solutions)

    def test_medium(self):
        date, solutions = self.data_generator.generate_test_data(
            num_cookies=5000, num_dates=25
        )
        self.perform_test(date, solutions)

    def test_large(self):
        date, solutions = self.data_generator.generate_test_data(
            num_cookies=25000, num_dates=25, num_unique_cookies=250
        )
        self.perform_test(date, solutions)

    def test_very_large(self):
        date, solutions = self.data_generator.generate_test_data(
            num_cookies=50000, num_dates=25, num_unique_cookies=500
        )
        self.perform_test(date, solutions)

    def test_large_overlaps(self):
        date, solutions = self.data_generator.generate_test_data(
            num_cookies=25000, num_dates=25, num_unique_cookies=250, max_same_date=True
        )
        self.perform_test(date, solutions)

    def test_very_large_overlaps(self):
        date, solutions = self.data_generator.generate_test_data(
            num_cookies=50000, num_dates=25, num_unique_cookies=500, max_same_date=True
        )
        self.perform_test(date, solutions)

    def test_all(self, iterations=10):
        for _ in range(iterations):
            self.test_non_existent()
            self.test_mixed_days()
            self.test_same_day_max()
            self.test_medium()
            self.test_large()
            self.test_very_large()
            self.test_large_overlaps()
            self.test_very_large_overlaps()

if __name__ == "__main__":
    unittest.main()