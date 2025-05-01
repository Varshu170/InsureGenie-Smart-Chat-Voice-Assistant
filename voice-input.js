document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const voiceInputButton = document.getElementById('voice-input-button');

    if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser does not support speech recognition. Please try using Chrome.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false; // Stop recognition after one result
    recognition.interimResults = false; // No need for interim results

    recognition.onstart = function () {
        voiceInputButton.classList.add('recording');
        console.log('Voice recognition started');
    };

    recognition.onend = function () {
        voiceInputButton.classList.remove('recording');
        console.log('Voice recognition ended');
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error:', event.error);
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        searchInput.value = transcript;
        console.log('Recognized text:', transcript);
    };

    voiceInputButton.addEventListener('click', function () {
        recognition.start();
    });
});
