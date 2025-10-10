import sys
import time
from enum import Enum, unique


@unique
class Locale(Enum):
    EN = 1
    DE = 2


# Change language as needed
CURRENT_LANG = Locale.DE

MESSAGES = {
    Locale.EN: {
        "out_of_range": "is out of range",
        "invalid_vital": "[ERROR] Unknown vital parameter"
    },
    Locale.DE: {
        "out_of_range": "liegt außerhalb des zulässigen Bereichs",
        "invalid_vital": "[FEHLER] Unbekannter Vitalwert"
    }
}


def local_text(key: str) -> str:
    """Return localized text depending on CURRENT_LANG."""
    return MESSAGES.get(CURRENT_LANG, MESSAGES[Locale.EN]).get(key, key)


def _blink_alert(times: int, text: str):
    """Simulate an alert animation."""
    print(text)
    for i in range(times):
        for symbol in ("*", " *"):
            print(f"\r{symbol}", end="")
            sys.stdout.flush()
            time.sleep(1)


def _within_limit(value, low, high) -> bool:
    """Check if the value lies within its valid range."""
    return low <= value <= high


def _validate_vital(name, reading, low, high):
    """Check the range and print appropriate messages."""
    if not _within_limit(reading, low, high):
        message = local_text("out_of_range")
        _blink_alert(4, f"{name} {message}!")
        return False
    print(f"[OK] {name}: {reading}")
    return True


class HealthMetric:
    """Object-oriented representation of a measurable health metric."""

    def __init__(self, label: str, lower: float, upper: float):
        self.label = label
        self.lower = lower
        self.upper = upper

    def assess(self, reading: float):
        """Evaluate if the reading is healthy."""
        if _within_limit(reading, self.lower, self.upper):
            print(f"[OK] {self.label}: {reading}")
        else:
            message = local_text("out_of_range")
            _blink_alert(2, f"{self.label} {message}!")


METRICS = {
    "temp": HealthMetric("Temperature", 95, 102),
    "pulse": HealthMetric("Pulse Rate", 60, 100),
    "spo2": HealthMetric("Oxygen Level", 90, 150),
    "glucose": HealthMetric("Blood Sugar", 70, 110),
    "bp": HealthMetric("Blood Pressure", 90, 150),
    "rr": HealthMetric("Respiration Rate", 12, 20)
}


def analyze_readings(measurements: dict):
    """Loop through each metric and evaluate."""
    for key, val in measurements.items():
        metric = METRICS.get(key)
        if not metric:
            print(f"{local_text('invalid_vital')}: {key}")
            continue
        metric.assess(val)


if __name__ == "__main__":
    sample_data = {
        "temp": 104,
        "pulse": 120,
        "spo2": 85,
        "glucose": 92,
        "bp": 160,
        "rr": 15
    }
    analyze_readings(sample_data)
