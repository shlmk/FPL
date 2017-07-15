import xlsxwriter

def write_worksheet(wksheet, data, sheet):
  columns = ['Week ' + str(num) for num in range(1,39)]
  columns.insert(0, 'Teams')

  wksheet.write_row(0,0, columns)

  teams = sorted(data.keys())
  wksheet.write_column(1, 0, teams)                           # Win Lose Draw
  wksheet.write_column(1 + len(teams) + 1, 0, teams)          # Number of Goals Conceded
  wksheet.write_column(1 + 2 * (len(teams) + 1), 0, teams)    # Number of Goals Scored

def create_spreadsheet(spreadsheet_name, data, desired_sheets='all'):

  if (desired_sheets!= 'all' and desired_sheets != 'opponents' and desired_sheets!= 'diffculty'):
    raise ValueError('Wrong value for wookbook -- must be ALL, Fixtures, or Diffculty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name+'.xlsx')

  if desired_sheets == 'all' or desired_sheets == 'opponents':
    worksheet = workbook.add_worksheet('opponents')

  if desired_sheets == 'all' or desired_sheets == 'difficulty':
    worksheet = workbook.add_worksheet('difficulty')

  workbook.close()
