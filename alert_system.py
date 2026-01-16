from datetime import datetime, timedelta
import pyttsx3


class AlertManager:
    """
    Central alert handling system for VigilDrive AI
    """

    def __init__(self, cooldown_seconds=5):
        self.last_alert_time = None
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.alert_count = 0

        # Text-to-speech engine (cross-platform)
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)

    def handle_detection(self, detection_result: dict):
        """
        Entry point used by detector/app.
        Expects detector output dictionary.
        """
        alert_level = detection_result.get("alert_level", "LOW")
        confidence = detection_result.get("confidence", 0.0)

        self.trigger_alert(alert_level, confidence)

    def trigger_alert(self, level: str, confidence: float = 0.0):
        now = datetime.now()

        # Prevent alert spam
        if self.last_alert_time and now - self.last_alert_time < self.cooldown:
            return

        if level == "LOW":
            return  # no alert

        if level == "MEDIUM":
            self.visual_alert(level, confidence)

        elif level == "HIGH":
            self.visual_alert(level, confidence)
            self.voice_warning()

        self.last_alert_time = now
        self.alert_count += 1

    def visual_alert(self, level: str, confidence: float):
        print(
            f"🚨 ALERT [{level}] | Confidence: {confidence:.2f} | "
            f"Time: {datetime.now().strftime('%H:%M:%S')}"
        )

    def voice_warning(self):
        self.engine.say(
            "Warning. Driver fatigue detected. Please take a break."
        )
        self.engine.runAndWait()
