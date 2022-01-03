from datetime import timedelta
import csv
import os

#date      = d
#startTime = s
#breakTime = b
#endTime   = e

#d Nov 5 21
#s 09:30
#b 15
#e 10:45

def findTime(line):
    """Converts text to the timedelta object"""
    foundTime = line[1].split(":")
    foundTime = timedelta(hours=int(foundTime[0]),minutes=int(foundTime[1]))
    return foundTime


def readStartEnd(log, line):
    """
    Reads the log line by line from a line starting with s
    to a line starting with e and returns a dict with:
    1. start time
    2. shift length
    """
    startTime = timedelta(hours=0,minutes=0)
    breakLen = timedelta(hours=0,minutes=0)
    endTime = timedelta(hours=0,minutes=0)

    # handles the start of a day
    if(line[0] == "s"):
        i = 0
        startTime = findTime(line)
        # limits the day to 10 starts, breaks, and ends
        while(i < 10):
            line = log.readline().split(" ")
            if(line[0] == "b"):
                breakLen += findTime(line)
            elif(line[0] == "e"):
                endTime = findTime(line)
                break
            i += 1

        # does final calclations before returning the results
        daytotal = (endTime - startTime) - breakLen
        day = {'start':startTime,'total':daytotal}
    return day


def parseLog(fileName):
    """
    Opens log file for reading, determins the day, reads the 
    contents of each day and puts it into its own day in a dict
    """
    log = open(fileName, "r")
    line = log.readline().split(" ")
    days = [{'start':timedelta(hours=0,minutes=0),'end':timedelta(hours=0,minutes=0),'total':timedelta(hours=0,minutes=0)}]
    whichDay = 0
    firstEntry = 0

    # loops through the file until the end signaled by 'x'
    while(line[0] != "x"):
        # handles a new day in the log
        if(line[0] == "d"):
            datestr = line[1] + " " + line[2] + ", " + line[3][:-1]
            days.append({'date':datestr,'start':timedelta(hours=0,minutes=0),'end':timedelta(hours=0,minutes=0),'total':timedelta(hours=0,minutes=0)})
            whichDay += 1
            firstEntry = 0
        # calls the function that reads through the contents of a day
        # enters the contents into the variable containing parsed log
        # file data
        else:
            startTotal = readStartEnd(log, line)
            if firstEntry is 0:
                days[whichDay]['start'] = startTotal['start']
                firstEntry += 1
            days[whichDay]['total'] += startTotal['total']
            days[whichDay]['end'] = startTotal['start'] + startTotal['total']
        line = log.readline().split(" ")
    
    log.close()
    return days


def csvMe(days,outputFileName):
    """
    takes the days data collected from the log file and 
    prints it out in CSV format
    """
    field_names = ['Date','Start', 'End', 'Total']

    # writing CSV data to output file
    with open(outputFileName, 'a+', encoding='utf-8') as file:
        csvwriter = csv.DictWriter(file, field_names)

        # check if size of file is 0 and print header
        if os.stat(outputFileName).st_size == 0:
            csvwriter.writeheader()
        
        print(days)
        for i in days:
            csvwriter.writerow({'Date': i['date'],'Start': i['start'],'End': i['end'],'Total': i['total']})


def printing(days):
    """Prints the printing options and handles each option"""
    while True:
        select = input("1 - Print results to csv file\n2 - List dates with time totals\n3 - List day, shift start, shift end, total time \n4 - Exit\nEnter the options you would like (e.g. 234)\n")

        for opt in str(select):
            #remove void leading day
            tmp = days.pop(0)

            # print to csv
            # Date,Start,End,Total
            # "Nov 4, 21",9:30:00,10:30:00,1:00:00
            if opt == "1":
                outputFileName = input("Name for output file:")
                csvMe(days,outputFileName)

            # list | date   | time  |
            if opt == "2":
                print("| DATE\t\t| TOTAL\t\t|")
                for i in days:
                    print("| {}\t| {}\t|".format(i['date'], i['total']))
                print("\n")

            # list | date    | shift start  | shift end | total time    |
            if opt == "3":
                print("| DATE\t\t| START\t\t| END\t\t| TOTAL\t\t|")

                for i in days:
                    print("| {}\t| {}\t| {}\t| {}\t|".format(i['date'],i['start'],i['end'],i['total']))
                print("\n")
            days.insert(0,tmp)

            if opt == "4":
                select = "4"
        
        if select == "4":
            break


def main():
    """Gets the file name and calls the funciton to parse it"""
    fileName = input("Enter your log file's name:")
    days = parseLog(fileName)
    printing(days)


if __name__=="__main__":
    main()

