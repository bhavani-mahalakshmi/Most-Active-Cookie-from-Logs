import datetime
import unittest
import csv
import random
import math

from most_active_cookie_old import CookieProcessor
from string import ascii_letters
from random import randint
from datetime import timezone


class DataGenerator:

    def generate_random_date(self, dummy_date=False):
        year, month, day = randint(2000, 2021), randint(1, 12), randint(1, 28)
        hour, minute, second = randint(1, 23), randint(1, 59), randint(1, 59)
        if dummy_date:
            year, month, day = 9999, 9, 9
        date = datetime.datetime(year, month, day, hour, minute, second,
                                 tzinfo=timezone.utc)
        return date.strftime("%Y-%m-%dT%H:%M:%S%z")

    def generate_date_mask(self, count_mask, max_same_date, num_dates=10):
        date_mask = []
        max_count = max(count_mask)
        max_occurrences = count_mask.count(max_count)
        max_query_day_count = randint(1,
                                      max_occurrences) if not max_same_date else max_occurrences
        other_query_day_count = randint(1,
                                        num_dates - max_occurrences) if num_dates - max_occurrences > 0 else 0
        query_date_index = randint(0, num_dates - 1)
        excluded_list = list(range(num_dates))
        excluded_list.pop(query_date_index)
        for count in count_mask:
            if count == max_count:
                if max_query_day_count > 0:
                    date_mask.append(query_date_index)
                    max_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    date_mask.append(date_index)
            else:
                if other_query_day_count > 0:
                    date_mask.append(query_date_index)
                    other_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    date_mask.append(date_index)

        return date_mask, query_date_index

    def generate_count_mask(self, num_unique_cookies, num_cookies,
                            max_same_date):
        count_mask = []
        cookies_left = num_cookies
        for i in range(num_unique_cookies):
            if i < num_unique_cookies - 1:
                add_amount = randint(1, math.ceil(
                    num_cookies // num_unique_cookies))
            else:
                if max_same_date:
                    add_amount = randint(1, math.ceil(
                        num_cookies // num_unique_cookies))
                else:
                    add_amount = cookies_left
            count_mask.append(add_amount)
            cookies_left -= add_amount
        return count_mask

    def generate_test_data(self, exists=True, max_same_date=False,
                           num_unique_cookies=10, num_cookies=20, num_dates=10):
        cookie_list = self.generate_cookies(num_unique_cookies)
        date_list = [self.generate_random_date() for i in range(num_dates)]
        count_mask = self.generate_count_mask(num_unique_cookies, num_cookies,
                                              max_same_date)
        max_count = max(count_mask)
        date_mask, query_date_index = self.generate_date_mask(count_mask,
                                                              max_same_date,
                                                              num_dates)
        test_data, test_solutions = [], set()
        query_date = date_list[
            query_date_index] if exists else self.generate_random_date(
            dummy_date=True)
        for cookie_num in range(num_unique_cookies):
            rows = []
            cookie, num_rows = cookie_list[cookie_num], count_mask[cookie_num]
            date = date_list[date_mask[cookie_num]]
            for row_num in range(num_rows):
                rows.append([cookie, date])

            if num_rows == max_count and date == query_date:
                test_solutions.add(cookie)
            test_data.extend(rows)
        self.write_csv(test_data)
        return query_date.split("T")[0], test_solutions

    def write_csv(self, data):
        with open("big_file.csv", "w") as test_file:
            csv_writer = csv.writer(test_file)
            csv_writer.writerow(["cookie", "timestamp"])
            for row in data:
                csv_writer.writerow(row)

    def generate_cookies(self, num_unique=10):
        cookie_list = []
        valid_symbols = list(ascii_letters)
        valid_symbols.extend([0, 1, 2, 3, 5, 6, 7, 8, 9])
        for i in range(num_unique):
            cookie = "".join(
                [str(random.choice(valid_symbols)) for _ in range(30)])
            cookie_list.append(cookie)
        return cookie_list


class CookieProcessorTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_generator = DataGenerator()

    def test_nonexistent(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            exists=False)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_same_day_max(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True, num_unique_cookies=10, num_cookies=20,
            num_dates=2)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_mixed_days(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data()
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_medium(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_cookies=5000, num_dates=25)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_large(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_unique_cookies= 250,
            num_cookies=25000, num_dates=25)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_very_large(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_unique_cookies=500,
            num_cookies=50000, num_dates=25)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_large_overlaps(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True,
            num_unique_cookies=500,
            num_cookies=25000, num_dates=25)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_very_large_overlaps(self):
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True,
            num_unique_cookies=500,
            num_cookies=50000, num_dates=25)
        cookie_processor.process_file("big_file.csv")
        computed_cookies = cookie_processor.get_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_all_multiple_iter(self, iterations=10):
        for iteration in range(iterations):
            self.test_nonexistent()
            self.test_mixed_days()
            self.test_same_day_max()
            self.test_medium()
            self.test_large()
            self.test_very_large()
            self.test_large_overlaps()
            self.test_very_large_overlaps()


if __name__ == '__main__':
    unittest.main()
