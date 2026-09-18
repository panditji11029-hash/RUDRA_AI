import sys
import time
import threading


class Animation:

    def __init__(self):
        self.running = False
        self.thread = None

    def start(self, mode="thinking"):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=0.3)

        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()

    def _run(self):

        # ANSI colors
        cyan = "\033[96m"
        blue = "\033[94m"
        purple = "\033[95m"
        reset = "\033[0m"

        frames = [
            f"{cyan}●{reset}  THINKING",
            f"{blue}●{cyan}●{reset}  THINKING",
            f"{purple}●{blue}●{cyan}●{reset}  THINKING",
            f"{blue}●{purple}●{blue}●{cyan}●{reset}  THINKING",
            f"{cyan}●{blue}●{purple}●{blue}●{cyan}●{reset}  THINKING",
            f"{blue}●{purple}●{blue}●{cyan}●{blue}●{reset}  THINKING",
            f"{purple}●{blue}●{cyan}●{reset}  THINKING",
            f"{blue}●{cyan}●{reset}  THINKING",
        ]

        i = 0

        while self.running:

            frame = frames[i % len(frames)]

            sys.stdout.write(
                "\r" + frame + " " * 20
            )

            sys.stdout.flush()

            i += 1
            time.sleep(0.10)


animation = Animation()