#!/usr/bin/env python

# WS client example

import asyncio
import websockets

delay = 1 # seconds

json = open("sample1.json").read().splitlines()

async def hello():
	
	uri = "ws://localhost:7071"
	
	async with websockets.connect(uri) as websocket:
		
		for line in json:
		
			await websocket.send(line)
			print(" -> ", line)

			in_txt = await websocket.recv()
			print(" <- ", in_txt)
			
			await asyncio.sleep(delay)

asyncio.get_event_loop().run_until_complete(hello())
