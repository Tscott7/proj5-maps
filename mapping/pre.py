"""
Pre-process a map file. 

"""
import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

def process(raw):
    """
    Line by line processing of map file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment and skipped. 
    """
    field = None
    entry = {}
    cooked = []
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            log.debug("Skipping")
            continue
        parts = line.split(':')
        Latitude = parts[1]
        Longitude = parts[3]
        Description = str(parts[5])
        Latitude2 = parts[7]
        Longitude2 = parts[9]
        Description2 = parts[11]
        Latitude3 = parts[13]
        Longitude3 = parts[15]
        Description3 = parts[17]

        entry['Latitude'] = Latitude
        entry['Longitude'] = Longitude
        entry['Description'] = Description
        entry['Latitude2'] = Latitude2
        entry['Longitude2'] = Longitude2
        entry['Description2'] = Description2
        entry['Latitude3'] = Latitude3
        entry['Longitude3'] = Longitude3
        entry['Description3'] = Description3

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("data/markers.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
