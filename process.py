# process.py  05/11/2016  D.J.Whale
#
# Process a log file
# eventually this will be done on the fly
# It's good enough for now to turn already captured data into Excel form.

def from_csv(line):
    return line.split(',')


def to_csv(*args):
    result = ""
    for arg in args:
        if result != "":
            result += ','
        result += str(arg)
    return result


def main(in_name):
    speed = 0
    rpm = 0
    temp = 0

    with open(in_name) as f:
        while True:
            line = f.readline()
            if line == "": break # EOF
            line = line.strip() # strip nl
            #print("line:%s" % line)
            data = from_csv(line)
            type, value = data[0], data[1] # unpack

            if type == "SPEED":
                speed = int(value)
            elif type == "RPM":
                rpm = int(value)
            elif type == "TEMP":
                temp = int(value)
            else:
                pass # ignore unknown records

            print to_csv(rpm, temp, speed)

if __name__ == "__main__":
    import sys
    in_name = sys.argv[1]
    main(in_name)

# END