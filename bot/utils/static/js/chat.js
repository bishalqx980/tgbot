const socket = io();

const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

const memberList = document.getElementById("memberList");
const memberCount = document.getElementById("memberCount");

const typingIndicator = document.getElementById("typingIndicator");

const connectionDot = document.getElementById("connectionDot");
const connectionText = document.getElementById("connectionText");

const clearChat = document.getElementById("clearChat");

const copyRoom = document.getElementById("copyRoom");
const leaveRoom = document.getElementById("leaveRoom");

const fileInput = document.getElementById("fileInput");
const fileButton = document.getElementById("fileButton");

const uploadPreview = document.getElementById("uploadPreview");
const uploadInfo = document.getElementById("uploadInfo");
const cancelUpload = document.getElementById("cancelUpload");

const passwordModal = document.getElementById("passwordModal");
const roomPasswordInput = document.getElementById("roomPasswordInput");
const passwordCancel = document.getElementById("passwordCancel");
const passwordJoin = document.getElementById("passwordJoin");

const notification = document.getElementById("notification");
const notificationTitle = document.getElementById("notificationTitle");
const notificationMessage = document.getElementById("notificationMessage");


let typingTimeout = null;
let typingUsers = new Set();
let selectedFile = null;
let clearCooldown = false;

const initialParams = new URLSearchParams(
    window.location.search
);

let roomPassword = initialParams.get("password") || "";


socket.on("connect", () => {
    connectionDot.classList.add("connected");
    connectionText.textContent = "Connected";

    joinCurrentRoom();
});


socket.on("disconnect", () => {
    connectionDot.classList.remove("connected");
    connectionText.textContent = "Disconnected";
});


socket.on("connect_error", () => {
    connectionText.textContent = "Reconnecting";
});


function joinCurrentRoom() {
    socket.emit("join", {
        name: USER_NAME,
        room: ROOM_ID,
        password: ROOM_ID === "127.0.0.1"
            ? ""
            : roomPassword,
        admin: IS_ADMIN
    });
}


socket.on("join_error", data => {
    showNotification(
        "Unable to Join",
        data.message,
        "error"
    );

    setTimeout(() => {
        window.location.href = "/";
    }, 1500);
});


socket.on("password_required", () => {
    passwordModal.classList.remove("hidden");
    roomPasswordInput.value = "";
    roomPasswordInput.focus();
});


socket.on("wrong_password", data => {
    passwordModal.classList.remove("hidden");

    roomPasswordInput.value = "";
    roomPasswordInput.focus();

    showNotification(
        "Wrong Password",
        data.message,
        "error"
    );
});


socket.on("room_joined", data => {
    updateMembers(data.members);

    showNotification(
        "Connected",
        `You joined room ${data.room}`,
        "success"
    );
});


socket.on("user_joined", data => {
    updateMembers(data.members);

    addSystemMessage(
        `${data.name} joined the room`
    );
});


socket.on("user_left", data => {
    updateMembers(data.members);

    addSystemMessage(
        `${data.name} left the room`
    );
});


socket.on("new_message", data => {
    addMessage(data);
});


socket.on("new_file", data => {
    addFileMessage(data);
});


socket.on("typing", data => {
    if (data.typing) {
        typingUsers.add(data.name);
    } else {
        typingUsers.delete(data.name);
    }

    updateTypingIndicator();
});


socket.on("chat_cleared", data => {
    messages.innerHTML = "";

    typingUsers.clear();

    updateTypingIndicator();

    addSystemMessage(
        `${data.name} cleared the chat`
    );

    showNotification(
        "Chat Cleared",
        `${data.name} cleared the chat for everyone.`,
        "success"
    );
});


socket.on("clear_cooldown", data => {
    clearCooldown = true;

    showNotification(
        "Please Wait",
        `You need to wait ${data.remaining} seconds before clearing the chat again.`,
        "warning"
    );
});


