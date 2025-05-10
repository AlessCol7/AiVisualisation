# import gradio as gr
# import requests

# API_URL = "http://localhost:8000"

# # --- Authentication ---
# def login_user(u, p):
#     resp = requests.post(f"{API_URL}/login", json={"username": u, "password": p})
#     return resp.status_code == 200

# def register_user(u, p):
#     resp = requests.post(f"{API_URL}/register", json={"username": u, "password": p})
#     return resp.status_code == 200

# def do_login(u, p):
#     if login_user(u, p):
#         return True, u, gr.update(visible=False), gr.update(visible=True), "✅ Login successful!"
#     else:
#         return False, "", gr.update(), gr.update(), "❌ Login failed. Try again."

# def do_register(u, p):
#     if register_user(u, p):
#         return "✅ Registration successful!"
#     else:
#         return "❌ Username already exists or error occurred."

# # --- Chat Logic ---
# def chat_wrapper(message, room_histories, current_room, username):
#     if current_room not in room_histories:
#         room_histories[current_room] = []

#     room_histories[current_room].append((message, None))

#     lower_msg = message.strip().lower()
#     if "hello" in lower_msg:
#         bot_response = "Hi! How can I help you today?"
#     elif "thanks" in lower_msg:
#         bot_response = "You're welcome!"
#     else:
#         bot_response = "I'm just a simple bot for now 😅"

#     room_histories[current_room].append((None, bot_response))

#     chat_display = [(room_histories[current_room][i][0], room_histories[current_room][i+1][1])
#                     for i in range(0, len(room_histories[current_room]), 2)]
    
#     return "", chat_display, room_histories

# def switch_room(room, room_histories):
#     if room not in room_histories:
#         room_histories[room] = []

#     chat_display = [(room_histories[room][i][0], room_histories[room][i+1][1])
#                     for i in range(0, len(room_histories[room]), 2)]
#     return room, chat_display

# def add_room(new_room, room_list, room_histories):
#     if new_room and new_room not in room_list:
#         room_list.append(new_room)
#         room_histories[new_room] = []
#     return gr.update(choices=room_list, value=new_room), room_list, room_histories, []

# # --- Initial Room Setup ---
# rooms = ["main", "introduction", "general", "random"]

# with gr.Blocks() as demo:
#     logged_in = gr.State(value=False)
#     username = gr.State()
#     current_room = gr.State(value="main")
#     all_rooms = gr.State(rooms.copy())
#     room_histories = gr.State({room: [] for room in rooms})

#     # --- Login UI ---
#     with gr.Column(visible=True) as login_col:
#         gr.Markdown("## 🔐 Login to ChatBot")
#         user = gr.Textbox(label="Username")
#         password = gr.Textbox(label="Password", type="password")
#         login_btn = gr.Button("Login")
#         register_btn = gr.Button("Register")
#         msg = gr.Markdown()

#     # --- Chat UI ---
#     with gr.Row(visible=False) as chat_col:
#         # Sidebar
#         with gr.Column(scale=1):
#             with gr.Row():
#                 user_info = gr.Markdown("🟢 **User:**", elem_id="user_display")

#             gr.Markdown("### 🗂 Rooms")
#             room_list = gr.Radio(choices=rooms, value="main", label="", interactive=True)

#             with gr.Row():
#                 new_room = gr.Textbox(placeholder="New room", scale=3)
#                 add_room_btn = gr.Button("➕", scale=1)

#         # Chat Interface
#         with gr.Column(scale=4):
#             gr.Markdown("### 💬 Chat Interface")
#             gr.Markdown("### 🤖 How can I help you today?")
#             chatbot = gr.Chatbot(label="", height=450)

#             with gr.Row():
#                 msg_input = gr.Textbox(placeholder="Type your message...", scale=9)
#                 send_btn = gr.Button("Send", scale=1)

#     # --- Callbacks ---
#     login_btn.click(do_login, [user, password], [logged_in, username, login_col, chat_col, msg])
#     register_btn.click(do_register, [user, password], msg)

#     username.change(lambda u: gr.update(value=f"🟢 **User:** {u}"), username, user_info)

#     room_list.change(switch_room, [room_list, room_histories], [current_room, chatbot])
#     add_room_btn.click(add_room, [new_room, all_rooms, room_histories], [room_list, all_rooms, room_histories, chatbot])

#     send_btn.click(chat_wrapper, [msg_input, room_histories, current_room, username],
#                    [msg_input, chatbot, room_histories])
#     msg_input.submit(chat_wrapper, [msg_input, room_histories, current_room, username],
#                      [msg_input, chatbot, room_histories])

# if __name__ == "__main__":
#     demo.launch()
# frontend.py
import gradio as gr
import requests

API_URL = "http://localhost:8000"

# --- Authentication ---
def login_user(u, p):
    resp = requests.post(f"{API_URL}/login", json={"username": u, "password": p})
    return resp.status_code == 200

