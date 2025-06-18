document.addEventListener("DOMContentLoaded", () => {
    const promptInput = document.getElementById("promptInput");
    const generateButton = document.getElementById("generateButton");
    const resultSection = document.getElementById("resultSection");

    const generateImage = async () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert("Please enter a prompt!");
            return;
        }

        // --- Start Loading State ---
        generateButton.disabled = true;
        generateButton.innerHTML = '<i class="fa-solid fa-hourglass-half"></i> Generating...';
        resultSection.innerHTML = '<div class="loader"></div>';
        resultSection.style.borderColor = "var(--primary-color)";

        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt }),
            });

            const data = await response.json();

            if (!response.ok) {
                // Display error from the server
                throw new Error(data.error || "An unknown error occurred.");
            }

            // --- Display Result ---
            resultSection.innerHTML = `
                <div class="image-wrapper">
                    <img src="${data.image_url}" alt="Generated image for: ${prompt}">
                    <a href="${data.image_url}" class="download-button" download>
                        <i class="fa-solid fa-download"></i> Download Image
                    </a>
                </div>
            `;

        } catch (error) {
            console.error("Error:", error);
            resultSection.innerHTML = `<div class="placeholder"><p style="color:red;">Error: ${error.message}</p></div>`;
            resultSection.style.borderColor = "red";
        } finally {
            // --- End Loading State ---
            generateButton.disabled = false;
            generateButton.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate';
        }
    };

    generateButton.addEventListener("click", generateImage);
    promptInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            generateImage();
        }
    });
});