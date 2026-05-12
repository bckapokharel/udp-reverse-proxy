# Reverse Proxy Networking

Hi! I'm Bishika Pokharel (EUID: bp0797), and this is my reverse proxy
project for the networking class. It's written in Python.

## What this does

So the idea behind a reverse proxy is pretty simple. Normally a client
talks directly to a server. With a reverse proxy, the client only ever
talks to the proxy, and the proxy decides which actual server should
handle the request. The client has no idea there are multiple servers
behind the scenes.

In my version, the proxy uses a round-robin schedule. That just means
the first request goes to server 1, the second goes to server 2, the
third goes back to server 1, and so on. Pretty straightforward.

The whole thing runs over UDP, so packets can get lost. To make that
realistic (and to actually demonstrate the timeouts), my server randomly
drops about a third of the packets it receives. When that happens, the
proxy waits a bit, gives up, and the client eventually times out.

## What's in here

There are three Python files:

- `server.py` — a basic UDP server that replies "PONG" when you send it
  "PING". Drops some packets on purpose.
- `proxy.py` — the reverse proxy. This is the main thing for the
  assignment.
- `client.py` — sends 10 PINGs and prints what comes back.

Plus this README.

## What you need

Just Python 3. Nothing to install, nothing to download. I'm using
Python 3.14 on my Mac but anything 3.7 or newer should work fine.

To check what you have, run:python3 --version
## How to run it

You need four terminal tabs open. The reason is that the three server
programs (two servers + the proxy) all keep running and don't give you
your prompt back, so you can't share a tab with anything else.

On a Mac, press Cmd+T three times in Terminal to get four tabs total.

In **tab 1**, start the first server:
python3 server.py --port 8001
In **tab 2**, start the second server:
python3 server.py --port 8002
In **tab 3**, start the proxy and tell it about both servers:
python3 proxy.py --port 8000 --upstream 8001 8002
In **tab 4**, run the client:
python3 client.py --port 8000
The client will send 10 PINGs and then exit. The other three programs
will keep running until you stop them with Ctrl+C.

That's it!

## What you should see

The client will print something like this:
[client] Bishika Pokharel | EUID: bp0797
1  : sent PING... received  b'PONG via 8001 [0]'
2  : sent PING... Timed Out
3  : sent PING... received  b'PONG via 8002 [1]'
4  : sent PING... received  b'PONG via 8001 [0]'
5  : sent PING... Timed Out
The `via 8001 [0]` part is the proxy telling you which server actually
handled that request. `8001` is the port and `[0]` is its position in
the upstream list. So a reply tagged `[0]` came from the first server,
`[1]` came from the second, and so on.

The "Timed Out" lines happen when the server I'm randomly picking
decided to drop that packet. That's the whole point of running things
over UDP — packet loss is a real thing.

In the server tabs, you'll see lines like `[client] : PING` when a
packet got through, and `[server] : packet dropped` when it didn't.

The proxy tab is pretty quiet — it just shows that it's ready and then
sits there doing its job.

## A couple of notes

If you want to use more than two servers, just add more ports to the
upstream list:
python3 proxy.py --port 8000 --upstream 8001 8002 8003 8004
The proxy will round-robin across all of them.

If you ever see "Address already in use" when starting a server, that
means an old run is still hanging around on that port. The fix:
lsof -i :8001
kill -9 <PID>
Or just close that terminal tab and open a new one.

## How to stop

Press Ctrl+C in each of the three running tabs (the two servers and
the proxy). The client stops on its own after 10 PINGs.

Thanks for reading!
