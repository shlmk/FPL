import xlsxwriter

def create_spreadsheet(spreadsheet_name, data, desired_sheets='All'):

  if (desired_sheets!= 'All' and desired_sheets != 'Fixtures' and desired_sheets!= 'Diffculty'):
    raise ValueError('Wrong value for wookbook -- must be ALL, Fixtures, or Diffculty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name+'.xlsx')

  if desired_sheets == 'ALL' or desired_sheets == 'Fixtures':
    worksheet = workbook.add_worksheet('Fixtures')

  if desired_sheets == 'ALL' or desired_sheets == 'Difficulty':
    worksheet = workbook.add_worksheet('Diffculty')

  workbook.close()
