from threading import Thread

def GameFile():
    import Game

def webcamTestFile():
    import webcamTest


Thread(target = GameFile).start()
Thread(target = webcamTestFile).start()

