let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('recordingStatus');
const lessonSelect = document.getElementById('lesson-select');

recordButton.addEventListener('click', async () => {
if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordButton.textContent = "🎤 Iniciar Grabación";
    statusText.style.display = "none";
    return;
}

try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
    if (event.data.size > 0) {
        audioChunks.push(event.data);
    }
    };

    mediaRecorder.onstop = async () => {

    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    audioChunks = [];
    await sendAudioToBackend(audioBlob);
    };

    mediaRecorder.start();
    recordButton.textContent = "⏹ Stop recording";
    statusText.style.display = "inline";

} catch (err) {
    console.error("Error while accessing the microphone:", err);
    alert("Please allow access to the microphone to use the voice chat.");
}
});

async function sendAudioToBackend(audioBlob) {
const formData = new FormData();
formData.append("audio_file", audioBlob, "user_audio.webm");

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

    
} catch (err) {
    console.error("Error sending the audio:", err);
}
}