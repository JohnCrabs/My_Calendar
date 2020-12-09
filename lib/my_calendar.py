"""
my_calendar.py contains a Class Calendar, which creates a dictionary with events for a specific year.

Calendar Structure:
Dict{Date_Format: {Time_Format: {City: {Date: , Time: , Temperature: }}}}

Example: Let's say we need to add a temperature event, we can do it like this.
Dict{'08/01/2020': {'00:00': {'Athens': {Date: '08/01/2020', Time: '00:00', Temperature: '26.2',
                              'Brest': {Date: '08/01/2020', Time: '00:00', Temperature: '16.6'}}}}

Let's say we need to export it to excel:
1) Give date range for the exporting dates (e.g. start: 08/01/2020, end: 11/30/2020)
2) Give the format of the file (CSV of XLSX)
3) Create First Line ['Date', 'Time', 'Athens_Temperature', 'Brest_Temperature]
4) For each date in range export these value. If value does not exist print -9999.99
"""
import datetime as dt
import warnings

str_id_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
str_id_single_months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

str_id_days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
               '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
               '25', '26', '27', '28', '29', '30', '31']
str_id_single_days = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                      '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
                      '25', '26', '27', '28', '29', '30', '31']

str_id_hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
str_id_minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                  '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                  '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                  '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                  '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']

int_month_days_not_leap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
int_month_days_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Different systems to create a date
DD_MM_YYYY = 'ddmmyyyy'
DD_YYYY_MM = 'ddyyyymm'
MM_DD_YYYY = 'mmddyyyy'
MM_YYYY_DD = 'mmyyyydd'
YYYY_MM_DD = 'yyyymmdd'
YYYY_DD_MM = 'yyyyddmm'

D_M_YYYY = 'dmyyyy'
D_YYYY_M = 'dyyyym'
M_D_YYYY = 'mdyyyy'
M_YYYY_D = 'myyyyd'
YYYY_M_D = 'yyyymd'
YYYY_D_M = 'yyyydm'

DD_MM_YY = 'ddmmyy'
DD_YY_MM = 'ddyymm'
MM_DD_YY = 'mmddyy'
MM_YY_DD = 'mmyyydd'
YY_MM_DD = 'yymmdd'
YY_DD_MM = 'yyddmm'

D_M_YY = 'dmyy'
D_YY_M = 'dyym'
M_D_YY = 'mdyy'
M_YY_D = 'myyd'
YY_M_D = 'yymd'
YY_D_M = 'yydm'

# Delimeters
del_comma = ','
del_hashtag = '#'
del_colon = ':'
del_semicolon = ';'
del_space = ' '
del_underscore = '_'
del_dash = '-'
del_slash = '/'


# Read Csv
def read_csv(path: str, delimeter=del_comma):
    import csv
    list_tmp = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter)
        for row in csv_reader:
            list_tmp.append(row)
    return list_tmp


