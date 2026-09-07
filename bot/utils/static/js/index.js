const nameInput = document.getElementById("name");
const roomInput = document.getElementById("room");
const passwordInput = document.getElementById("password");

const joinButton = document.getElementById("joinButton");
const defaultRoom = document.getElementById("defaultRoom");
const randomRoom = document.getElementById("randomRoom");
const togglePassword = document.getElementById("togglePassword");


function joinRoom(room = null) {
    const name = nameInput.value.trim();
    const selectedRoom = room || roomInput.value.trim();
    const password = passwordInput.value;

    if (!name) {
        nameInput.focus();
        return;
    }

    if (!selectedRoom) {
        roomInput.focus();
        return;
    }

    const params = new URLSearchParams({
        name: name,
        room: selectedRoom
    });

    if (password && room !== "127.0.0.1") {
        params.set("password", password);
    }

    window.location.href = `/chat?${params.toString()}`;
}


joinButton.addEventListener("click", () => {
    joinRoom();
});


defaultRoom.addEventListener("click", () => {
    roomInput.value = "127.0.0.1";
    passwordInput.value = "";

    joinRoom("127.0.0.1");
});


randomRoom.addEventListener("click", async () => {
    try {
        const response = await fetch("/create-room");
        const data = await response.json();

        roomInput.value = data.room;
        passwordInput.focus();

    } catch {
        alert("Failed to create room number.");
    }
});


togglePassword.addEventListener("click", () => {
    const hidden = passwordInput.type === "password";

    passwordInput.type = hidden
        ? "text"
        : "password";

    togglePassword.textContent = hidden
        ? "Hide"
        : "Show";
});


[nameInput, roomInput, passwordInput].forEach(input => {
    input.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            joinRoom();
        }
    });
});