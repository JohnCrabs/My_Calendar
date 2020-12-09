import lib.my_calendar as cal

path_Athens = 'data/Athens2020_from_8_to_11.csv'
path_Brest = 'data/Brest2020_from_8_to_11.csv'
path_Madrid = 'data/Madrid2020_from_8_to_11.csv'
path_Vienna = 'data/Vienna2020_from_8_to_11.csv'

csv_header = ['Date', 'Time', 'Athens_Temp', 'Brest_Temp', 'Madrid_Temp', 'Vienna_Temp']
dataset_names = ['Athens', 'Brest', 'Madrid', 'Vienna']
dataset_month_range = [6, 10]
dataset_day_range = [30, 30]
no_data_value = cal.NaN

list_Athens = cal.read_csv(path_Athens)
list_Brest = cal.read_csv(path_Brest)
list_Madrid = cal.read_csv(path_Madrid)
list_Vienna = cal.read_csv(path_Vienna)

temp_cal = cal.Calendar()
temp_cal.create(date_format=cal.MM_DD_YYYY, date_delimeter=cal.del_slash,
                hour_start=0, hour_end=24, hour_step=1, minute_start=0, minute_end=60, minute_step=0)
temp_cal.add_default_events_in_range(event_list=dataset_names, no_data_value=no_data_value,
                                     month_start=dataset_month_range[0], month_end=dataset_month_range[1],
                                     day_start=dataset_day_range[0], day_end=dataset_day_range[1])

list_Brest = temp_cal.change_date_format_in_list(list_event=list_Brest,
                                                 date_format_from=cal.MM_DD_YY, date_format_to=cal.MM_DD_YYYY,
                                                 date_delimeter_from=cal.del_slash, date_delimeter_to=cal.del_slash,
                                                 century=21)

temp_cal.add_values_for_event_from_list(event_name=dataset_names[0], event_list=list_Athens)
temp_cal.add_values_for_event_from_list(event_name=dataset_names[1], event_list=list_Brest)
temp_cal.add_values_for_event_from_list(event_name=dataset_names[2], event_list=list_Madrid)
temp_cal.add_values_for_event_from_list(event_name=dataset_names[3], event_list=list_Vienna)

# temp_cal.calendar_print()
cal_list = [csv_header]
cal_list_tmp = temp_cal.calendar_print_and_return_in_range(month_start=dataset_month_range[0],
                                                           month_end=dataset_month_range[1],
                                                           day_start=dataset_day_range[0],
                                                           day_end=dataset_day_range[1],
                                                           bool_print=False)
for row in cal_list_tmp:
    cal_list.append(row)

cal.write_csv(path='export_dir/Temperatures.csv', list_write=cal_list, delimeter=cal.del_comma)

for row in cal_list:
    print(row)
