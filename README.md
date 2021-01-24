# caldav-export
Python scripts to export all `.ics` files from a CalDAV server in a specified time range and re-import them (e. g. on a different server).

## Dependencies
See `requirements.txt`.

Requires a recent python version (probably 3.6 or higher).

## Usage
Just run `python export.py` / `python import.py`.

If you don't want to be prompted for e. g. the calendar URL, create
a `.env` file containing one or more of the following variables:
* `CALENDAR_URL` - the URL of the calendar
* `CALENDAR_USER` - the username for the calendar
* `CALENDAR_PASS` - the password for the calendar
* `CALENDAR_START` - the start date and time for the export in ISO format *(only for export)*
* `CALENDAR_END` - the end date and time for the export in ISO format *(only for export)*

You will then only be prompted for the variables which aren't set.

## License
See `LICENSE.txt`.

---

Copyright (c) 2021 Max von Forell
