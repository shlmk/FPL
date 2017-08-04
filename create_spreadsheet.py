import xlsxwriter

#TODO: Need to move workbook into write_worksheet to be able to do formatting!

def write_section(wksheet, start_row, start_col, section_name, data, sheet):
  columns = ['Week ' + str(num) for num in range(1,39)]
  columns.insert(0, 'Teams')
  teams = sorted(data.keys())

  wksheet.write(start_row, start_col, section_name)    # Header (e.g. Win/Lose/Draw)
  wksheet.write_row(1+start_row, start_col, columns)   # Column Names
  wksheet.write_column(2+start_row, start_col, teams)  # Team names (rows)

  for idx, team in enumerate(teams):
    wksheet.write_row(2+idx+start_row, start_col+1, data[team][sheet])

def write_worksheet(wksheet, data, sheet, stats):

  num_of_teams = len(data.keys())

  for idx, stat in enumerate(stats):
    write_section(wksheet, idx * (num_of_teams + 3), 0, stat, data, sheet)

def create_spreadsheet(spreadsheet_name, data, desired_sheets='all'):

  stats = ['Win/Draw/Lose', 'Goals Conceded', 'Goals Scored']

  if (desired_sheets!= 'all' and desired_sheets != 'opponents' and desired_sheets!= 'diffculty'):
    raise ValueError('Wrong value for wookbook -- must be all, opponents, or diffculty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name)

  if desired_sheets == 'all' or desired_sheets == 'opponents':
    worksheet = workbook.add_worksheet('opponents')
    write_worksheet(worksheet, data, 'opponents', stats)

  if desired_sheets == 'all' or desired_sheets == 'difficulty':
    worksheet = workbook.add_worksheet('difficulty')
    write_worksheet(worksheet, data, 'difficulty', stats)

  workbook.close()
