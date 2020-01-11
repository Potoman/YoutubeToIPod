#include <Constants.au3>
#include <File.au3>
#include <MsgBoxConstants.au3>
#include <Misc.au3>

HotKeySet("{ESC}", "Terminate")
HotKeySet("{F7}", "GoDl")
HotKeySet("{F9}", "GoToUpdateYoutubeDl")

While 1
    Sleep(100)
WEnd

Func RunSyncProcess($cmd)
	Local $pid = Run($cmd)
	ProcessWaitClose($pid)
EndFunc

Func GoDl()
	While _IsPressed("{F7}")
		Sleep(10)
	WEnd
	Sleep(1000)
	LaunchPythonScript()
 EndFunc

Func GoToUpdateYoutubeDl()
	While _IsPressed("{F9}")
		Sleep(10)
	WEnd
	Sleep(1000)
	RunSyncProcess("pip install -U youtube-dl")
	Exit 0
EndFunc

Func LaunchPythonScript()
	ConsoleWrite("LaunchPythonScript")
	ClipPut("")
	Send("^l") ; Width Chrome, that select address toolbar.
	Sleep(1000)
	Send("^c") ; Copy url to clipboard
	Sleep(1000)
	Local $variable = ClipGet() ; Get url from clipboard
	RunSyncProcess("python " & @ScriptDir & "\main.py " & $variable)
EndFunc

Func Terminate()
   Exit 0
EndFunc
