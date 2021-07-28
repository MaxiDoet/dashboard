import nextion
from time import sleep

async def dim_in(client, time, start=0, stop=100):
    time_per_step = time / 100

    for i in range(start, stop, 1):
        sleep(time_per_step)
        await client.dim(i)

async def dim_out(client, time, start=100, stop=0):
    time_per_step = time / 100

    for i in range(start, stop, -1):
        sleep(time_per_step)
        await client.dim(i)