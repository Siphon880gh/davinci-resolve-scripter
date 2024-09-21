import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')


from python_get_resolve import GetResolve
resolve = app.GetResolve()
resolve.OpenPage("Edit")
