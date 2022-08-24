import multiprocessing

from heavy import heavy_computational_function

if __name__ == "__main__":

    p = []
    for i in range(200):
        p.append(
            multiprocessing.Process(
                target=heavy_computational_function,
                args=("log" + str(i % 50) + "  ",),
            )
        )

    for i in range(200):
        p[i].start()

    for i in range(200):
        p[i].join()
