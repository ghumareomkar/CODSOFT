import tkinter as tk
from tkinter import scrolledtext, filedialog
import re
import datetime

# ---------------- RULE ENGINE ---------------- #

class RuleBase:
    def __init__(self):
        self.rules = {
            "greeting": r"\b(hi|hello|hey|good morning|good evening)\b",
            "farewell": r"\b(bye|goodbye|see you|exit)\b",
            "name": r"\b(your name|who are you)\b",
            "time": r"\b(time|current time)\b",
            "date": r"\b(date|today)\b",
            "weather": r"\b(weather|temperature)\b",
            "help": r"\b(help|assist|support)\b",
            "thanks": r"\b(thank you|thanks)\b",
            "emotion": r"\b(sad|happy|angry|depressed|excited)\b"
        }

    def match_intent(self, text):
        for intent, pattern in self.rules.items():
            if re.search(pattern, text):
                return intent
        return "unknown"


# ---------------- MEMORY MANAGER ---------------- #

class MemoryManager:
    def __init__(self):
        self.last_intent = None
        self.conversation_history = []

    def update_memory(self, user_input, bot_response, intent):
        self.last_intent = intent
        self.conversation_history.append(
            (datetime.datetime.now(), user_input, bot_response)
        )


# ---------------- CHAT ENGINE ---------------- #

class ChatEngine:
    def __init__(self):
        self.rulebase = RuleBase()
        self.memory = MemoryManager()

    def sentiment_score(self, text):
        positive_words = ["happy", "good", "great", "awesome", "excited"]
        negative_words = ["sad", "bad", "angry", "depressed", "upset"]

        score = 0
        for word in positive_words:
            if word in text:
                score += 1
        for word in negative_words:
            if word in text:
                score -= 1
        return score

    def generate_response(self, user_input):
        text = user_input.lower()
        intent = self.rulebase.match_intent(text)
        sentiment = self.sentiment_score(text)

        response = ""

        if intent == "greeting":
            response = "Hello! How can I assist you today?"
        elif intent == "farewell":
            response = "Goodbye! Have a productive day."
        elif intent == "name":
            response = "I am a Rule-Based NLP Chatbot developed as an academic AI project."
        elif intent == "time":
            response = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
        elif intent == "date":
            response = f"Today's date is {datetime.date.today()}."
        elif intent == "weather":
            response = "Weather API not integrated. Please connect external service."
        elif intent == "help":
            response = "I can respond to greetings, time/date queries, emotions, and general conversation."
        elif intent == "thanks":
            response = "You're welcome!"
        elif intent == "emotion":
            if sentiment > 0:
                response = "I'm glad you're feeling positive!"
            elif sentiment < 0:
                response = "I'm sorry to hear that. Would you like to talk about it?"
            else:
                response = "Emotions detected. Tell me more."
        else:
            if self.memory.last_intent == "emotion":
                response = "Earlier you mentioned emotions. Would you like advice?"
            else:
                response = "I'm not sure I understand. Could you rephrase?"

        self.memory.update_memory(user_input, response, intent)
        return response

    def export_chat_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                for entry in self.memory.conversation_history:
                    timestamp, user, bot = entry
                    f.write(f"[{timestamp}]\nUser: {user}\nBot: {bot}\n\n")


# ---------------- GUI ---------------- #

class ChatGUI:
    def __init__(self, root):
        self.engine = ChatEngine()
        self.root = root
        self.root.title("Advanced Rule-Based Chatbot")
        self.root.configure(bg="#1e1e2f")

        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, font=("Arial", 12),
            bg="#2d2d44", fg="white"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(
            root, font=("Arial", 12),
            bg="#444466", fg="white"
        )
        self.input_field.pack(fill=tk.X, padx=10, pady=5)
        self.input_field.bind("<Return>", self.send_message)

        send_btn = tk.Button(
            root, text="Send",
            bg="#00a8ff", fg="white",
            command=self.send_message
        )
        send_btn.pack(pady=5)

        export_btn = tk.Button(
            root, text="Export Chat Log",
            bg="#e84118", fg="white",
            command=self.engine.export_chat_log
        )
        export_btn.pack(pady=5)

    def send_message(self, event=None):
        user_input = self.input_field.get()
        if user_input.strip() == "":
            return

        self.chat_area.insert(tk.END, f"\nYou: {user_input}\n")
        response = self.engine.generate_response(user_input)
        self.chat_area.insert(tk.END, f"Bot: {response}\n")

        self.input_field.delete(0, tk.END)
        self.chat_area.yview(tk.END)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = ChatGUI(root)
    root.mainloop()