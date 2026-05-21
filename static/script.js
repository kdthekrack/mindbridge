// ======================================================
// DOM ELEMENTS
// ======================================================

const chatWindow =
    document.getElementById(
        "chat-window"
    );

const messageInput =
    document.getElementById(
        "message-input"
    );

const sendButton =
    document.getElementById(
        "send-button"
    );

const typingIndicator =
    document.getElementById(
        "typing-indicator"
    );

const crisisBanner =
    document.getElementById(
        "crisis-banner"
    );

// ======================================================
// SEND MESSAGE
// ======================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    // ==================================================
    // VALIDATION
    // ==================================================

    if (!message) {

        return;
    }

    // ==================================================
    // USER MESSAGE UI
    // ==================================================

    addMessage({

        type: "user",

        text: message
    });

    // ==================================================
    // CLEAR INPUT
    // ==================================================

    messageInput.value = "";

    // ==================================================
    // SHOW TYPING
    // ==================================================

    showTyping();

    try {

        // ==============================================
        // API REQUEST
        // ==============================================

        const response = await fetch(

            "/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    username: username,

                    message: message
                })
            }
        );

        const data =
            await response.json();

        // ==============================================
        // HIDE TYPING
        // ==============================================

        hideTyping();

        // ==============================================
        // ERROR HANDLING
        // ==============================================

        if (!data.success) {

            addMessage({

                type: "bot",

                text:
                    "Something went wrong. "
                    + "Please try again."
            });

            return;
        }

        // ==============================================
        // CRISIS MODE
        // ==============================================

        if (data.crisis) {

            showCrisisBanner();

        } else {

            hideCrisisBanner();
        }

        // ==============================================
        // BOT MESSAGE
        // ==============================================

        addMessage({

            type: "bot",

            text: data.reply,

            emotion: data.emotion,

            support: data.support
        });

    } catch (error) {

        console.error(error);

        hideTyping();

        addMessage({

            type: "bot",

            text:
                "Connection issue. "
                + "Please try again."
        });
    }
}

// ======================================================
// ADD MESSAGE
// ======================================================

function addMessage({

    type,
    text,
    emotion = null,
    support = null
}) {

    // ==================================================
    // WRAPPER
    // ==================================================

    const messageWrapper =
        document.createElement("div");

    messageWrapper.classList.add(
        "message"
    );

    if (type === "user") {

        messageWrapper.classList.add(
            "user-message"
        );

    } else {

        messageWrapper.classList.add(
            "bot-message"
        );
    }

    // ==================================================
    // AVATAR
    // ==================================================

    const avatar =
        document.createElement("div");

    avatar.classList.add(
        "message-avatar"
    );

    avatar.textContent =
        type === "user"
            ? "🧑"
            : "🧠";

    // ==================================================
    // CONTENT
    // ==================================================

    const content =
        document.createElement("div");

    content.classList.add(
        "message-content"
    );

    // ==================================================
    // BUBBLE
    // ==================================================

    const bubble =
        document.createElement("div");

    bubble.classList.add(
        "message-bubble"
    );

    bubble.innerHTML =
        formatMessage(text);

    content.appendChild(bubble);

    // ==================================================
    // EMOTION TAG
    // ==================================================

    if (emotion && type === "bot") {

        const emotionTag =
            document.createElement("div");

        emotionTag.classList.add(
            "emotion-tag"
        );

        emotionTag.innerHTML =
            `Emotion detected: <strong>${emotion}</strong>`;

        content.appendChild(
            emotionTag
        );
    }

    // ==================================================
    // CBT SUPPORT
    // ==================================================

    if (support && type === "bot") {

        const supportCard =
            createSupportCard(
                support
            );

        content.appendChild(
            supportCard
        );
    }

    // ==================================================
    // ASSEMBLE
    // ==================================================

    if (type === "user") {

        messageWrapper.appendChild(
            content
        );

        messageWrapper.appendChild(
            avatar
        );

    } else {

        messageWrapper.appendChild(
            avatar
        );

        messageWrapper.appendChild(
            content
        );
    }

    chatWindow.appendChild(
        messageWrapper
    );

    // ==================================================
    // AUTO SCROLL
    // ==================================================

    scrollToBottom();
}

// ======================================================
// SUPPORT CARD
// ======================================================

function createSupportCard(
    support
) {

    const card =
        document.createElement("div");

    card.classList.add(
        "support-card"
    );

    card.innerHTML = `

        <div class="support-title">

            💡 ${support.title}

        </div>

        <div class="support-tip">

            ${support.tip}

        </div>

        <div class="support-exercise">

            ${support.exercise}

        </div>
    `;

    return card;
}

// ======================================================
// FORMAT MESSAGE
// ======================================================

function formatMessage(text) {

    return text.replace(
        /\\n/g,
        "<br>"
    );
}

// ======================================================
// TYPING INDICATOR
// ======================================================

function showTyping() {

    typingIndicator.style.display =
        "flex";

    scrollToBottom();
}

function hideTyping() {

    typingIndicator.style.display =
        "none";
}

// ======================================================
// CRISIS BANNER
// ======================================================

function showCrisisBanner() {

    crisisBanner.style.display =
        "block";
}

function hideCrisisBanner() {

    crisisBanner.style.display =
        "none";
}

// ======================================================
// AUTO SCROLL
// ======================================================

function scrollToBottom() {

    chatWindow.scrollTop =
        chatWindow.scrollHeight;
}

// ======================================================
// ENTER KEY
// ======================================================

messageInput.addEventListener(

    "keydown",

    function(event) {

        if (
            event.key === "Enter"
        ) {

            sendMessage();
        }
    }
);

// ======================================================
// BUTTON CLICK
// ======================================================

sendButton.addEventListener(

    "click",

    sendMessage
);

// ======================================================
// INITIAL FOCUS
// ======================================================

messageInput.focus();