import caldav
import getpass

from datetime import date, datetime
from os import mkdir
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
    except caldav.lib.error.AuthorizationError:
        print('Invalid URL or credentials.')
        exit(1)
    
    print('Please enter the start and end time for filtering.')
    default_start = datetime(date.today().year,     1, 1)
    default_end   = datetime(date.today().year + 1, 1, 1)
    start = timeinput(
        f'Start time [{default_start.strftime("%Y-%m-%d %H:%M")}]: ',
        default_start
    )
    end = timeinput(
        f'End time [{default_end.strftime("%Y-%m-%d %H:%M")}]: ',
        default_end
    )

    for cal in principal.calendars():
        for ev in cal.date_search(start=start, end=end, expand=True): # expand recurring events
            write_event(cal.name, ev)
        with open(join(calendar_folder(cal.name), CAL_NAME_FILE), 'w') as f: # for importing
            f.write(cal.name)
        print(f'Exported events from calendar \'{cal.name}\'.')

def timeinput(prompt, default):
    finished = False
    while not finished:
        user_input = input(prompt)
        try:
            return default if (user_input == '') else datetime.fromisoformat(user_input)
        except ValueError:
            print('Invalid time.')

def write_event(calendar_name, event):
    url = str(event.url)
    filename = url[url.rfind('/') + 1:]
    folder = calendar_folder(calendar_name)
    if not isdir(folder):
        mkdir(folder)
    with open(join(folder, filename), 'w') as f:
        f.write(event.data)

def calendar_folder(calendar_name):
    return f'{EXPORT_FOLDER_PREFIX}_{calendar_name.replace(" ", "_")}'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted.')
        exit(1)