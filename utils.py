import time

class Color:
	red = "\033[91m"
	green = "\033[92m"
	yellow = "\033[93m"
	blue = "\033[94m"
	purple = "\033[95m"
	cyan = "\033[96m"
	white = "\033[97m"
	end = "\033[0m"



def rainbow():
	colored = [Color.red, Color.green, Color.yellow, Color.blue, Color.purple, Color.cyan, Color.white]
	i = 0
	while True:
		if i == 7:
			i = 0
		print(colored[i] + "Hello World!" + Color.end)
		i += 1
		time.sleep(0.1)