socket.on("upload_error", data => {
    showNotification(
        "Upload Failed",
        data.message,
        "error"
    );

    selectedFile = null;

    uploadPreview.classList.add("hidden");

    fileInput.value = "";
});


socket.on("kicked", data => {
    showNotification(
        "Removed",
        data.message,
        "error"
    );

    setTimeout(() => {
        window.location.href = "/";
    }, 1500);
});


function showNotification(title, message, type = "info") {
    notification.className = `notification ${type}`;

    notificationTitle.textContent = title;
    notificationMessage.textContent = message;

    notification.classList.add("show");

    clearTimeout(window.notificationTimeout);

    window.notificationTimeout = setTimeout(() => {
        notification.classList.remove("show");
    }, 4000);
}


function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    socket.emit("send_message", {
        message: message
    });

    messageInput.value = "";

    socket.emit("typing", {
        typing: false
    });
}


function addMessage(data) {
    removeWelcome();

    const messageElement = document.createElement("div");

    messageElement.className = "message";

    if (data.name === USER_NAME) {
        messageElement.classList.add("own");
    }

    const name = document.createElement("strong");

    let displayName = data.name;

    if (data.name === USER_NAME) {
        displayName += " (You)";
    }

    if (data.admin) {
        displayName += " • ADMIN";
    }

    name.textContent = displayName;

    const text = document.createElement("p");

    text.textContent = data.message;

    messageElement.appendChild(name);
    messageElement.appendChild(text);

    messages.appendChild(messageElement);

    scrollMessages();
}


function addFileMessage(data) {
    removeWelcome();

    const messageElement = document.createElement("div");

    messageElement.className = "message file-message";

    if (data.name === USER_NAME) {
        messageElement.classList.add("own");
    }

    const name = document.createElement("strong");

    let displayName = data.name;

    if (data.name === USER_NAME) {
        displayName += " (You)";
    }

    if (data.admin) {
        displayName += " • ADMIN";
    }

    name.textContent = displayName;

    const content = document.createElement("div");

    content.className = "file-content";

    if (data.type.startsWith("image/")) {
        const image = document.createElement("img");

        image.src = data.url;
        image.alt = data.filename;
        image.loading = "lazy";

        content.appendChild(image);
    }

    else if (data.type.startsWith("video/")) {
        const video = document.createElement("video");

        video.src = data.url;
        video.controls = true;
        video.preload = "metadata";

        content.appendChild(video);
    }

    else {
        const fileLink = document.createElement("a");

        fileLink.href = data.url;
        fileLink.target = "_blank";
        fileLink.download = data.filename;

        const fileName = document.createElement("strong");

        fileName.textContent = data.filename;

        const fileSize = document.createElement("span");

        fileSize.textContent = formatFileSize(data.size);

        fileLink.appendChild(fileName);
        fileLink.appendChild(fileSize);

        content.className += " generic-file";

        content.appendChild(fileLink);
    }

    const filename = document.createElement("div");

    filename.className = "attachment-name";

    filename.textContent = data.filename;

    messageElement.appendChild(name);
    messageElement.appendChild(content);

    if (
        data.type.startsWith("image/")
        || data.type.startsWith("video/")
    ) {
        messageElement.appendChild(filename);
    }

    messages.appendChild(messageElement);

    scrollMessages();
}


function addSystemMessage(text) {
    const element = document.createElement("div");

    element.className = "system-message";

    element.textContent = text;

    messages.appendChild(element);

    scrollMessages();
}


function removeWelcome() {
    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }
}


function scrollMessages() {
    messages.scrollTop = messages.scrollHeight;
}


