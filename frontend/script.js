const UPLOAD_URL = "http://127.0.0.1:8000/api/documents/upload";
const ASK_URL = "http://127.0.0.1:8000/api/documents/ask";

const uploadForm = document.getElementById("uploadForm");
const pdfFile = document.getElementById("pdfFile");
const uploadStatus = document.getElementById("uploadStatus");

const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const chatBox = document.getElementById("chatBox");


/* ---------------------------
   Add message to chat
---------------------------- */
function addMessage(content, className) {
    const message = document.createElement("div");
    message.className = `message ${className}`;
    message.textContent = content;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}


/* ---------------------------
   Upload PDF
---------------------------- */
uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = pdfFile.files[0];
    if (!file) return;

    const submitButton = uploadForm.querySelector("button");
    const formData = new FormData();

    formData.append("file", file);

    uploadStatus.textContent = "Uploading and indexing document...";
    submitButton.disabled = true;

    try {
        const response = await fetch(UPLOAD_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const data = await response.json();

        uploadStatus.textContent = `${data.message} Chunks created: ${data.chunks_created}`;

        addMessage(
            `Document uploaded: ${data.filename}`,
            "bot-message"
        );

    } catch (error) {
        uploadStatus.textContent = "Failed to upload document. Please try again.";
    } finally {
        submitButton.disabled = false;
    }
});


/* ---------------------------
   Ask Question
---------------------------- */
questionForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, "user-message");
    questionInput.value = "";

    const loadingMessage = addMessage(
        "Searching document and generating answer...",
        "bot-message"
    );

    const submitButton = questionForm.querySelector("button");
    submitButton.disabled = true;

    try {
        const response = await fetch(ASK_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error("Question request failed");
        }

        const data = await response.json();

        // Show answer
        loadingMessage.textContent = data.answer;

        // Show sources if available
        if (data.sources && data.sources.length > 0) {
            const sourceText = data.sources
                .map((source, index) => {
                    return `Source ${index + 1}: ${source.source || "Unknown"}, Page ${source.page || "N/A"}`;
                })
                .join("\n");

            addMessage(sourceText, "source-message");
        }

    } catch (error) {
        loadingMessage.textContent =
            "Sorry, I could not answer this question right now.";
        loadingMessage.classList.add("error-message");

    } finally {
        submitButton.disabled = false;
        questionInput.focus();
    }
});