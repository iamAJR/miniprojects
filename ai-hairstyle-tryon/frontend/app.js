const video = document.getElementById('webcam');
const canvas = document.getElementById('snapshot-canvas');
const preview = document.getElementById('preview-image');
const btnStartCamera = document.getElementById('btn-start-camera');
const btnCapture = document.getElementById('btn-capture');
const btnRetake = document.getElementById('btn-retake');
const btnTryOn = document.getElementById('btn-tryon');
const btnReset = document.getElementById('btn-reset');
const fileUpload = document.getElementById('file-upload');
const uploadBtnLabel = document.querySelector('.upload-btn');

const presetCards = document.querySelectorAll('.preset-card');
const loadingOverlay = document.getElementById('loading-overlay');
const homeView = document.getElementById('home-view');
const resultView = document.getElementById('result-view');

const resultBefore = document.getElementById('result-before');
const resultAfter = document.getElementById('result-after');
const vibeRating = document.getElementById('vibe-rating');
const stylistNote = document.getElementById('stylist-note');

let stream = null;
let currentImageData = null;
let currentPreset = null;

// --- Camera & Upload Logic ---

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
        video.srcObject = stream;
        btnStartCamera.classList.add('hidden');
        uploadBtnLabel.classList.add('hidden');
        btnCapture.classList.remove('hidden');
        preview.classList.add('hidden');
        video.style.display = 'block';
    } catch (err) {
        console.error("Error accessing camera: ", err);
        alert("Could not access camera. Please use photo upload.");
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

function captureSnapshot() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    
    // Draw mirrored if facing mode is user
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Get base64 string
    const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
    setImage(dataUrl);
    
    stopCamera();
    video.style.display = 'none';
    btnCapture.classList.add('hidden');
    btnRetake.classList.remove('hidden');
}

function handleFileUpload(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            setImage(event.target.result);
            stopCamera();
            video.style.display = 'none';
            btnStartCamera.classList.add('hidden');
            uploadBtnLabel.classList.add('hidden');
            btnRetake.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

function setImage(dataUrl) {
    currentImageData = dataUrl;
    preview.src = dataUrl;
    preview.classList.remove('hidden');
    checkReady();
}

function resetInput() {
    currentImageData = null;
    preview.src = "";
    preview.classList.add('hidden');
    btnRetake.classList.add('hidden');
    btnStartCamera.classList.remove('hidden');
    uploadBtnLabel.classList.remove('hidden');
    checkReady();
}

// --- Preset Logic ---

function selectPreset(e) {
    presetCards.forEach(c => c.classList.remove('selected'));
    const card = e.currentTarget;
    card.classList.add('selected');
    currentPreset = card.dataset.preset;
    checkReady();
}

function checkReady() {
    if (currentImageData && currentPreset) {
        btnTryOn.disabled = false;
    } else {
        btnTryOn.disabled = true;
    }
}

// --- API Logic ---

async function doTryOn() {
    // Show loading
    loadingOverlay.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/tryon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: currentImageData,
                preset_id: currentPreset
            })
        });
        
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'API request failed');
        }
        
        const data = await response.json();
        
        // Show result
        resultBefore.src = currentImageData;
        resultAfter.src = data.transformed_image;
        vibeRating.innerText = data.vibe_rating;
        stylistNote.innerText = `"${data.stylist_note}"`;
        
        homeView.classList.add('hidden');
        resultView.classList.remove('hidden');
        
    } catch (err) {
        console.error(err);
        alert(err.message || 'Something went wrong.');
    } finally {
        loadingOverlay.classList.add('hidden');
    }
}

function resetApp() {
    resultView.classList.add('hidden');
    homeView.classList.remove('hidden');
    // Keep the selfie, clear the preset
    presetCards.forEach(c => c.classList.remove('selected'));
    currentPreset = null;
    checkReady();
}

// --- Event Listeners ---

btnStartCamera.addEventListener('click', startCamera);
btnCapture.addEventListener('click', captureSnapshot);
btnRetake.addEventListener('click', resetInput);
fileUpload.addEventListener('change', handleFileUpload);

presetCards.forEach(card => card.addEventListener('click', selectPreset));
btnTryOn.addEventListener('click', doTryOn);
btnReset.addEventListener('click', resetApp);
