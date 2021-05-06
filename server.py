#!/usr/bin/env python3

import asyncio
import websockets
import requests
import time
import json

host = "0.0.0.0"
port = 7071
connected = set()

async def trie(text):
	
	query = {"query": text}
	
	r = requests.get("https://api.smartterp.linkeddata.es/", params=query)
	
	return r.text

async def consumer(message):
	try:
		data = json.loads(message)

		text_data = data["result"]["hypotheses"][0]["transcript"].replace("\\r", "")
		
		if len(text_data) > 0:
			
			print("Request: ", data["request_id"])
			print("Data: ", text_data)
			
			return await trie(text_data)
			
		return json.dumps({"error": "No data"})
		
	except ValueError:
		print("No JSON data!")
		
		return json.dumps({"error": "No JSON data"})
		
	
#async def producer():
#	await asyncio.sleep(3)
#	return str(time.time())

async def consumer_handler(websocket, path):
	async for message in websocket:
		#print(" <- ", message)
		result = await consumer(message)
		await websocket.send(result)

#async def producer_handler(websocket, path):
#	while True:
#		message = await producer()
#		#print(" -> ", message)
#		await websocket.send(message)

async def handler(websocket, path):

	connected.add(websocket)
	try:
		consumer_task = asyncio.ensure_future(
			consumer_handler(websocket, path))
		#producer_task = asyncio.ensure_future(
		#	producer_handler(websocket, path))
		done, pending = await asyncio.wait(
			[
			consumer_task
			#, producer_task
			],
			return_when=asyncio.FIRST_COMPLETED,
		)
		for task in pending:
			task.cancel()
	finally:
		connected.remove(websocket)
		
		
start_server = websockets.serve(handler, host, port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
