from PIL import Image
from os import mkdir, walk
from time import time as now
from json import load as json
from threading import Thread


config = json(open('config.json', 'r', encoding='utf-8'))
TARGET_COLOR = tuple(config.get('target-color') or (255, 255, 255, 255))
TORELANCE_VALUE = float(config.get('torelance')) * 255

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

def removeImageBackground(inputFilepath: str, outputFilepath: str = '') -> Image:
  image = Image.open(inputFilepath)
  image = image.convert('RGBA') # RGBA 顏色編碼能夠設置透明度
  pixdata = image.load()
  bgPixels = []
  notIncludeInside = False
  
  for y in range(image.size[1]):
    rowIndices = list(range(image.size[0]))
    while len(rowIndices):
      x = rowIndices.pop()
      if isTargetColor(pixdata[x, y]):
        bgPixels.append((x, y))
      elif notIncludeInside:
        break
    while len(rowIndices):
      x = rowIndices.pop(0)
      if isTargetColor(pixdata[x, y]):
        bgPixels.append((x, y))
      elif notIncludeInside:
        break

  if notIncludeInside:
    for x in range(image.size[0]):
      columnIndices = list(range(image.size[1]))
      while len(columnIndices):
        y = columnIndices.pop()
        if isTargetColor(pixdata[x, y]):
          bgPixels.append((x, y))
        elif notIncludeInside:
          break
      while len(columnIndices):
        y = columnIndices.pop(0)
        if isTargetColor(pixdata[x, y]):
          bgPixels.append((x, y))
        elif notIncludeInside:
          break
  
  for coor in bgPixels: pixdata[coor] = (255, 255, 255, 0)
  
  if outputFilepath:
    try: mkdir('/'.join(outputFilepath.split('/')[:-1]))
    except: path
    image.save(outputFilepath, 'PNG')

  return image

class ImageProcess(Thread):
  __slots__ = ('filename', 'inputFilepath', 'outputFilepath')
  def __init__(self, filename: str, inputFilepath: str, outputFilepath: str = '') -> None:
    Thread.__init__(self)
    self.filename = filename
    self.inputFilepath = inputFilepath.replace('\\', '/')
    self.outputFilepath = outputFilepath.replace('\\', '/')
  def run(self) -> None:
    try:
      removeImageBackground(self.inputFilepath, self.outputFilepath)
      print(f'Processed: {self.filename}')
    except Exception as error:
      print(f'An error occurred while processing the file "{self.filename}". ({error})')

threads = []

t0 = now()

for path, dirs, files in walk('input/'):
  path = path.replace('input/', '', 1)
  if path: path += '/'
  for filename in files:
    filename = f'{path}{filename}'
    inputFilepath = f'input/{filename}'
    outputFilepath = f'output/{filename}'
    process = ImageProcess(filename, inputFilepath, outputFilepath)
    threads.append(process)

for t in threads: t.start()
for t in threads: t.join()

print(f'Time taken:  {round(now() - t0, 4)}s')