from struct import *
from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = ord(string[count + 1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
           print("소켓이 null")
           return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        # Fill in start
        # Fetch the ICMP header from the IP packet
        icmpheader = recPacket[20:28] #20부터 28바이트까지 앞의 20바이트는 ip의 헤더
        type, code, checksum, receiveID, sequence = struct.unpack("bbHHh", icmpHeader) # 헤더로부터 타입, 코드 등 분리
        if type == 0:
            print( "Destination Network Unreachable")
        if type == 1:
            print ("Destination Host Unreachable")
        if type == 3:
            print( "Destination Unreachable")
        if type == 4: # 송신지 억제
            print ("Source Quench")
        if type == 5: # 재지시
            print( "Redirect")
        if type == 11: # ttl초과
            print ("Time Exceeded")
        if type == 12: # 재지시
            print ("Parameter Problem")


        if receiveID == ID: #보낸 id와 받은 id가 같은 경우!(내가 송신자일 경우)
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent
        # Fill in end

        timeLeft = timeLeft - howLongInSelect
        print(timeLeft)
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(str(header + data))

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


# Both LISTS and TUPLES consist of a number of objects
# which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw

    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    min = 0
    first = True
    max = 0
    total = 0
    loss_count = 0
    count = 0

    # Send ping requests to a server separated by approximately one second
    while 1:
        delay = doOnePing(dest, timeout)
        print(delay)
        if delay == "Request timed out.":
         count = count+1
         loss_count = loss_count+1
         print ("Time out")
        else:
         count = count+1
         delay = delay * 1000
         total = total + delay
         if delay > max:
            max = delay
         if delay < min or first == True:
            first = False
            min = delay
    average = total / count
    print("max = %0.3fms " % max)
    print( "min = %0.3fms" % min)
    print("average = %0.3fms" % average)
    print("loss rate" %(loss_count*100/count))
    time.sleep(1)  # one second
    return delay


ping("127.0.0.1")
