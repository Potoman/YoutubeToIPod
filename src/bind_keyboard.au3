#include <MsgBoxConstants.au3>
#include <Misc.au3>

HotKeySet("{ESC}", "Terminate")
HotKeySet("{F7}", "GoArtistFirst")
HotKeySet("{F8}", "GoTitleFirst")

While 1
    Sleep(100)
WEnd

Func GoArtistFirst()
	While _IsPressed("{F7}")
		Sleep(10)
	WEnd
	LaunchPythonScript("true")
EndFunc

Func GoTitleFirst()
	While _IsPressed("{F8}")
		Sleep(10)
	WEnd
	LaunchPythonScript("false")
EndFunc

Func LaunchPythonScript($parameterIsArtistFirst)
	ClipPut("")
	Send("^l") ; Width Chorme, that select address toolbar.
	Sleep(50)
	Send("^c") ; Copy url to clipboard
	Sleep(50)
	$variable = ClipGet() ; Get url from clipboard
	Run("py dly.py " & $variable & " " & $parameterIsArtistFirst)
	Sleep(5000)
EndFunc

Func Terminate()
    Exit
EndFunc
