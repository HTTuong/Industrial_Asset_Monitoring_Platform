from dataclasses import dataclass
from app.config import settings


@dataclass
class AnomalyResult:
    is_anomaly: bool
    reasons: list[str]


def detect_anomaly(temperature: float | None, vibration: float | None) -> AnomalyResult:
    reasons = []

    if temperature is not None and temperature > settings.temperature_threshold:
        reasons.append(f"Temperature {temperature}°C exceeds threshold {settings.temperature_threshold}°C")

    if vibration is not None and vibration > settings.vibration_threshold:
        reasons.append(f"Vibration {vibration} exceeds threshold {settings.vibration_threshold}")

    return AnomalyResult(is_anomaly=len(reasons) > 0, reasons=reasons)