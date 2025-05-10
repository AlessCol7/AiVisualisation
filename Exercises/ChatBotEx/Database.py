import sqlite3
import gradio as gr
from passlib.hash import bcrypt

# --- Database and Auth Functions ---
DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

def register_user(username, password):
    if not username or not password:
        return False, "Username and password are required."
    hashed = bcrypt.hash(password)
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username already exists."

def authenticate(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.verify(password, result[0]):
        return True
    return False

# --- Gradio UI and Logic ---
def chat_response(message, history, username):
    # Simple echo bot for demo; replace with your AI logic!
    return f"{username}: {message}"

def login(username, password):
    if authenticate(username, password):
        return (True, username, gr.update(visible=False), gr.update(visible=True), "")
    return (False, None, gr.update(), gr.update(), "Login failed. Check your username and password.")

def register(username, password):
    success, msg = register_user(username, password)
    if success:
        return (True, username, gr.update(visible=False), gr.update(visible=True), msg)
    return (False, None, gr.update(), gr.update(), msg)

with gr.Blocks(theme="soft", title="DiscordAI Chat") as demo:
    username_state = gr.State()
    with gr.Column(visible=True) as login_col:
        gr.Markdown("## Login / Register")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        with gr.Row():
            login_btn = gr.Button("Login")
            register_btn = gr.Button("Register")
        status = gr.Markdown()

    with gr.Column(visible=False) as chat_col:
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(label="Message", placeholder="Type your message...")
        clear = gr.ClearButton([msg, chatbot])

    login_btn.click(
        login, inputs=[username, password], outputs=[status, username_state, login_col, chat_col, status]
    )
    register_btn.click(
        register, inputs=[username, password], outputs=[status, username_state, login_col, chat_col, status]
    )
    msg.submit(
        chat_response, inputs=[msg, chatbot, username_state], outputs=[chatbot]
    )

demo.launch()
