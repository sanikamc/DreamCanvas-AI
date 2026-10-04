
const promptInput = document.getElementById("prompt");
const generateBtn = document.getElementById("generateBtn");
const statusText = document.getElementById("status");
const resultDiv = document.getElementById("result");
const charCount = document.getElementById("charCount");
const historyGallery = document.getElementById("historyGallery");

const API_URL = "http://127.0.0.1:5000";

// Character counter
promptInput.addEventListener("input", () => {
    charCount.textContent = `${promptInput.value.length} / 1000`;
});


// Generate image
generateBtn.addEventListener("click", async () => {

    const prompt = promptInput.value.trim();

    if (!prompt) {
        statusText.textContent = "Please enter a description first!";
        return;
    }

    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
    statusText.textContent = "✨ Creating your artwork. Please wait...";

    resultDiv.innerHTML = `
        <div class="placeholder">
            <span>⏳</span>
            <h3>Creating your artwork...</h3>
            <p>This may take a little time.</p>
        </div>
    `;

    try {

        const response = await fetch(`${API_URL}/api/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt: prompt })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Image generation failed.");
        }

        const imageUrl = `${API_URL}${data.image_url}`;

        resultDiv.innerHTML = `
            <div class="generated-result">

                <img
                    src="${imageUrl}"
                    class="generated-image"
                    alt="Generated artwork"
                >

                <br>

                <button id="downloadBtn" class="download-btn">
                    ⬇ Download Image
                </button>

            </div>
        `;

        // Download newly generated image
        document.getElementById("downloadBtn").addEventListener("click", async () => {
            await downloadImage(imageUrl, "DreamCanvas_AI.png");
        });

        statusText.textContent = "🎉 Your image has been generated!";

        // Refresh image history
        loadHistory();

    } catch (error) {

        statusText.textContent = "Error: " + error.message;

        resultDiv.innerHTML = `
            <div class="placeholder">
                <span>⚠️</span>
                <h3>Generation unsuccessful</h3>
                <p>Please check the backend and try again.</p>
            </div>
        `;

    } finally {

        generateBtn.disabled = false;
        generateBtn.textContent = "✦ Generate Image";

    }

});


// Download image function
async function downloadImage(imageUrl, filename) {

    try {

        const response = await fetch(imageUrl);

        if (!response.ok) {
            throw new Error("Could not download image.");
        }

        const imageBlob = await response.blob();
        const downloadUrl = URL.createObjectURL(imageBlob);

        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = filename;

        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => {
            URL.revokeObjectURL(downloadUrl);
        }, 1000);

    } catch (error) {

        statusText.textContent = "Download failed: " + error.message;

    }

}


// Load image history
async function loadHistory() {

    try {

        const response = await fetch(`${API_URL}/api/history`);

        if (!response.ok) {
            throw new Error("Could not load history.");
        }

        const images = await response.json();

        if (images.length === 0) {

            historyGallery.innerHTML = `
                <div class="empty-gallery">
                    <span>✦</span>
                    <h3>No creations yet</h3>
                    <p>Your AI-generated artwork will appear here.</p>
                </div>
            `;

            return;
        }

        historyGallery.innerHTML = images.map((image, index) => {

            const imageUrl = `${API_URL}${image.image_url}`;

            return `
                <div class="gallery-card">

                    <img
                        src="${imageUrl}"
                        alt="AI generated artwork"
                        class="gallery-image"
                    >

                    <div class="gallery-info">

                        <span class="image-number">
                            CREATION ${index + 1}
                        </span>

                        <p class="gallery-prompt">
                            ${escapeHTML(image.prompt)}
                        </p>

                        <button
                            class="gallery-download"
                            data-index="${index}"
                        >
                            ⬇ Download
                        </button>

                    </div>

                </div>
            `;

        }).join("");

        // Add download events to history cards
        historyGallery.querySelectorAll(".gallery-download").forEach(button => {

            button.addEventListener("click", async () => {

                const image = images[Number(button.dataset.index)];

                if (image) {
                    await downloadImage(
                        `${API_URL}${image.image_url}`,
                        `DreamCanvas_Creation_${Number(button.dataset.index) + 1}.png`
                    );
                }

            });

        });

    } catch (error) {

        console.error("History error:", error);

    }

}


// Safely display prompt text
function escapeHTML(text) {

    const element = document.createElement("div");

    element.textContent = text;

    return element.innerHTML;

}


// Load history when page opens
loadHistory();