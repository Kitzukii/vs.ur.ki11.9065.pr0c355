import requests, threading, json
import tkinter as tk
from tkinter import ttk

class GitRepo: # lua style. (bootstrap/apioframe-cores reference)
    def __init__(self, user, repo, branch):
        self.__repo_base_url__ = f"https://raw.githubusercontent.com/{user}/{repo}"
        self.branch = branch

    def getFile(self, path: str) -> bytes:
        r = requests.get(
            f"{self.__repo_base_url__}/refs/heads/{self.branch}/{path}",
            timeout=15)
        r.raise_for_status()
        return r.content

    def getJsonFile(self, path: str) -> dict:
        r = requests.get(
            f"{self.__repo_base_url__}/refs/heads/{self.branch}/{path}",
            timeout=15)
        r.raise_for_status()
        return json.loads(r.content)

class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        root.title("vs.ur.ki11.9065.pr0c355")
        root.geometry("420x180")
        root.resizable(False, False)

        self.status = tk.StringVar(value="Idle")
        self.progress = tk.IntVar(value=0)

        ttk.Label(root, text="Status:").pack(anchor="w", padx=10, pady=(10,0))
        ttk.Label(root, textvariable=self.status).pack(anchor="w", padx=20)

        self.bar = ttk.Progressbar(root, maximum=100, variable=self.progress)
        self.bar.pack(fill="x", padx=10, pady=10)

        self.start_btn = ttk.Button(root, text="Start Download", command=self.start)
        self.start_btn.pack(pady=10)

        self.lock = threading.Lock()
        self.total = 0
        self.completed = 0
        self.finished = False

    def start(self):
        self.start_btn.config(state="disabled")
        self.status.set("Fetching metadata...")
        threading.Thread(target=self.run, daemon=True).start()
        self.root.after(100, self.watch_completion)

    def run(self):
        try:
            repo = GitRepo("Kitzukii", "vs.ur.ki11.9065.pr0c355", "main")
            meta = repo.getJsonFile("fs.json")

            prefix = meta.get("prefix", "mods")
            files = meta.get("files", [])

            if not prefix.endswith("/"):
                prefix += "/"

            self.total = len(files)

            if self.total == 0:
                self.completed = 0
                return

            self.status.set(f"Downloading {self.total} files...")

            for file in files:
                threading.Thread(
                    target=self.download,
                    args=(repo, prefix, file),
                    daemon=True
                ).start()

        except Exception as e:
            self.status.set(f"Error: {e}")

    def download(self, repo, prefix, file):
        try:
            data = repo.getFile(prefix + file)
            with open(file, "wb") as f:
                f.write(data)
        finally:
            with self.lock:
                self.completed += 1

    def watch_completion(self):
        with self.lock:
            done = self.completed
            total = self.total

        if total > 0:
            percent = int((done / total) * 100)
            self.progress.set(percent)
            self.status.set(f"Downloaded {done}/{total}")

        if total > 0 and done >= total and not self.finished:
            self.finish()
            return

        self.root.after(100, self.watch_completion)

    def finish(self):
        self.finished = True
        self.progress.set(100)
        self.status.set("Finished downloading.\nYou can now close this window.\nEnjoy!")
        # self.root.after(5000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    DownloaderGUI(root)
    root.mainloop()