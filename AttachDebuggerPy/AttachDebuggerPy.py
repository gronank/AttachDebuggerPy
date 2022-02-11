import os
import win32com.client
import pythoncom
import WindowTitle
import ctypes
import re

def GetVisualStudioInstances():
    instances = []
    wmi=win32com.client.GetObject('winmgmts:')
    for p in wmi.InstancesOf('win32_process') :
        if(p.Name.startswith('devenv')):
            title=WindowTitle.enum_process_windows(p.Handle)
            instances.append((title, p.ProcessID))
    return instances

def AttachToDebugger(debuggerProcessId, applicationProcessId):
    name, dte=getDTE(debuggerProcessId)
    for process in dte.Debugger.LocalProcesses:
        if process.ProcessID == applicationProcessId:
            process.Attach()
            break

def getDTE(processId):
    rot = pythoncom.GetRunningObjectTable()
    running_objects=rot.EnumRunning()
    dteMatcher =re.compile(f'!VisualStudio.DTE\.\d+\.\d+\:{processId}') 
    ctx=pythoncom.CreateBindCtx(0)
    
    for moniker in iter(running_objects):
        name=moniker.GetDisplayName(ctx, None)
        if(dteMatcher.match(name)):
            dte = rot.GetObject(moniker).QueryInterface(pythoncom.IID_IDispatch)
            className = getClass(name)
            dteId = win32com.client.pywintypes.IID(className)
            dte = win32com.client.Dispatch(dte, className, resultCLSID=dteId, clsctx=pythoncom.CLSCTX_ALL)
            return name, dte
    return None

def getClass(name):
    m = re.match("!(.*?):", name)
    return m.group(1)

if __name__=="__main__":
    vsInstances = GetVisualStudioInstances()
    for title, pid in vsInstances:
        if(ctypes.windll.user32.MessageBoxW(0, title, "Your title", 1) == 1):
            AttachToDebugger(pid, os.getpid())
            break
    a=43