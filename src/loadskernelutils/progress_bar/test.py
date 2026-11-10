import logging
import time
from loadskernel.utils.progress_bar import ProgressLogger

logging.basicConfig(level=logging.INFO, format="%(message)s")

process = ProgressLogger()
print('start')

process.begin(tmax= 100)
for i in range(100):
    process.update(t= i)
    time.sleep(0.05)
process.end()


process.begin(tmax= 200)
for i in range(200):
    process.update(t= i)
    time.sleep(0.05)
process.end()


process.begin(tmax= 300)
for i in range(300):
    process.update(t= i)
    time.sleep(0.05)
process.end()