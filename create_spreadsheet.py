import xlsxwriter

'''
  Helper function that writes a particular section of a worksheet, including the
  relevant information for all twenty teams as well as some basic formatting.
  @param    worksheet       The worksheet object (part of xlsxwriter)
  @param    sheet_name      The name of the worksheet (str)
  @param    section_name    The name of the section (str)
  @param    start_row       The start row to begin writing the data
  @param    cell_format     The formatting to use for headers
  @param    data            The relevant data
'''
def write_section(worksheet, sheet_name, section_name, start_row, cell_format, data):
  teams = sorted(data.keys())
  columns = ['Week ' + str(num) for num in range(1,39)]
  columns.insert(0, 'Teams')

  worksheet.write(start_row, 0, section_name, cell_format)    # Header (e.g. Win/Lose/Draw)
  worksheet.write_row(1+start_row, 0, columns, cell_format)   # Column Names
  worksheet.write_column(2+start_row, 0, teams, cell_format)  # Team names (rows)

  for idx, team in enumerate(teams):
    worksheet.write_row(2+idx+start_row, 1, data[team][sheet_name])

'''
  Helper function that writes a worksheet within a workbook. Not directly accessible.
  Instead is called by create_spreadsheet method
  @param    workbook       The workbook object (part of xlswriter)
  @param    sheet_name     The name of the worksheet
  @data     data           The relevant data
  @stats    stats          The stats (e.g Wins/Lose/Draw) that is being recorded
'''
def write_worksheet(workbook, sheet_name, data, stats):
  worksheet = workbook.add_worksheet(sheet_name)
  num_of_teams = len(data.keys())
  bold = workbook.add_format({'bold': True})
  #Note: rows and colums are zero indexed [A1] = (0, 0)
  for idx, stat in enumerate(stats):
    write_section(worksheet, idx * (num_of_teams + 3), stat, data, sheet_name,
                bold)

'''
  Function that creates Premier League fixture/difficulty spreadsheet. Called by
  the fixture_spreadsheet_generator script.
  @param   spreadsheet_name    The name of the spreadsheet that will be created
  @param   data                The data that contains the relevant fixture information
  @param   desired_sheets      The sheets to be included in the spreadsheet
'''
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
