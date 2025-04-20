// Grab DOM elements
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const audioPlayer = document.getElementById("audio-player");

let mediaRecorder;
let audioChunks = [];

// Start recording
startBtn.addEventListener("click", function() {
    startRecording();
    this.disabled = true;
    stopBtn.disabled = false;
});

// Stop recording
stopBtn.addEventListener("click", function() {
    stopRecording();
    this.disabled = true;
    startBtn.disabled = false;
});

// Start recording function
function startRecording() {
    console.log("Recording started...");

    // Access microphone and start recording
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioUrl; // Set audio player source to the recorded audio

                // Simulate sending the recorded audio to the backend
                const formData = new FormData();
                formData.append("audio_data", audioBlob, "user_input.wav");
                fetch("/upload", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    displayTranscription(data.transcription);
                    displayFeedback(data.feedback);
                })
                .catch(error => {
                    console.error("Error uploading audio:", error);
                    alert("Error uploading audio.");
                });
            };

            mediaRecorder.start();
        })
        .catch(error => {
            console.error("Error accessing microphone:", error);
            alert("Please allow microphone access to record audio.");
        });
}

// Stop recording function
function stopRecording() {
    console.log("Recording stopped...");
    mediaRecorder.stop();
}

// Display transcription
function displayTranscription(transcription) {
    document.getElementById("transcription-text").textContent = transcription;
}

// Display feedback
function displayFeedback(feedback) {
    document.getElementById("feedback-text").textContent = feedback;
}
