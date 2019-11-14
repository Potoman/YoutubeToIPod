#include <Constants.au3>
#include <File.au3>
#include <MsgBoxConstants.au3>
#include <Misc.au3>

HotKeySet("{ESC}", "Terminate")
HotKeySet("{F7}", "GoArtistFirst")
HotKeySet("{F8}", "GoTitleFirst")
HotKeySet("{F9}", "GoToUpdateYoutubeDl")

While 1
    Sleep(100)
WEnd

Func RunSyncProcess($cmd)
	Local $pid = Run($cmd, "", @SW_HIDE, $STDOUT_CHILD + $STDERR_CHILD)
	ProcessWaitClose($pid)
	Local $output = StdoutRead($pid)
	ConsoleWrite($cmd & " > " & $output & @LF)
	$filePath = @ScriptDir & "\dl_youtube_autoit.log"
	FileDelete($filePath)
	_FileWriteLog($filePath, $output)
EndFunc

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

Func GoToUpdateYoutubeDl()
	While _IsPressed("{F9}")
		Sleep(10)
	WEnd
	Sleep(1000)
	RunSyncProcess("pip install -U youtube-dl")
	Exit 0
EndFunc

Func LaunchPythonScript($parameterIsArtistFirst)
	ConsoleWrite("LaunchPythonScript : " + $parameterIsArtistFirst)
	ClipPut("")
	Send("^l") ; Width Chrome, that select address toolbar.
	Sleep(1000)
	Send("^c") ; Copy url to clipboard
	Sleep(1000)
	Local $variable = ClipGet() ; Get url from clipboard
	RunSyncProcess("py " & @ScriptDir & "\main.py " & $variable & " " & $parameterIsArtistFirst)
EndFunc

Func Terminate()
   Exit 0
EndFunc
