let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('recordingStatus');
const lessonSelect = document.getElementById('lesson-select');
const audioFileInput = document.getElementById('audioFileInput');

recordButton.addEventListener('click', async () => {
if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordButton.textContent = "🎤 Start Recording";
    statusText.style.display = "none";
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
    await sendAudioToBackend(audioBlob, 'user_audio.webm');
    };

    mediaRecorder.start();
    recordButton.textContent = "⏹ Stop recording";
    statusText.textContent = "🔴 Grabando...";
    statusText.style.display = "inline";

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

    statusText.textContent = "📤 Enviando archivo...";
    statusText.style.display = "inline";
    await sendAudioToBackend(file, file.name);
    event.target.value = '';
});

async function sendAudioToBackend(audioFile, filename) {
const formData = new FormData();
formData.append("audio_file", audioFile, filename);

if (lessonSelect && lessonSelect.value) {
    formData.append("lesson_id", lessonSelect.value);
}

try {

    const endpoint = (typeof processAudioUrl !== 'undefined') ? processAudioUrl : '/voice_chat/process_audio';
    const response = await fetch(endpoint, {
    method: "POST",
    body: formData
    });
    
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || 'Unable to process the audio.');
    }

    statusText.textContent = "✅ Audio procesado";
    statusText.style.color = "green";
    statusText.style.display = "inline";

} catch (err) {
    console.error("Error sending the audio:", err);
    statusText.textContent = err.message || "Error al procesar el audio";
    statusText.style.color = "red";
    statusText.style.display = "inline";
}
}