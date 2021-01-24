from caldav import DAVClient
from caldav.lib.error import AuthorizationError
from datetime import date, datetime
from dotenv import load_dotenv
from getpass import getpass
from os import getenv, mkdir
from os.path import isdir, join
from sys import exit


EXPORT_FOLDER_PREFIX = 'ical_export'
CAL_NAME_FILE        = 'calendar_name.txt'
URL_ENV   = 'CALENDAR_URL'
USER_ENV  = 'CALENDAR_USER'
PASS_ENV  = 'CALENDAR_PASS'
START_ENV = 'CALENDAR_START'
END_ENV   = 'CALENDAR_END'


def main():
    url      = getenv(URL_ENV)
    username = getenv(USER_ENV)
    password = getenv(PASS_ENV)

    if url is None:
        url = input('URL: ')
    if username is None:
        username = input('Username: ')
    if password is None:
        password = getpass(prompt='Password: ')

    client = DAVClient(
        url=url,
        username=username,
        password=password
    )

    try:
        principal = client.principal()
    except AuthorizationError:
        print('Invalid URL or credentials.')
        exit(1)

    start = getenv(START_ENV)
    end   = getenv(END_ENV)
    try:
        start = datetime.fromisoformat(start)
        end   = datetime.fromisoformat(end)
    except ValueError:
        print(f'Invalid {START_ENV} or {END_ENV} value.')
        exit(1)

    if start is None:
        default_start = datetime(date.today().year,     1, 1)
        start = timeinput(
            f'Start time [{default_start.strftime("%Y-%m-%d %H:%M")}]: ',
            default_start
        )
    if end is None:
        default_end   = datetime(date.today().year + 1, 1, 1)
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
        load_dotenv()
        main()
    except KeyboardInterrupt:
        print('\nInterrupted.')
        exit(1)
