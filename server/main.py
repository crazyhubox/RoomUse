from server import Server
import datetime
import argparse

def get_week_day():
    d=datetime.datetime.now()
    return d.weekday() + 1


parser = argparse.ArgumentParser()
parser.add_argument('-d','--day',default=get_week_day())
parser.add_argument('-c','--command',default=None)


def main():
    args = parser.parse_args()
    command=  args.command
    day = int(args.day)
    server = Server()
    server.Select(command,day)


if __name__ == '__main__':
    main()
