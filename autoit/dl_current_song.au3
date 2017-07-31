#include <MsgBoxConstants.au3>
#include <Misc.au3>

HotKeySet("{ESC}", "Terminate")
HotKeySet("{F7}", "Go")

While 1
    Sleep(100)
WEnd

Func Go()

	While _IsPressed("{F7}")
		Sleep(10)
	WEnd

	ClipPut("")
	Send("^l") ; Width Chorme, that select address toolbar.
	Sleep(50)
	Send("^c") ; Copy url to clipboard
	Sleep(50)

	$variable = ClipGet() ; Get url from clipboard

	Run("py C:\Users\LEPOT\Documents\python\YoutubeToIPod\src\dly.py " & $variable)
EndFunc

Func Terminate()
    Exit
EndFunc
