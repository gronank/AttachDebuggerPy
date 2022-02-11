import win32con as wcon
import win32api as wapi
import win32gui as wgui
import win32process as wproc

def enum_windows_proc(wnd, param):
    pid = param.get("pid", None)
    data = param.get("data", None)
    if pid is None or wproc.GetWindowThreadProcessId(wnd)[1] == pid:
        text = wgui.GetWindowText(wnd)
        if text:
            style = wapi.GetWindowLong(wnd, wcon.GWL_STYLE)
            if style & wcon.WS_VISIBLE:
                if data is not None:
                    data.append(text)
                    return


def enum_process_windows(pid=None):
    data = []
    param = {
        "pid": int(pid),
        "data": data,
    }
    wgui.EnumWindows(enum_windows_proc, param)
    return data[0]
