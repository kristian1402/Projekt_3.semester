from multiprocessing import Process

def GameFile():
    # Write the name of the file you want to play here

    # Regular game = "Game"
    # Input Override (50% Auto-Jump) = "InputOverride"
    # Rule Change (Slow Down) = "RuleChange"
    # Mitigated Failure (50% No Falling) = "MitigatedFailure
    import Game

def webcamTestFile():
    import CameraInput

def main():

    p1 = Process(target=GameFile)
    p1.start()
    p2 = Process(target=webcamTestFile)
    p2.start()

    p1.join()
    p2.join()

if __name__ == '__main__':
    main()



