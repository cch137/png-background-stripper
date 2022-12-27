from PIL import Image
from os import mkdir, listdir
from time import time, sleep
import json
from threading import Thread, Lock


config = json.load(open('config.json', 'r', encoding='utf-8'))
TARGET_COLOR = tuple(config.get('target-color') or (255, 255, 255, 255))
TORELANCE_VALUE = (config.get('torelance') or 0.05) * 255

try: mkdir('input/')
except: pass
try: mkdir('output/')
except: pass

def isTargetColor(rgbaTuple: tuple) -> bool:
  for index in range(4):
    if rgbaTuple[index] > TARGET_COLOR[index] + TORELANCE_VALUE:
      return False
    if rgbaTuple[index] < TARGET_COLOR[index] - TORELANCE_VALUE:
      return False
  return True

def removeWhiteBackground(inputFilepath: str, outputFilepath: str = '') -> Image:
  image = Image.open(inputFilepath)
  image = image.convert('RGBA') # RGBA 顏色編碼能夠設置透明度
  pixdata = image.load()
  processThreads = []
  processedPixels = []
  lock = Lock()

  def processPixel(x: int, y: int):
    if ((x, y) in processedPixels):
      return
    if x > 1:
      try: processPixel(x - 1, y)
      except Exception as e: print(e)
    if x + 1 < image.size[0]:
      try: processPixel(x + 1, y)
      except Exception as e: print(e)
    if y > 0:
      try: processPixel(x, y - 1)
      except Exception as e: print(e)
    if y + 1 < image.size[1]:
      try: processPixel(x, y + 1)
      except Exception as e: print(e)
    if isTargetColor(pixdata[x, y]):
      with lock:
        pixdata[x, y] = (255, 255, 255, 0)
    with lock:
      processedPixels.append((x, y))
  
  class processThread(Thread):
    __slots__ = ('x', 'y')
    def __init__(self, x: int, y:int) -> None:
      self.x = x
      self.y = y
    def run(self):
      processPixel(self.x, self.y)
  
  for y in range(image.size[1]):
    rowIndices = list(range(image.size[0]))
    while len(rowIndices):
      x = rowIndices.pop()
      if pixdata[x, y] == (255, 255, 255, 255):
        processedPixels.append(processThread(x, y))
      else:
        break
    while len(rowIndices):
      x = rowIndices.pop(0)
      if pixdata[x, y] == (255, 255, 255, 255):
        processedPixels.append(processThread(x, y))
      else:
        break
  
  for i in processThreads: i.start()
  for i in processThreads: i.join()

  sleep(3)
  
  if outputFilepath:
    image.save(outputFilepath, 'PNG')

  return image

for filename in listdir('input/'):
  t0 = time()
  inputFilepath = f'input/{filename}'
  outputFilepath = f'output/{filename}'
  try:
    removeWhiteBackground(inputFilepath, outputFilepath)
    print(f'Processed: {filename} ({round(time() - t0, 2)}s)')
  except Exception as error:
    print(f'An error occurred while processing the file "{filename}". ({error})')
