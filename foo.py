import asyncio
import numpy as np

a = np.random.randint(1, 10, size=10)
q = asyncio.Queue()
for i in a:
    q.put_nowait(i)
print(q.qsize())
