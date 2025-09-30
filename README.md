# Neovim Hooks rplugin

This plugin let you *attach* any shell command you want to any Neovim `event` you want for any file you want.  
For example, you can : 
 - execute a shell script when you save a certain file.
 - execute a shell script when you open a certain file.
 - execute a shell script when you close a certain file.
 - etc.

For now, it only works with the command that run on buffers.    
But in the future you will be also be able to attach commands on event like `VimEnter`, `VimLeave`, `BufEnter` and `BufLeave`.

> [!NOTE]
> For now, it has only be tested on Linux.

## Installation

git clone this repo where you want (the destination doesn't matter) :
```bash
cd /where/you/want
git clone https://github.com/Rrominet/nvim-hooks 
```

Once done copy the file `hooks.py` in your `~/.config/nvim/rplugin/python3/` directory.  
If you don't have the directory, create it.

After this, open `nvim` and hit the command `:UpdateRemotePlugins`  
You can close it now.

The plugin should be installed.

## Usage

For this plugin to work, you need a configuration file : `~/.config/nvim/hooks.json`  
It's a json that contains the commands you want to attach to the events you want.

Here is a minimal example : 
```json
[
    {
        "event": "BufWritePost",
        "commands" : 
        [
            "echo 'BufWritePost on $file'"
        ], 

        "files" : 
        [
            "/tmp/test.md"
        ]
    }
]
```

This would simply execute the command `echo 'BufWritePost on $file'` when you save the file `/tmp/test.md`.  
`BufWritePost` being the event executing by `nvim` just after it has saved a file.

The file `hooks.json` contains an array of objects that have 3 keys :   
 - `event` : the event to attach the commands to. (a single string - you can see all the events you can listen too [here](#neovim-events-reference)
 - `commands` : the commands to execute. (an array of strings where each string is a complete shell command. You can use the variable `$file` in it that will be replaced by the current file that received the event)
 - `files` : the filepaths you want these commands to be executed on. If your file is not in there, the commands will not be executed. (an array of strings where each string is a filepath)

When you modify your `hooks.json` file, you don't need to restart `nvim`, you can just hit the command `:ReloadHooks` and you're good to go.

Aaaand you're done !  
Good Luck ! 

## Neovim Events Reference
This is all the events you can react too :

### Buffer events
 - BufAdd – buffer added to the buffer list
 - BufDelete – buffer removed from buffer list
 - BufEnter – entered buffer
 - BufLeave – leaving buffer
 - BufNew – new buffer created
 - BufNewFile – new file created
 - BufRead – just before reading a buffer
 - BufReadPre – before reading a file into a buffer
 - BufReadPost – after reading a file into a buffer
 - BufUnload – before buffer is unloaded
 - BufWinEnter – buffer is displayed in a window
 - BufWinLeave – buffer is removed from a window
 - BufWrite – before writing buffer
 - BufWritePre – before writing buffer to file
 - BufWritePost – after writing buffer to file

### File events
 - FileReadPre, FileReadPost
 - FileWritePre, FileWritePost
 - FileAppendPre, FileAppendPost

### Window events
 - WinLeave – leaving a window
 - WinNew – new window opened
 - WinClosed – window closed

### Editing events
 - InsertEnter – starting Insert mode
 - InsertLeave – leaving Insert mode
 - TextChanged – text was changed in Normal mode
 - TextChangedI – text was changed in Insert mode
 - TextYankPost – after a yank

### Session/UI events
 - VimEnter – after startup
 - VimLeavePre – just before exiting
 - VimLeave – exiting Vim
 - ColorScheme – after loading a color scheme
 - DirChanged – after :cd/:lcd
 - Filetype / Syntax
 - FileType – after setting filetype
 - Syntax – after setting syntax

### Neovim - specific events
 - ChanOpen – a channel opened
 - ChanClose – a channel closed
 - CmdUndefined – command is undefined
 - DirChanged – working directory changed
 - Signal – received a signal
 - TermOpen – terminal buffer opened
 - TermClose – terminal closed
 - UIEnter, UILeave – when a UI attaches/detaches
