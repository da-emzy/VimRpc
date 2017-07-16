"vim handler
"DRY
if exists('g:loaded_rpc_init')
    finish
endif
let g:loaded_rpc_init = 1
"=====Initializing ........ variables ........."

if has("python3")
	let g:py_enable = "python3"
elseif has("python")
	let g:py_enable = "python"
else
	finish
endif

"=====Initializing ........Default Variables ........."
if !exists('g:rpc_bind_port')
    let g:rpc_bind_port=1700
endif

if !exists('g:rpc_bind_address')
    let g:rpc_bind_address='foreign'
endif

if !exists('g:rpc_proto')
    let g:rpc_proto = 'json'
endif
if !exists('g:rpc_client_conn')
    let g:rpc_client_conn = 3
endif
"=======end Initializing....."
"
if g:py_enable =='python3'
    command! -nargs=1 -complete=file PyCall :py3file <args>
    command! -nargs=+   PyMe   :py3  <args>
elseif  g:py_enable =='python'
    command! -nargs=1 -complete=file PyCall :pyfile <args>
    command! -nargs=+   PyMe   :py   <args>
else
    echo 'error'
endif
"
"PATH SETUP
let PY_Sc = globpath(&rtp, 'rpcscripts/')
let py_home = split(PY_Sc, '\n')
PyMe import sys, vim
PyMe sys.path = vim.eval('py_home') + sys.path

"
let myproto=g:rpc_proto
if myproto == 'json'
    PyMe from vimjson import VimRpc
elseif myproto == 'xml'
    PyMe from vimxml import VimRpc
else
    echohl Errormsg
    echo 'UNKWOWN RPC PROTOCOL.....exiting...'
    echohl None
    finish 
endif
"DESC: Initialize Python Class VimRpc
PyMe MainRpc = VimRpc()
"done
"
"........FunctionS
function RpcStarter()
"DESC: START RPC SERVER ON SUPPORTED PROTOCOLS
    echohl Character
    PyMe MainRpc._fork_serv()
    echohl None
    redraw
"
endfunction
".....
function RpcKiller()
"DESC: STOP RPC SERVER
    echohl Character
    PyMe MainRpc.kill_serv()
    echohl None
    redraw
endfunction

command  -nargs=0 StartRpc :call RpcStarter()
"
command  -nargs=0 StopRpc :call RpcKiller()
"
command -nargs=0 RestartRpc StopRpc | StartRpc
let buffname = expand('%:p')
let name = expand('~/.vim/fakepid.VimRpc')
if name == buffname
    try
        setlocal noswapfile
        setlocal buftype=nofile
        StartRpc
        redraw
        PyMe from writevimpid import writepid
        PyMe writepid('self')
        redraw
    catch
    endtry
endif