function updateMembers(members) {
    memberList.innerHTML = "";

    memberCount.textContent = members.length;

    members.forEach(member => {
        const item = document.createElement("div");

        item.className = "member";

        const avatar = document.createElement("div");

        avatar.className = "member-avatar";

        avatar.textContent = member.name
            .charAt(0)
            .toUpperCase();

        const name = document.createElement("span");

        let displayName = member.name;

        if (member.name === USER_NAME) {
            displayName += " (You)";
        }

        if (member.admin) {
            displayName += " • Admin";
        }

        name.textContent = displayName;

        item.appendChild(avatar);
        item.appendChild(name);

        memberList.appendChild(item);
    });
}


function updateTypingIndicator() {
    if (typingUsers.size === 0) {
        typingIndicator.textContent = "";
        return;
    }

    const users = Array.from(typingUsers);

    if (users.length === 1) {
        typingIndicator.textContent =
            `${users[0]} is typing...`;

        return;
    }

    typingIndicator.textContent =
        `${users.length} people are typing...`;
}


function formatFileSize(bytes) {
    if (bytes < 1024) {
        return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}


function uploadSelectedFile() {
    if (!selectedFile) {
        return;
    }

    if (selectedFile.size > 20 * 1024 * 1024) {
        showNotification(
            "File Too Large",
            "Maximum file size is 20 MB.",
            "error"
        );

        return;
    }

    const reader = new FileReader();

    reader.onload = event => {
        socket.emit("upload_file", {
            filename: selectedFile.name,
            type: selectedFile.type || "application/octet-stream",
            file: event.target.result
        });

        selectedFile = null;

        uploadPreview.classList.add("hidden");

        fileInput.value = "";
    };

    reader.readAsArrayBuffer(selectedFile);
}


sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    event => {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
);


messageInput.addEventListener(
    "input",
    () => {
        socket.emit("typing", {
            typing: true
        });

        clearTimeout(typingTimeout);

        typingTimeout = setTimeout(() => {
            socket.emit("typing", {
                typing: false
            });
        }, 1000);
    }
);


clearChat.addEventListener(
    "click",
    () => {
        socket.emit("clear_chat");
    }
);


copyRoom.addEventListener(
    "click",
    async () => {
        try {
            await navigator.clipboard.writeText(
                ROOM_ID
            );

            showNotification(
                "Copied",
                "Room number copied to clipboard.",
                "success"
            );

        } catch {
            showNotification(
                "Failed",
                "Could not copy room number.",
                "error"
            );
        }
    }
);


leaveRoom.addEventListener(
    "click",
    () => {
        window.location.href = "/";
    }
);


fileButton.addEventListener(
    "click",
    () => {
        fileInput.click();
    }
);


fileInput.addEventListener(
    "change",
    () => {
        const file = fileInput.files[0];

        if (!file) {
            return;
        }

        if (file.size > 20 * 1024 * 1024) {
            showNotification(
                "File Too Large",
                "Maximum file size is 20 MB.",
                "error"
            );

            fileInput.value = "";

            return;
        }

        selectedFile = file;

        uploadInfo.innerHTML = `
            <strong>${escapeHtml(file.name)}</strong>
            <span>${formatFileSize(file.size)}</span>
        `;

        uploadPreview.classList.remove("hidden");

        uploadSelectedFile();
    }
);


cancelUpload.addEventListener(
    "click",
    () => {
        selectedFile = null;

        fileInput.value = "";

        uploadPreview.classList.add("hidden");
    }
);


passwordCancel.addEventListener(
    "click",
    () => {
        window.location.href = "/";
    }
);


passwordJoin.addEventListener(
    "click",
    () => {
        roomPassword = roomPasswordInput.value.trim();

        if (!roomPassword) {
            showNotification(
                "Password Required",
                "Enter the room password.",
                "warning"
            );

            roomPasswordInput.focus();

            return;
        }

        passwordModal.classList.add("hidden");

        joinCurrentRoom();
    }
);


roomPasswordInput.addEventListener(
    "keydown",
    event => {
        if (event.key === "Enter") {
            passwordJoin.click();
        }
    }
);


function escapeHtml(value) {
    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}
