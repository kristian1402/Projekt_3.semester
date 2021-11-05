from multiprocessing import Process

def GameFile():
    import Game

def webcamTestFile():
    import webcamTest

def main():

    p1 = Process(target=GameFile)
    p1.start()
    p2 = Process(target=webcamTestFile)
    p2.start()

    p1.join()
    p2.join()

if __name__ == '__main__':
    main()



