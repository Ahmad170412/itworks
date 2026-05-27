# ItWorks

A ridiculously simple Python + Browser bridge using plain text files.

itworks lets Python and JavaScript communicate without any complex:

- servers
- sockets
- APIs
- Flask
- WebSockets
- dependencies

## It's perfect for:

- local dashboards
- automation tools
- browser + Python projects
- rapid and easy prototyping
- offline applications
- beginners who find Flask complicated
- people who find flask and javascript hard (Like me:))


## How It Works

**Communication uses 2 files only!**

from_js.txt - Browser writes, Python reads
to_js.txt - Python writes, Browser reads

**The flow:**

Browser -> from_js.txt -> Python
Python  -> to_js.txt   -> Browser

Python clears incoming messages after reading them to avoid complicated issues.

### Functions:

**itworks.throw(filepath, data)**

Write data from Python -> Browser.

Example:

```python
import itworks

itworks.throw("to_js.txt", "Hello from Python")
```

**itworks.catch(filepath)**

Read data from Browser -> Python.

Automatically clears the file after reading.

Returns:

message string if data exists
None if file is empty or missing

Example:

```python
import itworks

msg = itworks.catch("from_js.txt")

if msg:
    print(msg)
```

**itworks.peek(filepath)**

Read a file **WITHOUT** clearing it.

Useful for debugging.

Example:

```import itworks

print(itworks.peek("from_js.txt"))
```
**itworks.lazy(from_js, to_js, output_html="index.html", poll_interval=500)**

Automatically generates a full browser UI.

Includes:

input box
output panel
send button
folder picker
auto polling
connection tester

Example:

```python
import itworks

itworks.lazy(
    from_js="from_js.txt",
    to_js="to_js.txt"
)
```
This creates:

index.html

Open it in **Chrome for it to work**

**itworks.engine(from_js, to_js, poll_interval=500)**

Generates a **minimal** JavaScript engine for custom UIs.

Example:

```python
import itworks

js = itworks.engine(
    from_js="from_js.txt",
    to_js="to_js.txt"
)

with open("engine.html", "w") as f:
    f.write(js)
```
Full Example


```python
import time
import itworks

while True:
    msg = itworks.catch("from_js.txt")

    if msg:
        print("Browser:", msg)

        response = f"Python received: {msg}"
        itworks.throw("to_js.txt", response)

    time.sleep(0.5)
```

Browser UI generator:
```python
import itworks

itworks.lazy("from_js.txt", "to_js.txt")
```
Open the generated HTML in chrome file.


Browser Requirements

**ONLY Works in:**

Chrome
Edge
Chromium browsers

Does **NOT** fully work in Firefox.


### Error Handling

#### throw() raises OSError for:

missing directories
permission problems
unexpected write errors

#### catch() safely returns None on most failures.

Minimal Echo Example


```python
import time
import itworks

while True:
    msg = itworks.catch("from_js.txt")

    if msg:
        itworks.throw("to_js.txt", f"Echo: {msg}")

    time.sleep(0.5)
```
