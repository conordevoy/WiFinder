import os


def check_path():
    """Procedure to check that path is correct and valid"""

    print('The current working directory is:', os.getcwd())
    path = input('If this is correct, press enter now. \n'
                 'Otherwise, press any key followed by enter.\n')


    if path != '':
        path_choice = input('Please enter the directory to use: \n')
        invalid_path = True

        while invalid_path:
            try:
                os.chdir(path_choice)
                invalid_path = False
            except:
                path_choice = input('Invalid path. Please enter the directory to use: \n')


def set_identifier(df):
    """Procedure to create ID column"""

    df['ID'] = ""

    room_index = df.columns.get_loc("Room")
    date_index = df.columns.get_loc("Date")
    hour_index = df.columns.get_loc("Hour")
    id_index = df.columns.get_loc("ID")

    for row in range(df.shape[0]):
        hour = str(df.iat[row, hour_index])
        date = str(df.iat[row, date_index])
        room = str(df.iat[row, room_index])

        identifier = str(hour + date + room)

        df.iat[row, id_index] = identifier
