const roomsContainer =
    document.getElementById("roomsContainer");

const totalUsers =
    document.getElementById("totalUsers");

const totalRooms =
    document.getElementById("totalRooms");

const defaultRoomCount =
    document.getElementById("defaultRoomCount");

const refreshRooms =
    document.getElementById("refreshRooms");

const roomModal =
    document.getElementById("roomModal");

const closeModal =
    document.getElementById("closeModal");

const modalRoomId =
    document.getElementById("modalRoomId");

const modalMemberCount =
    document.getElementById("modalMemberCount");

const modalMembers =
    document.getElementById("modalMembers");

const adminJoinModal =
    document.getElementById("adminJoinModal");

const closeAdminJoin =
    document.getElementById("closeAdminJoin");

const adminJoinRoomText =
    document.getElementById("adminJoinRoomText");

const adminJoinName =
    document.getElementById("adminJoinName");

const confirmAdminJoin =
    document.getElementById("confirmAdminJoin");


let selectedRoom = null;


async function loadRooms() {
    try {
        const response = await fetch(
            "/admin/rooms"
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        totalUsers.textContent =
            data.total_users;

        totalRooms.textContent =
            data.total_rooms;

        const defaultRoom = data.rooms.find(
            room =>
                room.room === "127.0.0.1"
        );

        defaultRoomCount.textContent =
            defaultRoom
                ? defaultRoom.count
                : 0;

        renderRooms(data.rooms);

    } catch {
        roomsContainer.innerHTML = `
            <div class="empty-state">
                Failed to load rooms
            </div>
        `;
    }
}


function renderRooms(rooms) {
    roomsContainer.innerHTML = "";

    if (!rooms.length) {
        roomsContainer.innerHTML = `
            <div class="empty-state">
                No active rooms
            </div>
        `;

        return;
    }

    rooms.forEach(room => {
        const card = document.createElement("div");

        card.className = "room-card-admin";

        const protection = room.password_protected
            ? "🔒 Protected"
            : "Public";

        card.innerHTML = `
            <div class="room-info">
                <span>ROOM</span>
                <h3>${escapeHtml(room.room)}</h3>
                <small>${protection}</small>
            </div>

            <div class="room-count">
                <strong>${room.count}</strong>
                <span>Members</span>
            </div>

            <div class="room-storage">
                ${formatFileSize(room.upload_size)}
                <span>Uploads</span>
            </div>

            <div class="room-actions">

                <button class="view-room">
                    View
                </button>

                <button class="join-room">
                    Join
                </button>

            </div>
        `;

        card.querySelector(".view-room")
            .addEventListener(
                "click",
                () => {
                    openRoom(room);
                }
            );

        card.querySelector(".join-room")
            .addEventListener(
                "click",
                () => {
                    openAdminJoin(room.room);
                }
            );

        roomsContainer.appendChild(card);
    });
}


function openRoom(room) {
    modalRoomId.textContent =
        `Room ${room.room}`;

    modalMemberCount.textContent =
        `${room.count} member${room.count !== 1 ? "s" : ""}`;

    modalMembers.innerHTML = "";

    room.members.forEach(member => {
        const item = document.createElement("div");

        item.className = "modal-member";

        const info = document.createElement("div");

        info.className = "member-info";

        const avatar = document.createElement("div");

        avatar.className = "member-avatar";

        avatar.textContent = member.name
            .charAt(0)
            .toUpperCase();

        const name = document.createElement("span");

        name.textContent = member.admin
            ? `${member.name} • Admin`
            : member.name;

        info.appendChild(avatar);
        info.appendChild(name);

        item.appendChild(info);

        if (!member.admin) {
            const kickButton =
                document.createElement("button");

            kickButton.className =
                "kick-button";

            kickButton.textContent =
                "Kick";

            kickButton.addEventListener(
                "click",
                async () => {
                    const confirmed = confirm(
                        `Kick ${member.name}?`
                    );

                    if (!confirmed) {
                        return;
                    }

                    try {
                        await fetch(
                            `/admin/kick/${member.sid}`,
                            {
                                method: "POST"
                            }
                        );

                        roomModal.classList.add(
                            "hidden"
                        );

                        loadRooms();

                    } catch {
                        alert(
                            "Failed to kick user."
                        );
                    }
                }
            );

            item.appendChild(kickButton);
        }

        modalMembers.appendChild(item);
    });

    roomModal.classList.remove("hidden");
}


function openAdminJoin(room) {
    selectedRoom = room;

    adminJoinRoomText.textContent =
        `Joining room ${room}`;

    adminJoinName.value = "Administrator";

    adminJoinModal.classList.remove(
        "hidden"
    );

    adminJoinName.focus();
    adminJoinName.select();
}


function confirmJoin() {
    const name = adminJoinName.value.trim();

    if (!name) {
        adminJoinName.focus();
        return;
    }

    const params = new URLSearchParams({
        room: selectedRoom,
        name: name
    });

    window.open(
        `/admin/join-room?${params.toString()}`,
        "_blank"
    );

    adminJoinModal.classList.add(
        "hidden"
    );
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


function escapeHtml(value) {
    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


refreshRooms.addEventListener(
    "click",
    loadRooms
);


closeModal.addEventListener(
    "click",
    () => {
        roomModal.classList.add("hidden");
    }
);


roomModal.addEventListener(
    "click",
    event => {
        if (event.target === roomModal) {
            roomModal.classList.add("hidden");
        }
    }
);


closeAdminJoin.addEventListener(
    "click",
    () => {
        adminJoinModal.classList.add(
            "hidden"
        );
    }
);


confirmAdminJoin.addEventListener(
    "click",
    confirmJoin
);


adminJoinName.addEventListener(
    "keydown",
    event => {
        if (event.key === "Enter") {
            confirmJoin();
        }
    }
);


adminJoinModal.addEventListener(
    "click",
    event => {
        if (event.target === adminJoinModal) {
            adminJoinModal.classList.add(
                "hidden"
            );
        }
    }
);


loadRooms();

setInterval(
    loadRooms,
    3000
);