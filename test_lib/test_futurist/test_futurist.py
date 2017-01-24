# NOTE: enable printing timestamp for additional data

import sys
import time
import datetime
import futurist
import eventlet
from futurist import periodics
import threading

def delayed_func():
    print("started")
    eventlet.sleep(3)
    print("done")

def test_1():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    e = futurist.SynchronousExecutor()
    fut = e.submit(delayed_func)
    eventlet.sleep(1)
    print("Hello")
    eventlet.sleep(1)
    e.shutdown()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def test_2():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    e = futurist.GreenThreadPoolExecutor()
    fut = e.submit(delayed_func)
    eventlet.sleep(1)
    print("Hello")
    eventlet.sleep(1)
    e.shutdown()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def test_3():
    "Creating and using a thread-based executor"
    def delayed_func():
        time.sleep(0.1)
        return "hello"

    e = futurist.ThreadPoolExecutor()
    fut = e.submit(delayed_func)
    print(fut.result())
    e.shutdown()

def test_4():
    "Creating and using a process-based executor"
    def delayed_func():
        time.sleep(0.1)
        return "hello"

    e = futurist.ProcessPoolExecutor()
    fut = e.submit(delayed_func)
    print(fut.result())
    e.shutdown()

def test_5():
    "Running a set of functions periodically"
    @periodics.periodic(1)
    def every_one(started_at):
        print("1: %s" % (time.time() - started_at))


    @periodics.periodic(2)
    def every_two(started_at):
        print("2: %s" % (time.time() - started_at))


    @periodics.periodic(4)
    def every_four(started_at):
        print("4: %s" % (time.time() - started_at))


    @periodics.periodic(6)
    def every_six(started_at):
        print("6: %s" % (time.time() - started_at))


    started_at = time.time()
    callables = [
        # The function to run + any automatically provided positional and
        # keyword arguments to provide to it everytime it is activated.
        (every_one, (started_at,), {}),
        (every_two, (started_at,), {}),
        (every_four, (started_at,), {}),
        (every_six, (started_at,), {}),
    ]
    w = periodics.PeriodicWorker(callables)

    # In this example we will run the periodic functions using a thread, it
    # is also possible to just call the w.start() method directly if you do
    # not mind blocking up the current program.
    t = threading.Thread(target=w.start)
    t.daemon = True
    t.start()

    # Run for 10 seconds and then stop.
    while (time.time() - started_at) <= 10:
        time.sleep(0.1)
    w.stop()
    w.wait()
    t.join()

def test_6():
    "Running a set of functions periodically (using an executor)"
    @periodics.periodic(1)
    def every_one(started_at):
        print("1: %s" % (time.time() - started_at))
        time.sleep(0.5)


    @periodics.periodic(2)
    def every_two(started_at):
        print("2: %s" % (time.time() - started_at))
        time.sleep(1)


    @periodics.periodic(4)
    def every_four(started_at):
        print("4: %s" % (time.time() - started_at))
        time.sleep(2)


    @periodics.periodic(6)
    def every_six(started_at):
        print("6: %s" % (time.time() - started_at))
        time.sleep(3)


    started_at = time.time()
    callables = [
        # The function to run + any automatically provided positional and
        # keyword arguments to provide to it everytime it is activated.
        (every_one, (started_at,), {}),
        (every_two, (started_at,), {}),
        (every_four, (started_at,), {}),
        (every_six, (started_at,), {}),
    ]

    # To avoid getting blocked up by slow periodic functions we can also
    # provide a executor pool to make sure that slow functions only block
    # up a thread (or green thread), instead of blocking other periodic
    # functions that need to be scheduled to run.
    executor_factory = lambda: futurist.ThreadPoolExecutor(max_workers=2)
    w = periodics.PeriodicWorker(callables, executor_factory=executor_factory)

    # In this example we will run the periodic functions using a thread, it
    # is also possible to just call the w.start() method directly if you do
    # not mind blocking up the current program.
    t = threading.Thread(target=w.start)
    t.daemon = True
    t.start()

    # Run for 10 seconds and then stop.
    while (time.time() - started_at) <= 10:
        time.sleep(0.1)
    w.stop()
    w.wait()
    t.join()

if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    # test_5()
    test_6()