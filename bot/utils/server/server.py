import os
import shutil
import random
import time
import uuid
from functools import wraps
from threading import Thread

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

app.config["SECRET_KEY"] = "619e2420-0d79-440b-8cc2-6a1c592abc1b"
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    max_http_buffer_size=20 * 1024 * 1024
)


ADMIN_USERNAME = "bishalqx980"
ADMIN_PASSWORD = "bishal654123"

DEFAULT_ROOM = "127.0.0.1"

MAX_FILE_SIZE = 20 * 1024 * 1024
MAX_ROOM_UPLOAD_SIZE = 200 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


rooms = {}
users = {}
clear_cooldowns = {}


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))

        return f(*args, **kwargs)

    return decorated


def get_room_upload_folder(room_id):
    safe_room = secure_filename(room_id)

    return os.path.join(
        UPLOAD_FOLDER,
        safe_room
    )


def get_room_upload_size(room_id):
    room = rooms.get(room_id)

    if not room:
        return 0

    return room.get("upload_size", 0)


def create_room(room_id, password=None):
    if room_id in rooms:
        return

    password_hash = None

    if room_id != DEFAULT_ROOM and password:
        password_hash = generate_password_hash(password)

    rooms[room_id] = {
        "members": {},
        "password_hash": password_hash,
        "upload_size": 0
    }


def delete_room(room_id):
    if room_id == DEFAULT_ROOM:
        return

    room_path = get_room_upload_folder(room_id)

    if os.path.exists(room_path):
        shutil.rmtree(room_path, ignore_errors=True)

    rooms.pop(room_id, None)


def get_members(room_id):
    if room_id not in rooms:
        return []

    members = []

    for sid, user in rooms[room_id]["members"].items():
        members.append({
            "sid": sid,
            "name": user["name"],
            "admin": user.get("admin", False)
        })

    return members


def remove_user_from_room(sid):
    if sid not in users:
        return None

    user = users.pop(sid)

    room_id = user["room"]

    if room_id in rooms:
        rooms[room_id]["members"].pop(sid, None)

        if rooms[room_id]["members"]:
            socketio.emit(
                "user_left",
                {
                    "name": user["name"],
                    "members": get_members(room_id)
                },
                room=room_id
            )

        else:
            if room_id == DEFAULT_ROOM:
                socketio.emit(
                    "user_left",
                    {
                        "name": user["name"],
                        "members": []
                    },
                    room=room_id
                )
            else:
                delete_room(room_id)

    return user


@app.route("/")
def index():
    return render_template(
        "index.html",
        default_room=DEFAULT_ROOM
    )


@app.route("/chat")
def chat():
    name = request.args.get("name", "").strip()
    room = request.args.get("room", "").strip()
    password = request.args.get("password", "")

    if not name or not room:
        return redirect(url_for("index"))

    if len(name) > 30:
        return redirect(url_for("index"))

    if len(room) > 100:
        return redirect(url_for("index"))

    return render_template(
        "chat.html",
        name=name,
        room=room,
        password=password,
        is_admin=False
    )


@app.route("/create-room")
def create_random_room():
    while True:
        room_id = str(
            random.randint(
                10000000,
                99999999
            )
        )

        if room_id not in rooms:
            break

    return jsonify({
        "room": room_id
    })


@app.route("/uploads/<room>/<filename>")
def uploaded_file(room, filename):
    folder = get_room_upload_folder(room)

    return send_from_directory(
        folder,
        filename
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):
            session["admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    return render_template(
        "admin_dashboard.html"
    )


@app.route("/admin/join-room")
@admin_required
def admin_join_room_page():
    name = request.args.get(
        "name",
        "Administrator"
    ).strip()

    room = request.args.get(
        "room",
        ""
    ).strip()

    if not room:
        return redirect(
            url_for("admin_dashboard")
        )

    if not name:
        name = "Administrator"

    return render_template(
        "chat.html",
        name=name,
        room=room,
        password="",
        is_admin=True
    )


@app.route("/admin/logout")
def admin_logout():
    session.clear()

    return redirect(
        url_for("admin_login")
    )


@app.route("/admin/rooms")
@admin_required
def admin_rooms():
    room_data = []

    for room_id, room in rooms.items():
        room_data.append({
            "room": room_id,
            "count": len(room["members"]),
            "members": get_members(room_id),
            "password_protected": (
                room["password_hash"] is not None
            ),
            "upload_size": room["upload_size"]
        })

    return jsonify({
        "rooms": room_data,
        "total_users": len(users),
        "total_rooms": len(rooms)
    })


@app.route("/admin/kick/<sid>", methods=["POST"])
@admin_required
def admin_kick(sid):
    if sid not in users:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    socketio.emit(
        "kicked",
        {
            "message": "You have been removed by an administrator."
        },
        to=sid
    )

    remove_user_from_room(sid)

    socketio.server.disconnect(sid)

    return jsonify({
        "success": True
    })


@socketio.on("connect")
def handle_connect():
    pass


