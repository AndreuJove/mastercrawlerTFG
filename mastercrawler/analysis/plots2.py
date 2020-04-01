import matplotlib
import matplotlib.pyplot as plt
import numpy as np

typeErrors = ["TimeoutError", "DNSLookupError", "ConnectError", "ConnectionRefusedError", "ResponseNeverReceived", "InvalidCodepoint", "ValueError", "IDNAError", "NoRouteError", "ResponseFailed"]
valuesCodes =[620, 345, 42, 36, 23, 3, 2, 1, 1, 1]

size = len(typeErrors)
y = np.arange(size) 
width = 0.50
fig, ay = plt.subplots()

rects1 = ay.barh(typeErrors,valuesCodes, width, color="purple")

ay.set_xlabel('Counts')
ay.set_xlim(0,700)
ay.set_title('Errors in Generic Tools')
ay.set_yticks(y)
ay.set_yticklabels(typeErrors)

def autolabel(rects):
    for rect in rects:
        height = rect.get_width()
        ay.annotate(f'{height}', xy=(height,rect.get_y()), xytext=(13, 0), textcoords="offset points", ha='center', va='bottom')

autolabel(rects1)

fig.tight_layout()

plt.show()