def register_user(u, p):
    resp = requests.post(f"{API_URL}/register", json={"username": u, "password": p})
    return resp.status_code == 200

def do_login(u, p):
    if login_user(u, p):
        return True, u, gr.update(visible=False), gr.update(visible=True), "✅ Login successful!"
    else:
        return False, "", gr.update(), gr.update(), "❌ Login failed. Try again."

def do_register(u, p):
    if register_user(u, p):
        return "✅ Registration successful!"
    else:
        return "❌ Username already exists or error occurred."

# --- Chat Logic ---
def chat_wrapper(message, room_histories, current_room, username):
    if current_room not in room_histories:
        room_histories[current_room] = []

    room_histories[current_room].append((message, None))

    lower_msg = message.strip().lower()
    if "hello" in lower_msg:
        bot_response = "Hi! How can I help you today?"
    elif "thanks" in lower_msg:
        bot_response = "You're welcome!"
    else:
        bot_response = "I'm just a simple bot for now 😅"

    room_histories[current_room].append((None, bot_response))

    chat_display = [(room_histories[current_room][i][0], room_histories[current_room][i+1][1])
                    for i in range(0, len(room_histories[current_room]), 2)]

    return "", chat_display, room_histories

def switch_room(room, room_histories):
    if room not in room_histories:
        room_histories[room] = []

    chat_display = [(room_histories[room][i][0], room_histories[room][i+1][1])
                    for i in range(0, len(room_histories[room]), 2)]
    return room, chat_display

def add_room(new_room, room_list, room_histories):
    if new_room and new_room not in room_list:
        room_list.append(new_room)
        room_histories[new_room] = []
    return gr.update(choices=room_list, value=new_room), room_list, room_histories, []

def handle_upload(uploaded_file, room_histories, current_room):
    if uploaded_file is None:
        return room_histories[current_room], room_histories

    display_name = uploaded_file.name
    file_msg = f"📎 Uploaded file: {display_name}"
    room_histories[current_room].append((file_msg, None))
    room_histories[current_room].append((None, "Thanks for the file! 📄"))

    chat_display = [(room_histories[current_room][i][0], room_histories[current_room][i+1][1])
                    for i in range(0, len(room_histories[current_room]), 2)]
    return chat_display, room_histories

# --- Initial Room Setup ---
rooms = ["main", "introduction", "general", "random"]

with gr.Blocks() as demo:
    logged_in = gr.State(value=False)
    username = gr.State()
    current_room = gr.State(value="main")
    all_rooms = gr.State(rooms.copy())
    room_histories = gr.State({room: [] for room in rooms})

    # --- Login UI ---
    with gr.Column(visible=True) as login_col:
        gr.Markdown("## 🔐 Login to ChatBot")
        user = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        register_btn = gr.Button("Register")
        msg = gr.Markdown()

    # --- Chat UI ---
    with gr.Row(visible=False) as chat_col:
        # Sidebar
        with gr.Column(scale=1):
            with gr.Row():
                user_info = gr.Markdown("🟢 **User:**", elem_id="user_display")

            gr.Markdown("### 🗂 Rooms")
            room_list = gr.Radio(choices=rooms, value="main", label="", interactive=True)

            with gr.Row():
                new_room = gr.Textbox(placeholder="New room", scale=3)
                add_room_btn = gr.Button("➕", scale=1)

        # Chat Interface
        with gr.Column(scale=8):
            gr.Markdown("### 💬 Chat Interface")
            gr.Markdown("### 🤖 How can I help you today?")
            chatbot = gr.Chatbot(label="", height=450)

            with gr.Row():
                msg_input = gr.Textbox(placeholder="Type your message...", scale=7)
                upload_btn = gr.File(label="📌", file_types=["image", ".pdf", ".docx"], scale=2,height=150, interactive=True)
                send_btn = gr.Button("Send", scale=1)

    # --- Callbacks ---
    login_btn.click(do_login, [user, password], [logged_in, username, login_col, chat_col, msg])
    register_btn.click(do_register, [user, password], msg)

    username.change(lambda u: gr.update(value=f"🟢 **User:** {u}"), username, user_info)

    room_list.change(switch_room, [room_list, room_histories], [current_room, chatbot])
    add_room_btn.click(add_room, [new_room, all_rooms, room_histories], [room_list, all_rooms, room_histories, chatbot])

    send_btn.click(chat_wrapper, [msg_input, room_histories, current_room, username],
                   [msg_input, chatbot, room_histories])
    msg_input.submit(chat_wrapper, [msg_input, room_histories, current_room, username],
                     [msg_input, chatbot, room_histories])

    upload_btn.change(handle_upload, [upload_btn, room_histories, current_room], [chatbot, room_histories])

if __name__ == "__main__":
    demo.launch()
