import caldav
import getpass

from os import chdir, getcwd, listdir
from os.path import isdir, join
from sys import exit

EXPORT_FOLDER_PREFIX = 'ical_export'
CAL_NAME_FILE = 'calendar_name.txt'

def main():
    client = caldav.DAVClient(
        url=input('URL: '),
        username=input('Username: '),
        password=getpass.getpass(prompt='Password: ')
    )

    try:
        principal = client.principal()
        available_calendars = {cal.name: cal for cal in principal.calendars()}
    except caldav.lib.error.AuthorizationError:
        print('Invalid URL or credentials.')
        exit(1)
    
    parent_folder = getcwd()
    for path in listdir():
        if not (path.startswith(EXPORT_FOLDER_PREFIX) and isdir(path)):
            continue
        
        chdir(join(parent_folder, path))
        try:
            with open(CAL_NAME_FILE, 'r') as f:
                cal_name = f.readline().strip()
        except FileNotFoundError:
            print(f'Found directory {path} which matches the export folder schema but does not contain a \
                    {CAL_NAME_FILE} file.')
            continue
        
        print(f'Importing calendar \'{cal_name}\'...')
        calendar = available_calendars.get(cal_name, principal.make_calendar(cal_name))
        
        count = len(listdir())
        for i, path in enumerate(listdir()):
            if path.endswith('.ics'):
                with open(path, 'r') as f:
                    calendar.save_event(''.join(f.readlines()))
            print(f'\t{i}/{count}', end='\r')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted.')
        exit(1)