import lib.my_calendar as cal
import pandas as pd
import numpy as np

# Read the data
path_Athens = 'data/Athens2020_from_8_to_11.csv'
path_Brest = 'data/Brest2020_from_8_to_11.csv'
path_Madrid = 'data/Madrid2020_from_8_to_11.csv'
path_Vienna = 'data/Vienna2020_from_8_to_11.csv'

# Create the output CSV informations
csv_header = ['Date', 'Time', 'Athens_Temp', 'Brest_Temp', 'Madrid_Temp', 'Vienna_Temp']
dataset_names = ['Athens_Temp', 'Brest_Temp', 'Madrid_Temp', 'Vienna_Temp']
dataset_month_range = [6, 10]
dataset_day_range = [30, 30]
no_data_value = None

list_Athens_2020 = cal.read_csv(path_Athens)
list_Brest_2020 = cal.read_csv(path_Brest)
list_Madrid_2020 = cal.read_csv(path_Madrid)
list_Vienna_2020 = cal.read_csv(path_Vienna)

# Calendar Creation for the year of 2020 and add default event values
temp_cal_2020 = cal.Calendar(year=2020)
temp_cal_2020.create(date_format=cal.MM_DD_YYYY, date_delimeter=cal.del_slash,
                     hour_start=0, hour_end=24, hour_step=1, minute_start=0, minute_end=60, minute_step=0)
temp_cal_2020.add_default_events_in_range(event_list=dataset_names, no_data_value=no_data_value,
                                          month_start=dataset_month_range[0], month_end=dataset_month_range[1],
                                          day_start=dataset_day_range[0], day_end=dataset_day_range[1])
# Change the Brest_2020 date format to be the same as calenda's.
list_Brest_2020 = temp_cal_2020.change_date_format_in_list(list_event=list_Brest_2020,
                                                           date_format_from=cal.MM_DD_YY,
                                                           date_format_to=cal.MM_DD_YYYY,
                                                           date_delimeter_from=cal.del_slash,
                                                           date_delimeter_to=cal.del_slash,
                                                           century=21)
# Add events to calendar
temp_cal_2020.add_values_for_event_from_list(event_name=dataset_names[0], event_list=list_Athens_2020)
temp_cal_2020.add_values_for_event_from_list(event_name=dataset_names[1], event_list=list_Brest_2020)
temp_cal_2020.add_values_for_event_from_list(event_name=dataset_names[2], event_list=list_Madrid_2020)
temp_cal_2020.add_values_for_event_from_list(event_name=dataset_names[3], event_list=list_Vienna_2020)

# temp_cal.calendar_print()
cal_list_2020 = [csv_header]
cal_list_tmp = temp_cal_2020.calendar_print_and_return_in_range(month_start=dataset_month_range[0],
                                                                month_end=dataset_month_range[1],
                                                                day_start=dataset_day_range[0],
                                                                day_end=dataset_day_range[1],
                                                                bool_print=False)
for row in cal_list_tmp:
    cal_list_2020.append(row)

cal.write_csv(path='export_dir/Temperatures_2020.csv', list_write=cal_list_2020, delimeter=cal.del_comma)

# for row in cal_list:
#    print(row)

# Interpolate missing values and export them
cal_array = np.array(cal_list_tmp).T
cal_dict_tmp = {}
i = 0
for key in csv_header:
    if key in dataset_names:
        cal_dict_tmp[key] = list(cal_array[i].astype(np.float))
    else:
        cal_dict_tmp[key] = list(cal_array[i])
    i += 1

df = pd.DataFrame(cal_dict_tmp)
df.interpolate(method='linear', limit_direction='both', inplace=True)
print(df)

cal_list_inter = [csv_header]
for row in df.values.tolist():
    cal_list_inter.append(row)
cal.write_csv(path='export_dir/Temperatures_Interpolated_2020.csv', list_write=cal_list_inter, delimeter=cal.del_comma)
