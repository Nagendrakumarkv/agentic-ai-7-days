const chatHistory = [];
let currentFiles = [];

const historyDiv = document.getElementById('chat-history');
const inputDiv = document.getElementById('prompt-input');
const generateBtn = document.getElementById('generate-btn');
const tabs = document.querySelectorAll('.tab-btn');
const contents = document.querySelectorAll('.tab-content');
const fileBrowser = document.getElementById('file-browser');
const codeContent = document.getElementById('code-content');
const previewFrame = document.getElementById('preview-frame');

// Setup Tabs
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
    });
});

function appendMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = `message ${role}-msg`;
    msg.innerText = text;
    historyDiv.appendChild(msg);
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

function showLoading() {
    const ld = document.createElement('div');
    ld.className = `loading`;
    ld.id = `typing-indicator`;
    ld.innerHTML = `<div class="dot"></div><div class="dot"></div><div class="dot"></div>`;
    historyDiv.appendChild(ld);
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

function removeLoading() {
    const ld = document.getElementById('typing-indicator');
    if (ld) ld.remove();
}

function renderFileTree() {
    fileBrowser.innerHTML = '';
    currentFiles.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.innerText = file.path;
        div.onclick = () => selectFile(index);
        fileBrowser.appendChild(div);
    });
}

function selectFile(index) {
    document.querySelectorAll('.file-item').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.file-item')[index].classList.add('active');
    const ext = currentFiles[index].path.split('.').pop();
    codeContent.innerText = currentFiles[index].content;
}

generateBtn.addEventListener('click', async () => {
    const prompt = inputDiv.value.trim();
    if (!prompt) return;

    appendMessage('user', prompt);
    inputDiv.value = '';
    generateBtn.disabled = true;
    showLoading();

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                prompt: prompt,
                chat_history: chatHistory
            })
        });

        const data = await response.json();
        removeLoading();

        if (response.ok) {
            appendMessage('ai', "Project updated successfully!");
            
            // Push to chat history state
            chatHistory.push({role: "user", content: prompt});
            // Let the AI remember its own generated output so it can confidently iterate
            chatHistory.push({role: "model", content: data.raw_text});

            // Update UI
            currentFiles = data.files;
            renderFileTree();
            if (currentFiles.length > 0) {
                selectFile(0);
            }

            // Update iframe cache bust
            previewFrame.src = data.sandbox_url + "/docs?t=" + new Date().getTime(); 
            
            // Switch to preview tab automatically
            tabs[1].click();

        } else {
            appendMessage('system', "Error: " + data.detail);
        }
    } catch (e) {
        console.error(e);
        removeLoading();
        appendMessage('system', "Error connecting to server. Is it running?");
    }

    generateBtn.disabled = false;
});