@socketio.on("join")
def handle_join(data):
    sid = request.sid

    name = str(
        data.get("name", "")
    ).strip()

    room_id = str(
        data.get("room", "")
    ).strip()

    password = str(
        data.get("password", "")
    )

    is_admin = bool(
        data.get("admin", False)
    )

    if not name or not room_id:
        emit(
            "join_error",
            {
                "message": "Invalid name or room."
            }
        )

        return

    if len(name) > 30:
        emit(
            "join_error",
            {
                "message": "Name is too long."
            }
        )

        return

    if len(room_id) > 100:
        emit(
            "join_error",
            {
                "message": "Invalid room ID."
            }
        )

        return

    if is_admin and not session.get("admin"):
        emit(
            "join_error",
            {
                "message": "Unauthorized administrator access."
            }
        )

        return

    if room_id == DEFAULT_ROOM:
        password = ""

    if room_id not in rooms:
        create_room(
            room_id,
            password
        )

    room = rooms[room_id]

    if (
        room_id != DEFAULT_ROOM
        and room["password_hash"]
        and not is_admin
    ):
        if not password:
            emit(
                "password_required",
                {
                    "message": "This room requires a password."
                }
            )

            return

        if not check_password_hash(
            room["password_hash"],
            password
        ):
            emit(
                "wrong_password",
                {
                    "message": "Incorrect room password."
                }
            )

            return

    users[sid] = {
        "name": name,
        "room": room_id,
        "admin": is_admin
    }

    rooms[room_id]["members"][sid] = {
        "name": name,
        "admin": is_admin
    }

    join_room(room_id)

    emit(
        "room_joined",
        {
            "room": room_id,
            "members": get_members(room_id),
            "password_protected": (
                room["password_hash"] is not None
            )
        }
    )

    socketio.emit(
        "user_joined",
        {
            "name": name,
            "members": get_members(room_id)
        },
        room=room_id,
        include_self=False
    )


@socketio.on("send_message")
def handle_message(data):
    sid = request.sid

    if sid not in users:
        return

    message = str(
        data.get("message", "")
    ).strip()

    if not message:
        return

    if len(message) > 2000:
        return

    user = users[sid]

    socketio.emit(
        "new_message",
        {
            "name": user["name"],
            "message": message,
            "admin": user["admin"]
        },
        room=user["room"]
    )


@socketio.on("typing")
def handle_typing(data):
    sid = request.sid

    if sid not in users:
        return

    user = users[sid]

    socketio.emit(
        "typing",
        {
            "name": user["name"],
            "typing": bool(
                data.get("typing")
            )
        },
        room=user["room"],
        include_self=False
    )


@socketio.on("clear_chat")
def handle_clear_chat():
    sid = request.sid

    if sid not in users:
        return

    user = users[sid]
    room_id = user["room"]

    if not user["admin"]:
        now = time.time()

        last_clear = clear_cooldowns.get(
            sid,
            0
        )

        elapsed = now - last_clear
        remaining = 30 - elapsed

        if remaining > 0:
            emit(
                "clear_cooldown",
                {
                    "remaining": int(remaining) + 1
                }
            )

            return

        clear_cooldowns[sid] = now

    room_path = get_room_upload_folder(room_id)

    if os.path.exists(room_path):
        shutil.rmtree(
            room_path,
            ignore_errors=True
        )

    os.makedirs(
        room_path,
        exist_ok=True
    )

    if room_id in rooms:
        rooms[room_id]["upload_size"] = 0

    socketio.emit(
        "chat_cleared",
        {
            "name": user["name"],
            "admin": user["admin"]
        },
        room=room_id
    )


@socketio.on("upload_file")
def handle_upload_file(data):
    sid = request.sid

    if sid not in users:
        emit(
            "upload_error",
            {
                "message": "Unauthorized."
            }
        )

        return

    filename = str(
        data.get("filename", "")
    )

    file_data = data.get("file")

    if not filename or not file_data:
        emit(
            "upload_error",
            {
                "message": "Invalid file."
            }
        )

        return

    if not isinstance(file_data, (bytes, bytearray)):
        emit(
            "upload_error",
            {
                "message": "Invalid file format."
            }
        )

        return

    file_size = len(file_data)

    if file_size > MAX_FILE_SIZE:
        emit(
            "upload_error",
            {
                "message": "File exceeds the 20 MB limit."
            }
        )

        return

    user = users[sid]
    room_id = user["room"]

    current_size = get_room_upload_size(room_id)

    if (
        current_size + file_size
        > MAX_ROOM_UPLOAD_SIZE
    ):
        emit(
            "upload_error",
            {
                "message": "Room has reached its 200 MB upload limit."
            }
        )

        return

    safe_filename = secure_filename(filename)

    if not safe_filename:
        safe_filename = "file"

    unique_filename = (
        f"{uuid.uuid4().hex}_{safe_filename}"
    )

    room_folder = get_room_upload_folder(
        room_id
    )

    os.makedirs(
        room_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        room_folder,
        unique_filename
    )

    try:
        with open(file_path, "wb") as file:
            file.write(file_data)

    except Exception:
        emit(
            "upload_error",
            {
                "message": "Failed to save file."
            }
        )

        return

    rooms[room_id]["upload_size"] += file_size

    mime_type = str(
        data.get(
            "type",
            "application/octet-stream"
        )
    )

    file_url = (
        f"/uploads/"
        f"{room_id}/"
        f"{unique_filename}"
    )

    socketio.emit(
        "new_file",
        {
            "name": user["name"],
            "admin": user["admin"],
            "filename": safe_filename,
            "url": file_url,
            "type": mime_type,
            "size": file_size
        },
        room=room_id
    )


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid

    clear_cooldowns.pop(sid, None)

    remove_user_from_room(sid)


create_room(DEFAULT_ROOM)


def run():
    socketio.run(
        app,
        host="0.0.0.0",
        port=PORT,
        # debug=True,
        allow_unsafe_werkzeug=True
    )


def server():
    Thread(target=run).start()
