import xlsxwriter

#TODO: Need to move workbook into write_worksheet to be able to do formatting!

def write_section(wksheet, start_row, section_name, data, sheet):
  columns = ['Week ' + str(num) for num in range(1,39)]
  columns.insert(0, 'Teams')

  teams = sorted(data.keys())

  wksheet.write(start_row, 0, section_name, bold)    # Header (e.g. Win/Lose/Draw)
  wksheet.write_row(1+start_row, 0, columns, bold)   # Column Names
  wksheet.write_column(2+start_row, 0, teams, bold)  # Team names (rows)

  for idx, team in enumerate(teams):
    wksheet.write_row(2+idx+start_row, 1, data[team][sheet])

def write_worksheet(wksheet, data, sheet, stats):
  num_of_teams = len(data.keys())

  # Note: rows and columns are zero indexed! (A1 = 0)
  for idx, stat in enumerate(stats):
    write_section(wksheet, idx * (num_of_teams + 3), stat, data, sheet)

def create_spreadsheet(spreadsheet_name, data, desired_sheets='all'):
  stats = ['Win/Draw/Lose', 'Goals Conceded', 'Goals Scored']

  if (desired_sheets!= 'all' and desired_sheets != 'opponents' and desired_sheets!= 'difficulty'):
    raise ValueError('Wrong value for wookbook -- must be all, opponents, or difficulty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name)

  if desired_sheets == 'all' or desired_sheets == 'opponents':
    worksheet = workbook.add_worksheet('opponents')
    write_worksheet(worksheet, data, 'opponents', stats)

  if desired_sheets == 'all' or desired_sheets == 'difficulty':
    worksheet = workbook.add_worksheet('difficulty')
    write_worksheet(worksheet, data, 'difficulty', stats)

  workbook.close()
