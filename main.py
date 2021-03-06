import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from gpiozero import Servo
from time import sleep, time
import threading

myGPIO = 17
myCorrection = 1
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000
servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
servo.detach()

app = FastAPI()


class Info:
    status = False
    speed = 1
    force = False
    duration = 60
    start_time = 0
    end_time = 0


@app.get("/start")
async def start(speed: float, duration: int):
    Info.status = True
    Info.force = False
    Info.speed = speed
    Info.start_time = time()
    Info.end_time = duration*60 + Info.start_time

    return JSONResponse({"res": "started"})


@app.get("/status")
async def status():
    return JSONResponse({"vugge": Info.vugge, "hastighed": Info.hastighed})


@app.get("/stop")
async def stop():
    Info.status = False
    return JSONResponse({"res": "stopped"})


@app.get("/force")
async def force():
    Info.force = True


class ThreadingRun(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.vugge, args=())
        thread.daemon = False
        thread.start()

    def vugge(self):
        while True:
            if Info.status and time() < Info.end_time:
                print("Time left: ", Info.end_time-time())
                print("Vugge")
                servo.max()
                print("max")
                sleep(1)
                servo.detach()
                sleep(Info.speed)
                if Info.force:
                    break
            else:
                print("Not vugging")
                servo.detach()
                sleep(1)


app.mount("/", StaticFiles(directory="website", html=True), name="website")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

run = ThreadingRun()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
