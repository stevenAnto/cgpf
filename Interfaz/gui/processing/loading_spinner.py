import tkinter as tk

class LoadingSpinner:
    def __init__(self, parent, text_prefix="Procesando"):
        self.parent = parent
        self.container = tk.Frame(parent)
        self.container.pack(pady=5)

        self.label = tk.Label(self.container, text="", fg="blue", font=("Arial", 14))
        self.label.pack()
        
        self.text_prefix = text_prefix
        self.running = False
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.delay = 100  # milisegundos
        self.current_index = 0

    def start(self):
        if not self.running:
            self.running = True
            self._animate()

    def stop(self):
        self.running = False
        self.label.config(text="")

    def _animate(self):
        if not self.running:
            return
        frame = self.spinner_frames[self.current_index % len(self.spinner_frames)]
        self.label.config(text=f"{self.text_prefix} {frame}")
        self.current_index += 1
        self.parent.after(self.delay, self._animate)
