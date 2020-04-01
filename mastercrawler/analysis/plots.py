import matplotlib
import matplotlib.pyplot as plt
import numpy as np

httpCodes = [200, 301, 302, 429, 404, 303, 403, 202, 503, 500, 307, 308, 502, 410, 401, 400]

valuesCodes =[19910, 4719, 3538, 1792, 810, 231, 68, 47, 47, 45, 20, 15, 12, 7, 3, 3]

x = np.arange(len(httpCodes)) 
width = 0.50
fig, ax = plt.subplots()

rects1 = ax.bar(x, valuesCodes, width, color="purple")

ax.set_ylabel('Counts')
ax.set_title('HTTP Codes Generic Tools')
ax.set_xticks(x)
ax.set_xticklabels(httpCodes)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}', xy=(rect.get_x(), height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

autolabel(rects1)

fig.tight_layout()

plt.show()




