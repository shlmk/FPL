import xlsxwriter

def write_section(worksheet, start_row, section_name, data, sheet_name, cell_format):
  teams = sorted(data.keys())
  columns = ['Week ' + str(num) for num in range(1,39)]
  columns.insert(0, 'Teams')

  worksheet.write(start_row, 0, section_name, cell_format)    # Header (e.g. Win/Lose/Draw)
  worksheet.write_row(1+start_row, 0, columns, cell_format)   # Column Names
  worksheet.write_column(2+start_row, 0, teams, cell_format)  # Team names (rows)

  for idx, team in enumerate(teams):
    worksheet.write_row(2+idx+start_row, 1, data[team][sheet_name])

def write_worksheet(workbook, data, sheet_name, stats):
  worksheet = workbook.add_worksheet(sheet_name)
  num_of_teams = len(data.keys())
  bold = workbook.add_format({'bold': True})
  #Note: rows and colums are zero indexed [A1] = (0, 0)
  for idx, stat in enumerate(stats):
    write_section(worksheet, idx * (num_of_teams + 3), stat, data, sheet_name,
                bold)
                
def create_spreadsheet(spreadsheet_name, data, desired_sheets='all'):
  stats = ['Win/Draw/Lose', 'Goals Conceded', 'Goals Scored']

  if (desired_sheets!= 'all' and desired_sheets != 'opponents' and desired_sheets!= 'difficulty'):
    raise ValueError('Wrong value for wookbook -- must be all, opponents, or difficulty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name)

  if desired_sheets == 'all' or desired_sheets == 'opponents':
    write_worksheet(workbook, data, 'opponents', stats)

  if desired_sheets == 'all' or desired_sheets == 'difficulty':
    write_worksheet(workbook, data, 'difficulty', stats)

  workbook.close()
