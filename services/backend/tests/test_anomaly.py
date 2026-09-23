from app.anomaly import detect_anomaly


def test_normal_readings_produce_no_anomaly():
    result = detect_anomaly(temperature=45.5, vibration=3.0)

    assert result.anomalies == {}
    assert "high_temperature" in result.normal
    assert "high_vibration" in result.normal


def test_high_temperature_triggers_anomaly():
    result = detect_anomaly(temperature=95.0, vibration=3.0)

    assert "high_temperature" in result.anomalies
    assert "high_vibration" not in result.anomalies


def test_high_vibration_triggers_anomaly():
    result = detect_anomaly(temperature=45.5, vibration=9.5)

    assert "high_vibration" in result.anomalies
    assert "high_temperature" not in result.anomalies


def test_both_thresholds_exceeded_together():
    result = detect_anomaly(temperature=95.0, vibration=9.5)

    assert "high_temperature" in result.anomalies
    assert "high_vibration" in result.anomalies
    assert len(result.anomalies) == 2