def write_csv(path: str, list_write, delimeter=del_comma):
    import csv
    with open(path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimeter,
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in list_write:
            csv_writer.writerow(row)


class Calendar:
    def __init__(self, year=dt.datetime.now().year):
        self.year = year
        self.leap = self.isLeap(year)
        self.date_format = DD_MM_YYYY
        self.date_delimeter = del_slash
        self.list_timespamp = None
        self.int_list_size = 0
        self.dict_calendar = {}

    @staticmethod
    def isLeap(year=dt.datetime.now().year):
        """
        :param year: The year we need to check
        :return: True/False
        """
        if year % 4 == 0:
            if year % 100 != 0 or year % 400 == 0:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def set_time(hour_start=0, hour_end=24, hour_step=1, minute_start=0, minute_end=60, minute_step=0):
        """
        :param hour_start: The starting hour. Range (0, 24)
        :param hour_end: The ending hour. Range (0, 24)
        :param hour_step: The step for hours. Range (1, 24). Big step means same hour.
        :param minute_start: The starting minute. Range (0, 60).
        :param minute_end: The ending minute. Range (0, 60)
        :param minute_step: The minute step. Range (0, 60). Big step means the same minute every hour.
        :return:
        """
        if hour_start < 0 or hour_start > 24:
            warnings.warn("Hour start out of range. Set it to default value '0'")
            hour_start = 0
        if hour_end < hour_start or hour_end > 24:
            warnings.warn("Hour end out of range. Set it to default value '24'")
            hour_end = 24
        if minute_start < 0 or minute_start > 60:
            warnings.warn("Minute start out of range. Set it to default value '0'")
            minute_start = 0
        if minute_end < minute_start or minute_end > 60:
            warnings.warn("Minute end out of range. Set it to default value '60'")
            minute_end = 60

        list_timestamp = []
        int_size = 0

        if hour_step <= 0:
            return None
        else:
            for hour in range(hour_start, hour_end, hour_step):
                if minute_step == 0:
                    timestamp_tmp = str_id_hours[hour] + ':'
                    timestamp_tmp += str_id_minutes[0]
                    list_timestamp.append(timestamp_tmp)
                    int_size += 1
                    # print(timestamp_tmp)
                else:
                    for minutes in range(minute_start, minute_end, minute_step):
                        timestamp_tmp = str_id_hours[hour] + ':'
                        timestamp_tmp += str_id_minutes[minutes]
                        list_timestamp.append(timestamp_tmp)
                        int_size += 1
                        # print(timestamp_tmp)
        # print(list_timestamp)
        return list_timestamp, int_size

    @staticmethod
    def change_day_month_to_single_format(day, month):
        day_single = int(day)
        day_single = str_id_single_days[day_single - 1]
        month_single = int(month)
        month_single = str_id_single_months[month_single - 1]
        return day_single, month_single

    @staticmethod
    def change_day_month_to_double_format(day, month):
        day_double = int(day)
        day_double = str_id_days[day_double - 1]
        month_double = int(month)
        month_double = str_id_months[month_double - 1]
        return day_double, month_double

    @staticmethod
    def date_break_to_day_month_year(date: str, date_format: str, date_delimeter=del_slash, century=21):
        """
                Check the format of the day (eg DD/MM/YYYY) and returns a string.
                :param century: The current century
                :param date: The date to be changed
                :param date_format: The date format. Can be: DD_MM_YYYY
                                                             DD_YYYY_MM
                                                             MM_DD_YYYY
                                                             MM_YYYY_DD
                                                             YYYY_MM_DD
                                                             YYYY_DD_MM
                                                             D_M_YYYY
                                                             D_YYYY_M
                                                             M_D_YYYY
                                                             M_YYYY_D
                                                             YYYY_M_D
                                                             YYYY_D_M
                                                             DD_MM_YY
                                                             DD_YY_MM
                                                             MM_DD_YY
                                                             MM_YY_DD
                                                             YY_MM_DD
                                                             YY_DD_MM
                                                             D_M_YY
                                                             D_YY_M
                                                             M_D_YY
                                                             M_YY_D
                                                             YY_M_D
                                                             YY_D_M

                :param date_delimeter: The delimeter of the date.
                :return: day: str, month: str, year: str
                """
        # DD_MM_YYYY or D_M_YYYY or DD_MM_YY or D_M_YY
        if date_format == DD_MM_YYYY or date_format == D_M_YYYY or date_format == DD_MM_YY or date_format == D_M_YY:
            day, month, year = date.split(date_delimeter)
            if date_format == DD_MM_YY or date_format == D_M_YY:
                year = str(int(year) + (century-1)*100)
            return day, month, year
        # DD_YYYY_MM or D_YYYY_M or DD_YY_MM or D_YY_M
        elif date_format == DD_YYYY_MM or date_format == D_YYYY_M or date_format == DD_YY_MM or date_format == D_YY_M:
            day, year, month = date.split(date_delimeter)
            if date_format == DD_YY_MM or date_format == D_YY_M:
                year = str(int(year) + (century-1)*100)
            return day, month, year
        # MM_DD_YYYY or M_D_YYYY or MM_DD_YY or M_D_YY
        elif date_format == MM_DD_YYYY or date_format == M_D_YYYY or date_format == MM_DD_YY or date_format == M_D_YY:
            month, day, year = date.split(date_delimeter)
            if date_format == MM_DD_YY or date_format == M_D_YY:
                year = str(int(year) + (century-1)*100)
            return day, month, year
        # MM_YYYY_DD or M_YYYY_D or MM_YY_DD or M_YY_D
        elif date_format == MM_YYYY_DD or date_format == M_YYYY_D or date_format == MM_YY_DD or date_format == M_YY_D:
            month, year, day = date.split(date_delimeter)
            if date_format == MM_YY_DD or date_format == M_YY_D:
                year = str(int(year) + (century-1)*100)
            return day, month, year
        # YYYY_MM_DD or YYYY_M_D or YY_MM_DD or YY_M_D
        elif date_format == YYYY_MM_DD or date_format == YYYY_M_D or date_format == YY_MM_DD or date_format == YY_M_D:
            year, month, day = date.split(date_delimeter)
            if date_format == YY_MM_DD or date_format == YY_M_D:
                year = str(int(year) + (century-1)*100)
            return day, month, year
        # YYYY_DD_MM or YYYY_D_M or YY_DD_MM or YY_D_M
        elif date_format == YYYY_DD_MM or date_format == YYYY_D_M or date_format == YY_DD_MM or date_format == YY_D_M:
            year, day, month = date.split(date_delimeter)
            if date_format == YY_DD_MM or date_format == YY_D_M:
                year = str(int(year) + (century-1)*100)
            return day, month, year

    def change_date_format_in_list(self, list_event: [], date_format_from: str, date_format_to: str,
                                   date_delimeter_from=del_slash, date_delimeter_to=del_slash, century=21):
        list_date_new = []
        for event in list_event:
            day, month, year = self.date_break_to_day_month_year(date=event[0], date_format=date_format_from,
                                                                 date_delimeter=date_delimeter_from, century=century)

            date_tmp = self.create_date_format(day=day, month=month, year=year,
                                               date_format=date_format_to, date_delimeter=date_delimeter_to)
            event[0] = date_tmp
            list_date_new.append(event)

        return list_date_new

    def create_date_format(self, day: str, month: str, year: str, date_format=DD_MM_YYYY, date_delimeter=del_slash):
        """
        Check the format of the day (eg DD/MM/YYYY) and returns a string.
        :param day: The day of the date.
        :param month: The month of the date.
        :param year: The year of the date.
        :param date_format: The date format. Can be: DD_MM_YYYY
                                                     DD_YYYY_MM
                                                     MM_DD_YYYY
                                                     MM_YYYY_DD
                                                     YYYY_MM_DD
                                                     YYYY_DD_MM
                                                     D_M_YYYY
                                                     D_YYYY_M
                                                     M_D_YYYY
                                                     M_YYYY_D
                                                     YYYY_M_D
                                                     YYYY_D_M
                                                     DD_MM_YY
                                                     DD_YY_MM
                                                     MM_DD_YY
                                                     MM_YY_DD
                                                     YY_MM_DD
                                                     YY_DD_MM
                                                     D_M_YY
                                                     D_YY_M
                                                     M_D_YY
                                                     M_YY_D
                                                     YY_M_D
                                                     YY_D_M

        :param date_delimeter: The delimeter of the date.
        :return: A date string.
        """
        # DD_MM_YYYY
        if date_format == DD_MM_YYYY:
            day, month = self.change_day_month_to_double_format(day, month)
            return day + date_delimeter + month + date_delimeter + year
        # DD_YYYY_MM
        elif date_format == DD_YYYY_MM:
            day, month = self.change_day_month_to_double_format(day, month)
            return day + date_delimeter + year + date_delimeter + month
        # MM_DD_YYYY
        elif date_format == MM_DD_YYYY:
            day, month = self.change_day_month_to_double_format(day, month)
            return month + date_delimeter + day + date_delimeter + year
        # MM_YYYY_DD
        elif date_format == MM_YYYY_DD:
            day, month = self.change_day_month_to_double_format(day, month)
            return month + date_delimeter + year + date_delimeter + day
        # YYYY_MM_DD
        elif date_format == YYYY_MM_DD:
            day, month = self.change_day_month_to_double_format(day, month)
            return year + date_delimeter + month + date_delimeter + day
        # YYYY_DD_MM
        elif date_format == YYYY_DD_MM:
            day, month = self.change_day_month_to_double_format(day, month)
            return year + date_delimeter + day + date_delimeter + month

        # D_M_YYYY
        elif date_format == D_M_YYYY:
            day, month = self.change_day_month_to_single_format(day, month)
            return day + date_delimeter + month + date_delimeter + year
        # D_YYYY_M
        elif date_format == D_YYYY_M:
            day, month = self.change_day_month_to_single_format(day, month)
            return day + date_delimeter + year + date_delimeter + month
        # M_D_YYYY
        elif date_format == M_D_YYYY:
            day, month = self.change_day_month_to_single_format(day, month)
            return month + date_delimeter + day + date_delimeter + year
        # M_YYYY_D
        elif date_format == M_YYYY_D:
            day, month = self.change_day_month_to_single_format(day, month)
            return month + date_delimeter + year + date_delimeter + day
        # YYYY_M_D
        elif date_format == YYYY_M_D:
            day, month = self.change_day_month_to_single_format(day, month)
            return year + date_delimeter + month + date_delimeter + day
        # YYYY_D_M
        elif date_format == YYYY_D_M:
            day, month = self.change_day_month_to_single_format(day, month)
            return year + date_delimeter + day + date_delimeter + month

        # DD_MM_YY
        if date_format == DD_MM_YY:
            day, month = self.change_day_month_to_double_format(day, month)
            return day + date_delimeter + month + date_delimeter + str(int(year) % 100)
        # DD_YY_MM
        elif date_format == DD_YY_MM:
            day, month = self.change_day_month_to_double_format(day, month)
            return day + date_delimeter + str(int(year) % 100) + date_delimeter + month
        # MM_DD_YY
        elif date_format == MM_DD_YY:
            day, month = self.change_day_month_to_double_format(day, month)
            return month + date_delimeter + day + date_delimeter + str(int(year) % 100)
        # MM_YY_DD
        elif date_format == MM_YY_DD:
            day, month = self.change_day_month_to_double_format(day, month)
            return month + date_delimeter + str(int(year) % 100) + date_delimeter + day
        # YY_MM_DD
        elif date_format == YY_MM_DD:
            day, month = self.change_day_month_to_double_format(day, month)
            return str(int(year) % 100) + date_delimeter + month + date_delimeter + day
        # YY_DD_MM
        elif date_format == YY_DD_MM:
            day, month = self.change_day_month_to_double_format(day, month)
            return str(int(year) % 100) + date_delimeter + day + date_delimeter + month

        # D_M_YY
        elif date_format == D_M_YY:
            day, month = self.change_day_month_to_single_format(day, month)
            return day + date_delimeter + month + date_delimeter + str(int(year) % 100)
        # D_YY_M
        elif date_format == D_YY_M:
            day, month = self.change_day_month_to_single_format(day, month)
            return day + date_delimeter + str(int(year) % 100) + date_delimeter + month
        # M_D_YY
        elif date_format == M_D_YY:
            day, month = self.change_day_month_to_single_format(day, month)
            return month + date_delimeter + day + date_delimeter + str(int(year) % 100)
        # M_YY_D
        elif date_format == M_YY_D:
            day, month = self.change_day_month_to_single_format(day, month)
            return month + date_delimeter + str(int(year) % 100) + date_delimeter + day
        # YY_M_D
        elif date_format == YY_M_D:
            day, month = self.change_day_month_to_single_format(day, month)
            return str(int(year) % 100) + date_delimeter + month + date_delimeter + day
        # YY_D_M
        elif date_format == YY_D_M:
            day, month = self.change_day_month_to_single_format(day, month)
            return str(int(year) % 100) + date_delimeter + day + date_delimeter + month

    def calendar_print(self):
        """
        Print the calendar.
        :return: Nothing
        """
        for date in self.dict_calendar.keys():
            print(date)
            for time in self.dict_calendar[date].keys():
                print(time)

    def calendar_print_and_return_in_range(self, month_start=1, day_start=0, month_end=12, day_end=31,
                                           bool_print=False):
        """
        Print the calendar.
        :return: np.array
        """
        calendar = []

        if month_start < 0 or month_start > 11:
            warnings.warn("Start month out of range (0, 11). Set it to default value '0'.")
            month_start = 0
        if month_end < 0 or month_end > 11:
            warnings.warn("Start month out of range (0, 11). Set it to default value '11'.")
            month_end = 11

        if self.isLeap():
            # If leap is True
            if day_start < 0 or day_start > int_month_days_leap[month_start]:
                warn = "Start day out of range (0," + str(int_month_days_leap[month_start]) \
                       + "). Set it to default value '0'."
                warnings.warn(warn)
                day_start = 0
            if day_end < 0 or day_end > int_month_days_leap[month_end]:
                warn = "End day out of range (0," + str(int_month_days_leap[month_end]) \
                       + "). Set it to default value '" + str(int_month_days_leap[month_end]) + "'."
                warnings.warn(warn)
                day_end = int_month_days_leap[month_end]

            for month in range(month_start, month_end + 1):
                # If the month is the same with the month start then don't start the day from 01, but from the
                # day the user wants
                if month == month_start:
                    for day in range(day_start, int_month_days_leap[month]):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)

                # The same logic as the month is month start applies to the month end.
                elif month == month_end:
                    for day in range(0, day_end):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)

                # For all middle months iterate from start to end of the month
                else:
                    for day in range(0, int_month_days_leap[month]):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)

            else:
                # If the month is the same, then do the for loop for the days
                month = month_start
                for day in range(day_start, day_end):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    for time in self.list_timespamp:
                        calendar_tmp = [date_tmp, time]
                        for event in self.dict_calendar[date_tmp][time].keys():
                            calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                        calendar.append(calendar_tmp)
        else:
            # If leap is not True
            if day_start < 0 or day_start > int_month_days_not_leap[month_start]:
                warn = "Start day out of range (0," + str(int_month_days_leap[month_start]) \
                       + "). Set it to default value '0'."
                warnings.warn(warn)
                day_start = 0
            if day_end < 0 or day_end > int_month_days_not_leap[month_end]:
                warn = "End day out of range (0," + str(int_month_days_leap[month_end]) \
                       + "). Set it to default value '" + str(int_month_days_leap[month_end]) + "'."
                warnings.warn(warn)
                day_end = int_month_days_leap[month_end]

            for month in range(month_start, month_end + 1):
                # If the month is the same with the month start then don't start the day from 01, but from the
                # day the user wants
                if month == month_start:
                    for day in range(day_start, int_month_days_not_leap[month]):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)

                # The same logic as the month is month start applies to the month end.
                elif month == month_end:
                    for day in range(0, day_end):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)

                # For all middle months iterate from start to end of the month
                else:
                    for day in range(0, int_month_days_not_leap[month]):
                        date_tmp = self.create_date_format(day=str_id_days[day],
                                                           month=str_id_months[month],
                                                           year=str(self.year),
                                                           date_format=self.date_format,
                                                           date_delimeter=self.date_delimeter)
                        for time in self.list_timespamp:
                            calendar_tmp = [date_tmp, time]
                            for event in self.dict_calendar[date_tmp][time].keys():
                                calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                            calendar.append(calendar_tmp)
            else:
                # If the month is the same, then do the for loop for the days
                month = month_start
                for day in range(day_start, day_end):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    for time in self.list_timespamp:
                        calendar_tmp = [date_tmp, time]
                        for event in self.dict_calendar[date_tmp][time].keys():
                            calendar_tmp.append(self.dict_calendar[date_tmp][time][event])
                        calendar.append(calendar_tmp)

        if bool_print:
            for cal in calendar:
                print(cal)

        return calendar

    def create(self, date_format=DD_MM_YYYY, date_delimeter=del_slash,
               hour_start=0, hour_end=24, hour_step=1, minute_start=0, minute_end=60, minute_step=0):
        """
        Calendar Creation.
        :param date_format: The date format. Can be: DD_MM_YYYY
                                                     DD_YYYY_MM
                                                     MM_DD_YYYY
                                                     MM_YYYY_DD
                                                     YYYY_MM_DD
                                                     YYYY_DD_MM
        :param date_delimeter: The delimeter of the date.
        :param hour_start: The starting hour.
        :param hour_end: The ending hour.
        :param hour_step: The step of the hours.
        :param minute_start: The start of the minutes.
        :param minute_end: The end of the minutes.
        :param minute_step: The step of the minutes.
        :return: Nothing
        """
        self.date_format = date_format
        self.date_delimeter = date_delimeter
        list_timestamp, int_list_size = self.set_time(hour_start=hour_start,
                                                      hour_end=hour_end,
                                                      hour_step=hour_step,
                                                      minute_start=minute_start,
                                                      minute_end=minute_end,
                                                      minute_step=minute_step)

        self.list_timespamp = list_timestamp
        self.int_list_size = int_list_size

        if self.leap:
            for month in range(0, 12):
                for day in range(0, int_month_days_leap[month]):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    self.dict_calendar[date_tmp] = {}
                    for timestamp in self.list_timespamp:
                        self.dict_calendar[date_tmp][timestamp] = {}

        else:
            for month in range(0, 12):
                for day in range(0, int_month_days_not_leap[month]):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    # print(date_tmp)
                    self.dict_calendar[date_tmp] = {}
                    for timestamp in self.list_timespamp:
                        self.dict_calendar[date_tmp][timestamp] = {}

    def add_default_events_in_range(self, event_list, no_data_value=None, month_start=1, day_start=0,
                                    month_end=12, day_end=31):
        """
        Add an event.
        :param event_list: The name of the event.
        :param no_data_value: Set no data value. This needed, if the event is a range of numerical values.
        :param month_start: The month start (for the range month)
        :param day_start: The day start (for the range day)
        :param month_end: The month end (for the range month)
        :param day_end: The day end (for the range month)
        :return: Nothing
        """
        if month_start < 0 or month_start > 11:
            warnings.warn("Start month out of range (0, 11). Set it to default value '0'.")
            month_start = 0
        if month_end < 0 or month_end > 11:
            warnings.warn("Start month out of range (0, 11). Set it to default value '11'.")
            month_end = 11

        if self.isLeap():
            # If leap is True
            if day_start < 0 or day_start > int_month_days_leap[month_start]:
                warn = "Start day out of range (0," + str(int_month_days_leap[month_start]) \
                       + "). Set it to default value '0'."
                warnings.warn(warn)
                day_start = 0
            if day_end < 0 or day_end > int_month_days_leap[month_end]:
                warn = "End day out of range (0," + str(int_month_days_leap[month_end]) \
                       + "). Set it to default value '" + str(int_month_days_leap[month_end]) + "'."
                warnings.warn(warn)
                day_end = int_month_days_leap[month_end]

            if month_start != month_end:
                # If the month is not the same, then do the nested for loops
                for month in range(month_start, month_end + 1):
                    # If the month is the same with the month start then don't start the day from 01, but from the
                    # day the user wants
                    if month == month_start:
                        for day in range(day_start, int_month_days_leap[month]):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value

                    # The same logic as the month is month start applies to the month end.
                    elif month == month_end:
                        for day in range(0, day_end):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value

                    # For all middle months iterate from start to end of the month
                    else:
                        for day in range(0, int_month_days_leap[month]):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value
            else:
                # If the month is the same, then do the for loop for the days
                month = month_start
                for day in range(day_start, day_end):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    for time in self.list_timespamp:
                        for event in event_list:
                            self.dict_calendar[date_tmp][time][event] = no_data_value
        else:
            # If leap is not True
            if day_start < 0 or day_start > int_month_days_not_leap[month_start]:
                warn = "Start day out of range (0," + str(int_month_days_leap[month_start]) \
                       + "). Set it to default value '0'."
                warnings.warn(warn)
                day_start = 0
            if day_end < 0 or day_end > int_month_days_not_leap[month_end]:
                warn = "End day out of range (0," + str(int_month_days_leap[month_end]) \
                       + "). Set it to default value '" + str(int_month_days_leap[month_end]) + "'."
                warnings.warn(warn)
                day_end = int_month_days_leap[month_end]

            # If the month is not the same, then do the nested for loops
            if month_start != month_end:
                for month in range(month_start, month_end + 1):
                    # If the month is the same with the month start then don't start the day from 01, but from the
                    # day the user wants
                    if month == month_start:
                        for day in range(day_start, int_month_days_not_leap[month]):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value
                    # If the month is the same, then do the for loop for the days
                    elif month == month_end:
                        for day in range(0, day_end):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value

                    else:
                        # For all middle months iterate from start to end of the month
                        for day in range(0, int_month_days_not_leap[month]):
                            date_tmp = self.create_date_format(day=str_id_days[day],
                                                               month=str_id_months[month],
                                                               year=str(self.year),
                                                               date_format=self.date_format,
                                                               date_delimeter=self.date_delimeter)
                            for time in self.list_timespamp:
                                for event in event_list:
                                    self.dict_calendar[date_tmp][time][event] = no_data_value
            else:
                # If the month is the same, then do the for loop for the days
                month = month_start
                for day in range(day_start, day_end):
                    date_tmp = self.create_date_format(day=str_id_days[day],
                                                       month=str_id_months[month],
                                                       year=str(self.year),
                                                       date_format=self.date_format,
                                                       date_delimeter=self.date_delimeter)
                    for time in self.list_timespamp:
                        for event in event_list:
                            self.dict_calendar[date_tmp][time][event] = no_data_value

    def add_values_for_event_from_list(self, event_name: str, event_list: []):
        for event in event_list:
            self.dict_calendar[event[0]][event[1]][event_name] = event[2]
