import os,sys
import win32com.client as win32
dte = win32.GetActiveObject("VisualStudio.DTE.16.0")
for x in dte.Debugger.LocalProcesses:
    if x .ProcessID == os.getpid():
        x.Attach()
        break
a=5
