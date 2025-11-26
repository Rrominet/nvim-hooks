#This is all the events you can react too :
#Buffer events
#BufAdd – buffer added to the buffer list
#BufDelete – buffer removed from buffer list
#BufEnter – entered buffer
#BufLeave – leaving buffer
#BufNew – new buffer created
#BufNewFile – new file created
#BufRead – just before reading a buffer
#BufReadPre – before reading a file into a buffer
#BufReadPost – after reading a file into a buffer
#BufUnload – before buffer is unloaded
#BufWinEnter – buffer is displayed in a window
#BufWinLeave – buffer is removed from a window
#BufWrite – before writing buffer
#BufWritePre – before writing buffer to file
#BufWritePost – after writing buffer to file
#
#File events
#FileReadPre, FileReadPost
#FileWritePre, FileWritePost
#FileAppendPre, FileAppendPost
#
#Window events
#WinLeave – leaving a window
#WinNew – new window opened
#WinClosed – window closed
#
#Editing events
#InsertEnter – starting Insert mode
#InsertLeave – leaving Insert mode
#TextChanged – text was changed in Normal mode
#TextChangedI – text was changed in Insert mode
#TextYankPost – after a yank
#
#Session/UI events
#VimEnter – after startup
#VimLeavePre – just before exiting
#VimLeave – exiting Vim
#ColorScheme – after loading a color scheme
#DirChanged – after :cd/:lcd
#Filetype / Syntax
#FileType – after setting filetype
#Syntax – after setting syntax
#
#Neovim-specific events
#CmdUndefined – command is undefined
#DirChanged – working directory changed
#Signal – received a signal
#TermOpen – terminal buffer opened
#TermClose – terminal closed
#UIEnter, UILeave – when a UI attaches/detaches

import pynvim
import os
import json
from ml import fileTools as ft

