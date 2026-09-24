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

def test_temperature_exactly_at_threshold_is_not_anomaly():
    result = detect_anomaly(temperature=80.0, vibration=3.0)

    assert "high_temperature" not in result.anomalies


def test_temperature_just_above_threshold_is_anomaly():
    result = detect_anomaly(temperature=80.1, vibration=3.0)

    assert "high_temperature" in result.anomalies


def test_temperature_just_below_threshold_is_not_anomaly():
    result = detect_anomaly(temperature=79.9, vibration=3.0)

    assert "high_temperature" not in result.anomalies