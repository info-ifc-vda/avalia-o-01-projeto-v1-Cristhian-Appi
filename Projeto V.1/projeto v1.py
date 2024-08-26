import concurrent.futures
import queue
import time
import random
import threading


def processTicket(requestId):
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)
    print(
        f"Requisição {requestId} processada com delay de {delay:.2f} segundos")


def producer(numberRequest, requestQueue):
    for i in range(numberRequest):
        print("Produzindo requisição ", i+1)
        requestQueue.put(i+1)
        time.sleep(random.uniform(0.01, 0.1))


def consumer(requestQueue):
    while True:
        try:
            requestId = requestQueue.get(timeout=1)
            processTicket(requestId)
            requestQueue.task_done()
        except queue.Empty:
            break


if __name__ == "__main__":
    numberRequest = 1000
    numThreadsConsumer = 10
    requestQueue = queue.Queue()

    producer_thread = threading.Thread(
        target=producer, args=(numberRequest, requestQueue))
    producer_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreadsConsumer) as executor:
        futures = [executor.submit(consumer, requestQueue)
                   for _ in range(numThreadsConsumer)]
        concurrent.futures.wait(futures)

    print("Todas as requisições foram processadas")
