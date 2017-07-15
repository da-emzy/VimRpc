# VimRpc #



| Src:  https://github.com/da-emzy/VimRpc

| Docs: https://github.com/da-emzy/VimRpc/doc/VimRpc.txt

*The project needs contributors*

VimRpc is a vim plugin that brings scripting to vim.
VimRpc allows you to  run vim as a REMOTE PROCEDURE CALL daemon,
Thereby connecting to it as a client and running the API FUNCTIONS bundled with VimRpc.

VimRpc allows you to embed vim in your program, 
giving you access to all of 'vim' functions and commands.
With VimRpc you can edit files in vim, run 'diff' commands open multiple windows
and do more with the programming language of your choice without launching vim.

VimRpc does this by making vim run as a "REMOTE PROCEDURE CALL" daemon where you run your
Commands as the client 'vim' handles it (being the server).
VimRpc also commes with HIGH-LEVEL API-FUNCTIONS to make VimRpc much more simpler and 
easy to use the User

******************
VimRpc comes bundled with 20+ API functions that give you HIGH-LEVEL access to the vim daemon.
Run:
``:help VimRpc-API-Functions`` 
To get details of the API-Functions and what they accept/return.


Documentation
=============

.. contents::

**To read VimRpc documentation in Vim, see** 
``help VimRpc.txt``

Requirements
============

- VIM >= 7.4 with `+python` or `+python3` support

How to install
==============

Using pathogen (recommended)
----------------------------
::

    % cd ~/.vim
    % mkdir -p bundle && cd bundle
    % git clone https://github.com/da-emzy/VimRpc.git

- Enable `pathogen <https://github.com/tpope/vim-pathogen>`_
  in your ``~/.vimrc``: ::

    " Pathogen load
    filetype off

    call pathogen#infect()
    call pathogen#helptags()

    filetype plugin indent on
    syntax on
Using Vundle (also recommended)
----------------------------
::

add the following to your `vimrc` then run
  `:PluginInstall`

        Plugin 'da-emzy/VimRpc'

Manually
--------
::

    % git clone https://github.com/da-emzy/VimRpc.git
    % cd VimRpc
    % cp -R * ~/.vim

Then rebuild **helptags** in vim::

    :helptags ~/.vim/doc/


Customization
=============

You can override most settings in VimRpc : ::

    "Override port VimRpc listens on to 2020"
    let g:rpc_bind_port = 2020

    "Override VimRpc protocol to use" # default "JSON"
    let g:rpc_proto = 'xml'

Run ``help VimRpc-Settings`` for more info


Bugtracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/da-emzy/VimRpc/issues

Contributing
============
Author
* Da Emzy (emzyoflyf@yahoo.com)

Also see the `AUTHORS` file.

Development of VimRpc happens at github:
https://github.com/klen/python-mode

Please make a pull request to `development` branch and add yourself to
`AUTHORS`.

Copyright
=========

Copyright © 207 Da Emzy (da-emzy)

License
=======

Licensed under a `GNU lesser general public license`_.

