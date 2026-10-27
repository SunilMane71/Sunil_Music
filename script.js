async function uploadAudio() {
    const fileInput = document.getElementById('audioFile');
    const statusText = document.getElementById('status');

    if (fileInput.files.length === 0) {
        alert("ದಯವಿಟ್ಟು ಮೊದಲು ಒಂದು ಆಡಿಯೋ ಫೈಲ್ ಸೆಲೆಕ್ಟ್ ಮಾಡಿ!");
        return;
    }

    const formData = new FormData();
    formData.append('audio_file', fileInput.files.get(0) || fileInput.files[0]);

    statusText.innerText = "Processing audio on backend server... Please wait ⏳";

    try {
        const response = await fetch('/api/process', {
    method: 'POST',
    body: formData
});

        if (!response.ok) {
            throw new Error('Server processing failed!');
        }

        // ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ಬ್ಲಬ್ (Blob) ರೆಡಿ ಮಾಡುವುದು
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'remix_output.mp3';
        document.body.appendChild(a);
        a.click();
        a.remove();

        statusText.innerText = "Success! Song downloaded successfully 🎉";
    } catch (error) {
        console.error(error);
        statusText.innerText = "Error: Something went wrong with the server!";
    }
}