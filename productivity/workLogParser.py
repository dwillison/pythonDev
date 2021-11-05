from datetime import timedelta
     
#startTime
#breakTime
#endTime

#s 09:30
#b 15
#e 10:45

def parseLog(fileName):
    log = open(fileName, "r")
    line = log.readline().split(" ")
    totalTime = timedelta(hours=0,minutes=0)

    while(line[0] != "x"):
        startTime = timedelta(hours=0,minutes=0)
        breakLen = timedelta(hours=0,minutes=0)
        endTime = timedelta(hours=0,minutes=0)
        if(line[0] == "s"):
            i = 0
            startTime = line[1].split(":")
            startTime = timedelta(hours=int(startTime[0]),minutes=int(startTime[1]))
            while(i < 10):
                line = log.readline().split(" ")
                if(line[0] == "b"):
                    breaktime = line[1].split(":")
                    breaktime = timedelta(hours=int(breaktime[0]),minutes=int(breaktime[1]))
                    breakLen = breakLen + breaktime
                elif(line[0] == "e"):
                    endTime = line[1].split(":")
                    endTime = timedelta(hours=int(endTime[0]),minutes=int(endTime[1]))
                    break
                i += 1
        timeLogged = (endTime - startTime) - breakLen
        totalTime += timeLogged
        print("- - - - - - - - - - - - - - - - -\nStart time:\t\t{}\nEnd time:\t\t{}\nTotal break time:\t{}\nTotal shift length:\t{}\n".format(str(startTime),str(endTime),str(breakLen),str(timeLogged)))
        line = log.readline().split(" ")
    log.close()
    return totalTime


def main():
    fileName = "workLog.txt"
    totalTime = parseLog(fileName)
    print("You worked {} hours this time period.".format(totalTime))


  
if __name__=="__main__":
    main()
