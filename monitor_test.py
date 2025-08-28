import pytest
from unittest.mock import patch
from monitor import vitals_ok, is_temperature_ok, is_pulse_rate_ok, is_spo2_ok


class TemperatureChecks:

    @pytest.mark.parametrize("temp", [95, 98.6, 100.5, 102])
    def test_normal_temperature_values(self, temp):
        assert is_temperature_ok(temp)

    @pytest.mark.parametrize("temp", [94.9, 90])
    def test_too_cold_temperature(self, temp):
        with patch("monitor.__display_vital_alert"):
            assert not is_temperature_ok(temp)

    @pytest.mark.parametrize("temp", [102.1, 105])
    def test_too_hot_temperature(self, temp):
        with patch("monitor.__display_vital_alert"):
            assert not is_temperature_ok(temp)

    def test_edge_temperature_limits(self):
        assert is_temperature_ok(95.0)
        assert is_temperature_ok(102.0)

        with patch("monitor.__display_vital_alert"):
            assert not is_temperature_ok(94.9999)
            assert not is_temperature_ok(102.0001)

    @pytest.mark.parametrize("bad_val", ["98.6", None, [98.6]])
    def test_invalid_temperature_inputs(self, bad_val):
        with pytest.raises(TypeError):
            is_temperature_ok(bad_val)


class PulseRateChecks:

    @pytest.mark.parametrize("pulse", [60, 70, 85, 100])
    def test_pulse_in_safe_zone(self, pulse):
        assert is_pulse_rate_ok(pulse)

    @pytest.mark.parametrize("pulse", [59, 45])
    def test_low_pulse_trigger(self, pulse):
        with patch("monitor.__display_vital_alert"):
            assert not is_pulse_rate_ok(pulse)

    @pytest.mark.parametrize("pulse", [101, 120])
    def test_high_pulse_trigger(self, pulse):
        with patch("monitor.__display_vital_alert"):
            assert not is_pulse_rate_ok(pulse)

    def test_pulse_at_boundaries(self):
        assert is_pulse_rate_ok(60)
        assert is_pulse_rate_ok(100)

        with patch("monitor.__display_vital_alert"):
            assert not is_pulse_rate_ok(59.9)
            assert not is_pulse_rate_ok(100.1)

    @pytest.mark.parametrize("invalid", ["70", None, [70]])
    def test_invalid_pulse_input(self, invalid):
        with pytest.raises(TypeError):
            is_pulse_rate_ok(invalid)


class OxygenSaturationChecks:

    @pytest.mark.parametrize("spo2", [90, 95, 99.5, 100, 150])
    def test_valid_oxygen_levels(self, spo2):
        assert is_spo2_ok(spo2)

    @pytest.mark.parametrize("spo2", [89, 85])
    def test_low_oxygen_levels(self, spo2):
        with patch("monitor.__display_vital_alert"):
            assert not is_spo2_ok(spo2)

    def test_spo2_edges(self):
        assert is_spo2_ok(90.0)
        assert is_spo2_ok(90.1)

        with patch("monitor.__display_vital_alert"):
            assert not is_spo2_ok(89.9)

    @pytest.mark.parametrize("bad", ["95", None, [95]])
    def test_invalid_spo2_inputs(self, bad):
        with pytest.raises(TypeError):
            is_spo2_ok(bad)


class VitalCombinationChecks:

    def test_all_good(self):
        assert vitals_ok(98.6, 70, 95)
        assert vitals_ok(95, 60, 90)
        assert vitals_ok(102, 100, 100)

    def test_individual_vital_failures(self):
        with patch("monitor.__display_vital_alert"):
            assert not vitals_ok(94, 70, 95)
            assert not vitals_ok(103, 70, 95)
            assert not vitals_ok(98.6, 59, 95)
            assert not vitals_ok(98.6, 101, 95)
            assert not vitals_ok(98.6, 70, 89)

    def test_multiple_failures(self):
        with patch("monitor.__display_vital_alert"):
            assert not vitals_ok(94, 59, 89)
            assert not vitals_ok(103, 101, 89)

    def test_mixed_cases(self):
        with patch("monitor.__display_vital_alert"):
            assert not vitals_ok(99, 102, 70)
        assert vitals_ok(98.1, 70, 98)

    @pytest.mark.parametrize(
        "t,p,s",
        [
            ("98.6", 70, 95),
            (98.6, "70", 95),
            (98.6, 70, "95"),
            (None, 70, 95),
        ],
    )
    def test_invalid_input_types(self, t, p, s):
        with pytest.raises(TypeError):
            vitals_ok(t, p, s)


class ExtremeValueTests:
    """Edge scenarios for vitals"""

    def test_zero_and_negative(self):
        with patch("monitor.__display_vital_alert"):
            for fn in (is_temperature_ok, is_pulse_rate_ok, is_spo2_ok):
                assert not fn(0)
                assert not fn(-5)

    def test_large_numbers(self):
        with patch("monitor.__display_vital_alert"):
            assert not is_temperature_ok(1000)
            assert not is_pulse_rate_ok(1000)
            assert not is_spo2_ok(1000)

    def test_floating_precision(self):
        assert is_temperature_ok(95.000001)
        assert is_pulse_rate_ok(60.000001)
        assert is_spo2_ok(90.000001)


if __name__ == "__main__":
    pytest.main([__file__])
