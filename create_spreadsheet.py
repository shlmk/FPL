import xlsxwriter

def create_spreadsheet(spreadsheet_name, data, desired_sheets='All'):

def create_spreadsheet(spreadsheet_name, data, desired_sheets='all'):

  if (desired_sheets!= 'all' and desired_sheets != 'opponents' and desired_sheets!= 'diffculty'):
    raise ValueError('Wrong value for wookbook -- must be ALL, Fixtures, or Diffculty!')

  workbook = xlsxwriter.Workbook(spreadsheet_name+'.xlsx')

  if desired_sheets == 'all' or desired_sheets == 'opponents':
    worksheet = workbook.add_worksheet('opponents')

  if desired_sheets == 'all' or desired_sheets == 'difficulty':
    worksheet = workbook.add_worksheet('difficulty')

  workbook.close()
