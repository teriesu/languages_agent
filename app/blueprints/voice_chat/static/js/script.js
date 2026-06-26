let mediaRecorder;
let audioChunks = [];
let pendingAudioFile = null;
let pendingAudioFilename = '';

const recordButton = document.getElementById('recordButton');
const processAudioButton = document.getElementById('processAudioButton');
const statusText = document.getElementById('recordingStatus');
const lessonSelect = document.getElementById('lesson-select');
const audioFileInput = document.getElementById('audioFileInput');
const originalTextCard = document.getElementById('originalTextCard');
const feedbackCard = document.getElementById('feedbackCard');
const correctedTextCard = document.getElementById('correctedTextCard');
const originalTextContent = document.getElementById('originalTextContent');
const feedbackContent = document.getElementById('feedbackContent');
const correctedTextContent = document.getElementById('correctedTextContent');

function setStatus(message, color = 'red') {
    statusText.textContent = message;
    statusText.style.color = color;
    statusText.style.display = 'inline';
}

function clearStatus() {
    statusText.textContent = '';
    statusText.style.display = 'none';
}

function setPendingAudio(audioFile, filename) {
    pendingAudioFile = audioFile;
    pendingAudioFilename = filename;
    processAudioButton.disabled = !pendingAudioFile;
}

function clearPendingAudio() {
    pendingAudioFile = null;
    pendingAudioFilename = '';
    processAudioButton.disabled = true;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function normalizeToken(token) {
    const normalized = token.toLowerCase().replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
    return normalized || token.toLowerCase();
}

function getTokenStatuses(originalText, correctedText) {
    const originalTokens = originalText.split(/\s+/).filter(Boolean);
    const correctedTokens = correctedText.split(/\s+/).filter(Boolean);
    const originalLength = originalTokens.length;
    const correctedLength = correctedTokens.length;

    if (!originalLength || !correctedLength) {
        return new Array(originalLength).fill('incorrect');
    }

    const dp = Array.from({ length: originalLength + 1 }, () => new Array(correctedLength + 1).fill(0));

    for (let i = originalLength - 1; i >= 0; i -= 1) {
        for (let j = correctedLength - 1; j >= 0; j -= 1) {
            if (normalizeToken(originalTokens[i]) === normalizeToken(correctedTokens[j])) {
                dp[i][j] = dp[i + 1][j + 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i + 1][j], dp[i][j + 1]);
            }
        }
    }

    const statuses = new Array(originalLength).fill('incorrect');
    let i = 0;
    let j = 0;

    while (i < originalLength && j < correctedLength) {
        if (normalizeToken(originalTokens[i]) === normalizeToken(correctedTokens[j])) {
            statuses[i] = 'correct';
            i += 1;
            j += 1;
        } else if (dp[i + 1][j] >= dp[i][j + 1]) {
            statuses[i] = 'incorrect';
            i += 1;
        } else {
            j += 1;
        }
    }

    return statuses;
}

function renderOriginalText(originalText, correctedText) {
    const statuses = getTokenStatuses(originalText, correctedText);
    let tokenIndex = 0;

    return originalText
        .split(/(\s+)/)
        .map((segment) => {
            if (/^\s+$/.test(segment)) {
                return escapeHtml(segment);
            }

            const status = statuses[tokenIndex] || 'incorrect';
            tokenIndex += 1;
            const className = status === 'correct' ? 'voice-token--correct' : 'voice-token--incorrect';
            return `<span class="${className}">${escapeHtml(segment)}</span>`;
        })
        .join('');
}

function renderResult(result) {
    const originalText = result.transcription || '';
    const correctedText = result.corrected_text || '';

    originalTextContent.innerHTML = originalText ? renderOriginalText(originalText, correctedText) : '';
    feedbackContent.textContent = result.feedback || '';
    correctedTextContent.textContent = correctedText;

    originalTextCard.hidden = !originalText;
    feedbackCard.hidden = !feedbackContent.textContent;
    correctedTextCard.hidden = !correctedText;
}

recordButton.addEventListener('click', async () => {
if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordButton.textContent = "🎤 Start recording";
    setStatus("🎙️ Grabación lista para enviar.", "#8d79e0");
    return;
}

try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
            noiseSuppression: true,
            echoCancellation: true,
            autoGainControl: true  
        }
    });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
    if (event.data.size > 0) {
        audioChunks.push(event.data);
    }
    };

    mediaRecorder.onstop = async () => {

    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    audioChunks = [];
    setPendingAudio(audioBlob, 'user_audio.webm');
    };

    mediaRecorder.start();
    recordButton.textContent = "⏹ Stop recording";
    setStatus("🔴 Recording...", "#8d79e0");

} catch (err) {
    console.error("Error while accessing the microphone:", err);
    alert("Please allow access to the microphone to use the voice chat.");
}
});

audioFileInput.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
        return;
    }

    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!['webm', 'mp3'].includes(extension || '')) {
        alert('Please select a .webm or .mp3 audio file.');
        event.target.value = '';
        return;
    }

    setPendingAudio(file, file.name);
    setStatus(`📎 File ready: ${file.name}.`, '#5c8ed6');
});

processAudioButton.addEventListener('click', async () => {
    if (!pendingAudioFile) {
        alert('Please select or record an audio file first.');
        return;
    }

    await sendAudioToBackend(pendingAudioFile, pendingAudioFilename);
});

async function sendAudioToBackend(audioFile, filename) {
const formData = new FormData();
formData.append("audio_file", audioFile, filename);

if (lessonSelect && lessonSelect.value) {
    formData.append("lesson_id", lessonSelect.value);
}

try {

    const endpoint = (typeof processAudioUrl !== 'undefined') ? processAudioUrl : '/voice_chat/process_audio';
    processAudioButton.disabled = true;
    setStatus("📤 Sending the audio...", '#5c8ed6');
    const response = await fetch(endpoint, {
    method: "POST",
    body: formData
    });
    
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || 'Unable to process the audio.');
    }

    renderResult(result);
    clearPendingAudio();
    audioFileInput.value = '';
    setStatus("✅ Audio processed", "#8ca455");

} catch (err) {
    console.error("Error sending the audio:", err);
    setStatus(err.message || "Error while processing the audio", "red");
    processAudioButton.disabled = !pendingAudioFile;
}
}
