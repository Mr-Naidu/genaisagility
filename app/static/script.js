function showLoader(type) {
    document.querySelector(`#${type}-btn span`).style.display = 'none';
    document.getElementById(`${type}-loader`).style.display = 'block';
    
    // Disable all buttons while processing
    document.getElementById('classify-btn').disabled = true;
    document.getElementById('rewrite-btn').disabled = true;
    hideResult();
}

function hideLoader(type) {
    document.querySelector(`#${type}-btn span`).style.display = 'block';
    document.getElementById(`${type}-loader`).style.display = 'none';
    
    // Re-enable all buttons
    document.getElementById('classify-btn').disabled = false;
    document.getElementById('rewrite-btn').disabled = false;
}

function showResult(title, content, isError = false) {
    const box = document.getElementById('result-box');
    const titleEl = document.getElementById('result-title');
    const contentEl = document.getElementById('result-content');
    
    box.style.display = 'block';
    if (isError) {
        box.classList.add('error');
        titleEl.textContent = 'Error';
    } else {
        box.classList.remove('error');
        titleEl.textContent = title;
    }
    
    contentEl.innerHTML = content;
}

function hideResult() {
    document.getElementById('result-box').style.display = 'none';
}

async function classifyEmail() {
    const content = document.getElementById('email-content').value.trim();
    if (!content) return alert('Please enter email content.');
    
    showLoader('classify');
    
    try {
        const response = await fetch('/api/v1/classify_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email_content: content })
        });
        
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.detail || 'Failed to classify');
        
        const confidencePercent = Math.round(data.confidence * 100);
        const resultHTML = `
            <strong>Category:</strong> ${data.category} <span class="badge">${confidencePercent}% Confidence</span><br><br>
            <strong>Reasoning:</strong> ${data.reasoning}
        `;
        
        showResult('Classification Complete', resultHTML);
    } catch (error) {
        showResult('Error', error.message, true);
    } finally {
        hideLoader('classify');
    }
}

async function rewriteEmail() {
    const content = document.getElementById('email-content').value.trim();
    const tone = document.getElementById('tone-select').value;
    
    if (!content) return alert('Please enter email content.');
    
    showLoader('rewrite');
    
    try {
        const response = await fetch('/api/v1/rewrite_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email_content: content, desired_tone: tone })
        });
        
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.detail || 'Failed to rewrite');
        
        const resultHTML = `
            <strong>Original Tone:</strong> <span class="badge">${data.original_tone}</span><br><br>
            <strong>Rewritten Email:</strong><br>
            <div style="margin-top:0.5rem; padding:1rem; background:rgba(0,0,0,0.2); border-radius:8px;">
                ${data.rewritten_content}
            </div>
        `;
        
        showResult('Rewrite Complete', resultHTML);
    } catch (error) {
        showResult('Error', error.message, true);
    } finally {
        hideLoader('rewrite');
    }
}
