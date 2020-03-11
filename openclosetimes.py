start_time = int(input('input start time (next 2pm wednesday)\n'))
num_weeks = int(input('input number of weeks to go back\n'))
curr_time = start_time
for _ in range(num_weeks):
  print('epoch range: %d-%d' %(curr_time - 604800, curr_time - 7200))
  curr_time -= 604800


