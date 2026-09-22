from dataclasses import dataclass, field
from app.config import settings


@dataclass
class AnomalyResult:
    anomalies: dict[str, str] = field(default_factory=dict)  # alert_type -> message
    normal: list[str] = field(default_factory=list)         


def detect_anomaly(temperature: float | None, vibration: float | None) -> AnomalyResult:
    result = AnomalyResult()

    if temperature is not None:
        if temperature > settings.temperature_threshold:
            result.anomalies["high_temperature"] = (
                f"Temperature {temperature}°C exceeds threshold {settings.temperature_threshold}°C"
            )
        else:
            result.normal.append("high_temperature")

    if vibration is not None:
        if vibration > settings.vibration_threshold:
            result.anomalies["high_vibration"] = (
                f"Vibration {vibration} exceeds threshold {settings.vibration_threshold}"
            )
        else:
            result.normal.append("high_vibration")

    return result