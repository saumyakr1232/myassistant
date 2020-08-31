import win32gui


def windowEnumerationHandler(hwnd, top_windows):
	"""

	:param hwnd:
	:type top_windows: List
	"""
	top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def bring_forward(name: str):
	"""
	:param name:
	"""

	top_windows = []
	win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	for i in top_windows:
		if name.lower() in i[1].lower():
			print(i)
			win32gui.ShowWindow(i[0], 5)
			win32gui.SetForegroundWindow(i[0])
			break


def main():
	print("done")


if __name__ == "__main__":
	main()
