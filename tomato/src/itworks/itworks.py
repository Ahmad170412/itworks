# itworks.py

__version__ = "1.0.0"
__all__ = ['throw', 'catch', 'peek', 'lazy', 'engine']

def throw(filepath, data):
# Write data to a file (Python -> Browser)
    
    try:
        with open(filepath, "w", encoding="utf-8") as shot:
            shot.write(str(data))
    except FileNotFoundError:
        raise OSError(f"itworks.throw(): Directory doesn't exist for '{filepath}'. Use full path or create directory first.")
    except PermissionError:
        raise OSError(f"itworks.throw(): Permission denied for '{filepath}'. Check file permissions.")
    except Exception as e:
        raise OSError(f"itworks.throw(): Unexpected error - {e}")


def catch(filepath):
# Read file and clear after read (Browser -> Python)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
        
        # Clear the file after reading (ONLY if there was data)
        if data:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("")
        return data if data else None
        
    except FileNotFoundError:
        # This is normal cos file might not exist yet because of js
        return None
    except PermissionError:
        print(f"itworks.catch(): Permission denied while reading '{filepath}'")
        return None
    except Exception as e:
        print(f"itworks.catch(): Unexpected ERROR - {e}")
        return None


def peek(filepath):
    # Read file WITHOUT clearing it (for debugging or smth)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read() or None
    except FileNotFoundError:
        return None


def lazy(from_js, to_js, output_html="index.html", poll_interval=500):
    # Generate HTML dashboard for LAZY users
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ItWorks Bridge</title>
    <style>
        :root {{
            --bg-color: #f4f7f6;
            --input-border-color: #4a90e2;
            --output-border-color: #e06c75;
            --button-bg-color: #333333;
            --button-text-color: #ffffff;
            --input-placeholder-text: "Enter your input data here...";
            --output-placeholder-text: "Results will be displayed here after processing...";
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .container {{
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .toolbar {{
            display: flex;
            gap: 10px;
            justify-content: flex-start;
        }}

        button {{
            background-color: var(--button-bg-color);
            color: var(--button-text-color);
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        button:hover {{
            opacity: 0.9;
        }}

        button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .input-section {{
            border: 3px solid var(--input-border-color);
            border-radius: 8px;
            background-color: #ffffff;
            padding: 15px;
        }}

        .output-section {{
            border: 3px solid var(--output-border-color);
            border-radius: 8px;
            background-color: #ffffff;
            padding: 15px;
            min-height: 150px;
        }}

        textarea {{
            width: 100%;
            height: 120px;
            border: none;
            resize: vertical;
            font-size: 16px;
            outline: none;
            font-family: inherit;
        }}

        textarea::placeholder {{
            color: #999999;
        }}

        .output-content {{
            font-size: 16px;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #333333;
        }}

        .output-placeholder {{
            color: #999999;
            font-size: 16px;
            white-space: pre-wrap;
        }}

        .status {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}

        .status-off {{
            background-color: #e06c75;
            color: white;
        }}

        .status-on {{
            background-color: #4a90e2;
            color: white;
        }}
    </style>
</head>
<body>

<div class="container">
    
    <div class="toolbar">
        <button id="sendBtn" disabled>Send</button>
        <button id="connectBtn">Configure Folder</button>
        <button id="testBtn">Test Connection</button>
        <span id="status" class="status status-off">Disconnected</span>
    </div>

    <div class="input-section">
        <textarea id="inputData" placeholder="Enter your input data here..."></textarea>
    </div>

    <div class="output-section" id="outputSection">
        <div id="outputContent" class="output-placeholder">Results will be displayed here after processing...</div>
    </div>

</div>

<script>

let dirHandle;
const FROM_JS = '{from_js}';
const TO_JS = '{to_js}';
const POLL_MS = {poll_interval};
const connectBtn = document.getElementById('connectBtn');
const sendBtn = document.getElementById('sendBtn');
const testBtn = document.getElementById('testBtn');
const statusSpan = document.getElementById('status');
const inputArea = document.getElementById('inputData');
const outputDiv = document.getElementById('outputContent');

connectBtn.onclick = async () => {{
    try {{
        dirHandle = await window.showDirectoryPicker();
        statusSpan.innerText = 'Connected';
        statusSpan.className = 'status status-on';
        sendBtn.disabled = false;
        startListening();
        outputDiv.innerText = 'Waiting for data from Python...';
        outputDiv.className = 'output-content';
    }} catch (err) {{
        if (err.name !== 'AbortError') {{
            alert('Error: ' + err.message);
        }}
    }}
}};

sendBtn.onclick = async () => {{
    let text = inputArea.value;
    if (!text.trim()) {{
        alert('Type something first');
        return;
    }}
    try {{
        let file = await dirHandle.getFileHandle(FROM_JS, {{create: true}});
        let w = await file.createWritable();
        await w.write(text);
        await w.close();
        inputArea.value = '';
        outputDiv.innerText = 'Sent: ' + text + '\\nWaiting for Python...';
        outputDiv.className = 'output-content';
    }} catch (err) {{
        alert('Send error: ' + err.message);
    }}
}};

testBtn.onclick = async () => {{
    if (!dirHandle) {{
        alert('Connect a folder first');
        return;
    }}
    try {{
        let file = await dirHandle.getFileHandle(FROM_JS, {{create: true}});
        let w = await file.createWritable();
        await w.write('TEST from browser at ' + new Date().toLocaleTimeString());
        await w.close();
        outputDiv.innerText = 'Test message sent to Python';
        outputDiv.className = 'output-content';
    }} catch (err) {{
        alert('Test error: ' + err.message);
    }}
}};

async function startListening() {{
    let lastContent = '';
    setInterval(async () => {{
        try {{
            let file = await dirHandle.getFileHandle(TO_JS);
            let f = await file.getFile();
            let text = await f.text();
            if (text && text !== lastContent) {{
                lastContent = text;
                outputDiv.innerText = text;
                outputDiv.className = 'output-content';
            }}
        }} catch (e) {{
            // File not exists yet - that's fine
        }}
    }}, POLL_MS);
}}

if (!window.isSecureContext) {{
    statusSpan.innerText = 'HTTPS Required';
    statusSpan.className = 'status status-off';
    alert('Use localhost or HTTPS for File System API');
}}
</script>

</body>
</html>"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Generated {output_html}")
    return output_html


def engine(from_js, to_js, poll_interval=500):
# returns a minimal JS core engine for user to build their own UI
    
    return f"""
<script>
// ItWorks Engine - Minimal JS for file communication
const FROM_JS = '{from_js}';
const TO_JS = '{to_js}';
const POLL_MS = {poll_interval};

let dirHandle;

async function connect() {{
    dirHandle = await window.showDirectoryPicker();
    let last = "";
    setInterval(async () => {{
        try {{
            let file = await dirHandle.getFileHandle(TO_JS);
            let text = await (await file.getFile()).text();
            if (text && text !== last) {{
                last = text;
                if (window.onPythonMessage) window.onPythonMessage(text);
            }}
        }} catch(e) {{}}
    }}, POLL_MS);
}}

async function send(data) {{
    let file = await dirHandle.getFileHandle(FROM_JS, {{create: true}});
    let w = await file.createWritable();
    await w.write(String(data));
    await w.close();
}}
</script>
"""