@pynvim.plugin
class Hooks(object) : 
    def __init__(self, nvim):
        self.nvim = nvim
        self.config = None
        self.active = False
        self.configpath = os.path.expanduser("~") + "/.config/nvim/hooks.json"

    def loadConfig(self):
        self.config = None
        if not os.path.exists(self.configpath):
            self.nvim.out_write(f"Config file {self.configpath} not found. Hooks rplugin disabled.\n")
            return
        try : 
            self.config = json.load(open(self.configpath))
            self.active = True
        except : 
            self.nvim.out_write(f"Config file {self.configpath} founded but not JSON parsable. Hooks rplugin disabled.\n")
            pass

    def on_event(self, event: str):
        if not self.active : 
            return
        buf = self.nvim.current.buffer.name if self.nvim.current.buffer else "NO_BUFFER"

        for cmd in self.config : 
            if cmd["event"] == event : 
                for c in cmd["commands"] : 
                    if buf not in cmd["files"] : 
                        continue
                    cmd = c.replace("$file", buf)
                    cmd = "!" + cmd
                    self.nvim.command(cmd)

    @pynvim.command('ReloadHooks', nargs='*', range='')
    def reloadConfig(self, args, _range):
        self.loadConfig()

    @pynvim.command('ConfigHooks', nargs='*', range='')
    def openConfig(self, args, _range):
        if not os.path.isdir(ft.parent(self.configpath)) : 
            os.makedirs(ft.parent(self.configpath))
        self.nvim.command(":e " + self.configpath)

    # -------------------------
    # Buffer events
    # -------------------------
    @pynvim.autocmd('BufAdd', pattern='*', sync=True)
    def _BufAdd(self): self.on_event("BufAdd")

    @pynvim.autocmd('BufDelete', pattern='*', sync=True)
    def _BufDelete(self): self.on_event("BufDelete")

    @pynvim.autocmd('BufEnter', pattern='*', sync=True)
    def _BufEnter(self): self.on_event("BufEnter")

    @pynvim.autocmd('BufLeave', pattern='*', sync=True)
    def _BufLeave(self): self.on_event("BufLeave")

    @pynvim.autocmd('BufNew', pattern='*', sync=True)
    def _BufNew(self): self.on_event("BufNew")

    @pynvim.autocmd('BufNewFile', pattern='*', sync=True)
    def _BufNewFile(self): self.on_event("BufNewFile")

    @pynvim.autocmd('BufRead', pattern='*', sync=True)
    def _BufRead(self): self.on_event("BufRead")

    @pynvim.autocmd('BufReadPre', pattern='*', sync=True)
    def _BufReadPre(self): self.on_event("BufReadPre")

    @pynvim.autocmd('BufReadPost', pattern='*', sync=True)
    def _BufReadPost(self): self.on_event("BufReadPost")

    @pynvim.autocmd('BufUnload', pattern='*', sync=True)
    def _BufUnload(self): self.on_event("BufUnload")

    @pynvim.autocmd('BufWinEnter', pattern='*', sync=True)
    def _BufWinEnter(self): self.on_event("BufWinEnter")

    @pynvim.autocmd('BufWinLeave', pattern='*', sync=True)
    def _BufWinLeave(self): self.on_event("BufWinLeave")

    @pynvim.autocmd('BufWrite', pattern='*', sync=True)
    def _BufWrite(self): self.on_event("BufWrite")

    @pynvim.autocmd('BufWritePre', pattern='*', sync=True)
    def _BufWritePre(self): self.on_event("BufWritePre")

    @pynvim.autocmd('BufWritePost', pattern='*', sync=True)
    def _BufWritePost(self): self.on_event("BufWritePost")

    # -------------------------
    # File events
    # -------------------------
    @pynvim.autocmd('FileReadPre', pattern='*', sync=True)
    def _FileReadPre(self): self.on_event("FileReadPre")

    @pynvim.autocmd('FileReadPost', pattern='*', sync=True)
    def _FileReadPost(self): self.on_event("FileReadPost")

    @pynvim.autocmd('FileWritePre', pattern='*', sync=True)
    def _FileWritePre(self): self.on_event("FileWritePre")

    @pynvim.autocmd('FileWritePost', pattern='*', sync=True)
    def _FileWritePost(self): self.on_event("FileWritePost")

    @pynvim.autocmd('FileAppendPre', pattern='*', sync=True)
    def _FileAppendPre(self): self.on_event("FileAppendPre")

    @pynvim.autocmd('FileAppendPost', pattern='*', sync=True)
    def _FileAppendPost(self): self.on_event("FileAppendPost")

    # -------------------------
    # Window events
    # -------------------------
    @pynvim.autocmd('WinEnter', pattern='*', sync=True)
    def _WinEnter(self): self.on_event("WinEnter")

    @pynvim.autocmd('WinLeave', pattern='*', sync=True)
    def _WinLeave(self): self.on_event("WinLeave")

    @pynvim.autocmd('WinNew', pattern='*', sync=True)
    def _WinNew(self): self.on_event("WinNew")

    @pynvim.autocmd('WinClosed', pattern='*', sync=True)
    def _WinClosed(self): self.on_event("WinClosed")

    # -------------------------
    # Editing events
    # -------------------------
    @pynvim.autocmd('InsertEnter', pattern='*', sync=True)
    def _InsertEnter(self): self.on_event("InsertEnter")

    @pynvim.autocmd('InsertLeave', pattern='*', sync=True)
    def _InsertLeave(self): self.on_event("InsertLeave")

    @pynvim.autocmd('TextChanged', pattern='*', sync=True)
    def _TextChanged(self): self.on_event("TextChanged")

    @pynvim.autocmd('TextChangedI', pattern='*', sync=True)
    def _TextChangedI(self): self.on_event("TextChangedI")

    @pynvim.autocmd('TextYankPost', pattern='*', sync=True)
    def _TextYankPost(self): self.on_event("TextYankPost")

    # -------------------------
    # Session/UI events
    # -------------------------
    @pynvim.autocmd('VimEnter', pattern='*', sync=True)
    def _VimEnter(self):
        self.loadConfig()
        self.on_event("VimEnter")

    @pynvim.autocmd('VimLeavePre', pattern='*', sync=True)
    def _VimLeavePre(self): self.on_event("VimLeavePre")

    @pynvim.autocmd('VimLeave', pattern='*', sync=True)
    def _VimLeave(self): self.on_event("VimLeave")

    @pynvim.autocmd('ColorScheme', pattern='*', sync=True)
    def _ColorScheme(self): self.on_event("ColorScheme")

    @pynvim.autocmd('DirChanged', pattern='*', sync=True)
    def _DirChanged(self): self.on_event("DirChanged")

    # -------------------------
    # Filetype / Syntax
    # -------------------------
    @pynvim.autocmd('FileType', pattern='*', sync=True)
    def _FileType(self): self.on_event("FileType")

    @pynvim.autocmd('Syntax', pattern='*', sync=True)
    def _Syntax(self): self.on_event("Syntax")

    # -------------------------
    # Neovim-specific events
    # -------------------------
    @pynvim.autocmd('CmdUndefined', pattern='*', sync=True)
    def _CmdUndefined(self): self.on_event("CmdUndefined")

    @pynvim.autocmd('Signal', pattern='*', sync=True)
    def _Signal(self): self.on_event("Signal")

    @pynvim.autocmd('TermOpen', pattern='*', sync=True)
    def _TermOpen(self): self.on_event("TermOpen")

    @pynvim.autocmd('TermClose', pattern='*', sync=True)
    def _TermClose(self): self.on_event("TermClose")

    @pynvim.autocmd('UIEnter', pattern='*', sync=True)
    def _UIEnter(self): self.on_event("UIEnter")

    @pynvim.autocmd('UILeave', pattern='*', sync=True)
    def _UILeave(self): self.on_event("UILeave")
