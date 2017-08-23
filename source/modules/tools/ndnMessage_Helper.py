from pyndn import Interest
from pyndn import Data
from pyndn import Exclude
from pyndn import Name
from pyndn import Face
from pyndn import InterestFilter
from pyndn.security import KeyChain
import os

lastChunk_window = 0
lastChunk_sent = 0


def extractData_message(path, fileName, data):
    payload = data.getContent()
    dataName = data.getName()
    dataName_size = dataName.size()
    print "Extracting Data message name: ", dataName.toUri()
    #print "Received data: ", payload.toRawStr()
    if not os.path.exists(path):
            os.makedirs(path)

    with open(os.path.join(path, fileName), 'ab') as temp_file:
        temp_file.write(payload.toRawStr())
        # if recieved Data is a segment of the file, then need to fetch remaning segments
        # try if segment number is existed in Data Name
    try:
        dataSegmentNum = (dataName.get(dataName_size - 1)).toSegment()
        lastSegmentNum = (data.getMetaInfo().getFinalBlockId()).toNumber()
        print "dataSegmentNum" + str(dataSegmentNum)
        print "lastSegmentNum" + str(lastSegmentNum)

        # If segment number is available and what have recieved is not the FINAL_BLOCK, then fetch the NEXT segment
        if lastSegmentNum != dataSegmentNum:
            interestName = dataName.getSubName(0, dataName_size - 1)
            interestName = interestName.appendSegment(dataSegmentNum + 1)
            return False, interestName
            #self._sendNextInterest(interestName, self.interestLifetime, 'pull')
        # If segment number is available and what have recieved is the FINAL_BLOCK, then EXECUTE the configuration script
        ### Recieve all chunks of data --> Execute it here

        elif lastSegmentNum == dataSegmentNum:
            print "Received complete Data message: %s  " %fileName
            interestName = 'complete'
            return True, interestName
        else:
            print 'Data segment failed'

    except RuntimeError as e:
            print "ERROR: %s" % e
            #self.isDone = True

def request_SubsequenceDataChunk(path, fileName, data, window):
    payload = data.getContent()
    dataName = data.getName()
    dataName_size = dataName.size()
    print "Extracting Data message name: ", dataName.toUri()
    if not os.path.exists(path):
            os.makedirs(path)

    with open(os.path.join(path, fileName), 'ab') as temp_file:
        temp_file.write(payload.toRawStr())
    try:
        dataSegmentNum = (dataName.get(dataName_size - 1)).toSegment()
        lastSegmentNum = (data.getMetaInfo().getFinalBlockId()).toNumber()
        print "dataSegmentNum" + str(dataSegmentNum)
        print "lastSegmentNum" + str(lastSegmentNum)

        if dataSegmentNum == self.lastChunk_window:
            print 'Send Interest of next window frame'
            firstChunk_sent = self.lastChunk_window + 1
            self.lastChunk_window = self.lastChunk_window + self.window
            if self.lastChunk_window <= lastSegmentNum:
                print 'This is NOT the last frame'
                self.lastChunk_sent = self.lastChunk_window
            else:
                print 'This is the last frame'
                self.lastChunk_sent = lastSegmentNum
            for chunkID in range (firstChunk_sent, self.lastChunk_sent + 1):
                interestName = dataName.getSubName(0, dataName_size - 1)
                interestName = interestName.appendSegment(chunkID)
                self._sendNextInterest(interestName, self.interestLifetime, 'pull')
        else:
            print 'Already sent window frame, Waiting for Data message'

        if lastSegmentNum == dataSegmentNum:
            print "Received complete image: %s, EXECUTED !!!!" % fileName
            self.lastChunk_window = 0

    # If Configuration Manager has sent a file with 'install' key word, but no segment number is available, that DATA packet is invalid. Then just do nothing and exist the program
    except RuntimeError as e:
            print "ERROR: %s" % e
            self.isDone = True
