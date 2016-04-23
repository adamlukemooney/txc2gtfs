# txc2gtfs

This is eventually intended to be a full conversion tool to transform
TransXChange public transport data to GTFS files. It is not ready
for general use yet, as it is in the early development stages.

You need Python 2.7 to run this program.

## How to run

1. Clone the repository
2. In your local copy, create an empty folder called `output`
3. Create a folder called `input` containing the input TransXChange XML files
4. Run `$ python main.py`

## Current implementation

The current implementation can extract all mandatory elements of a GTFS dataset
except for the calendar, which is coming soon.