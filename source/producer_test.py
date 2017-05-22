from createThread import createThread
import threading
import thread
import time

exitFlag = 0
print "Test Producer"
thread1 = createThread(1, "Thread-1", 1, '/ndn/test1')
thread2 = createThread(2, "Thread-2", 2, '/ndn/test2')

thread1.start()
thread2.start()

print "Exiting Main Thread"

# try:
#     #thread.start_new_thread(producer1.run())
#     thread.start_new_thread(Producer, ('/ndn/test1'))
#     thread.start_new_thread(Producer, ('/ndn/test2'))
# except:
#     print "Error: unable to start thread"







