import requests
from bs4 import BeautifulSoup

url= "https://www.youtube.com/watch?v=UROL6REOq6g"
res = requests.get(url)
html = res.content.decode('utf-8','replace')

soup = BeautifulSoup(html, 'html.parser')
print(soup)

# ________________________________________________________________________________

# ________________________________________________________________________________

import numpy as np
b = np.char.split(d[d.find("C")+1:d.rfind("C")].split("C"), sep=" ")

xd, yd = [], []
for z in b:
  xs, ys = z[3].split(",")
  x, y = (float(xs)-5)/1000, (100-float(ys))/100
  xd += [x]
  yd += [y]

from matplotlib import pyplot as plt
plt.figure(figsize=(20, 2))
plt.plot(xd, yd)
plt.show()