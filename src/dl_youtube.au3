#include <MsgBoxConstants.au3>
#include <Misc.au3>

HotKeySet("{ESC}", "Terminate")
HotKeySet("{F7}", "GoArtistFirst")
HotKeySet("{F8}", "GoTitleFirst")

Global $PidPython

While 1
    Sleep(100)
WEnd

Func GoArtistFirst()
	While _IsPressed("{F7}")
		Sleep(10)
	WEnd
	Sleep(1000)
	LaunchPythonScript("true")
EndFunc

Func GoTitleFirst()
	While _IsPressed("{F8}")
		Sleep(10)
	WEnd
	Sleep(1000)
	LaunchPythonScript("false")
EndFunc

Func LaunchPythonScript($parameterIsArtistFirst)
	ConsoleWrite("LaunchPythonScript : " + $parameterIsArtistFirst)
	ClipPut("")
	Send("^l") ; Width Chrome, that select address toolbar.
	Sleep(1000)
	Send("^c") ; Copy url to clipboard
	Sleep(1000)
	Local $variable = ClipGet() ; Get url from clipboard
	$PidPython = Run("py " & @ScriptDir & "\dly.py " & $variable & " " & $parameterIsArtistFirst)
EndFunc

Func Terminate()
   ProcessClose($PidPython)
   Exit 0
EndFunc
