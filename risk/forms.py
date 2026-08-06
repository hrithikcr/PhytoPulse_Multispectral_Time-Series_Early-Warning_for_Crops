from django import forms

# ---------------------------------------------
# Placeholder hints (UX only, not validation)
# ---------------------------------------------
PH = {
    "ndvi": "0.00–1.00",
    "gndvi": "0.00–1.00",
    "evi": "0.00–1.00",

    "rain": "0–300 mm",
    "temp": "10–45 °C",
    "humidity": "10–100 %",

    "ndvi_lag1": "0.00–1.00",
    "ndvi_lag2": "0.00–1.00",
    "gndvi_lag1": "0.00–1.00",
    "evi_lag1": "0.00–1.00",

    "d_ndvi_1w": "−1.00–1.00",
    "d_gndvi_1w": "−1.00–1.00",
    "d_evi_1w": "−1.00–1.00",

    "re_ndvi_ratio": "0.00–2.00",
    "week": "1–52",
}

# ---------------------------------------------
# Universal numeric widget (ML-safe)
# ---------------------------------------------
def num_widget(minv=None, maxv=None):
    """
    Uses step='any' to allow unrestricted decimals.
    Prevents ALL browser step validation warnings.
    """
    attrs = {
        "class": "input",
        "step": "any",
        "placeholder": "",
    }
    if minv is not None:
        attrs["min"] = minv
    if maxv is not None:
        attrs["max"] = maxv
    return forms.NumberInput(attrs=attrs)


# ---------------------------------------------
# Manual Input Form
# ---------------------------------------------
class ManualInputForm(forms.Form):

    # Vegetation indices
    ndvi  = forms.FloatField(label="NDVI",  widget=num_widget(0, 1))
    gndvi = forms.FloatField(label="GNDVI", widget=num_widget(0, 1))
    evi   = forms.FloatField(label="EVI",   widget=num_widget(0, 1))

    # Weather
    rain     = forms.FloatField(label="Rain (mm)",     widget=num_widget(0, 300))
    temp     = forms.FloatField(label="Temp (°C)",     widget=num_widget(10, 45))
    humidity = forms.FloatField(label="Humidity (%)",  widget=num_widget(10, 100))

    # Temporal lags
    ndvi_lag1  = forms.FloatField(label="NDVI lag1",  widget=num_widget(0, 1))
    ndvi_lag2  = forms.FloatField(label="NDVI lag2",  widget=num_widget(0, 1))
    gndvi_lag1 = forms.FloatField(label="GNDVI lag1", widget=num_widget(0, 1))
    evi_lag1   = forms.FloatField(label="EVI lag1",   widget=num_widget(0, 1))

    # Weekly deltas
    d_ndvi_1w  = forms.FloatField(label="Δ NDVI (1w)",  widget=num_widget(-1, 1))
    d_gndvi_1w = forms.FloatField(label="Δ GNDVI (1w)", widget=num_widget(-1, 1))
    d_evi_1w   = forms.FloatField(label="Δ EVI (1w)",   widget=num_widget(-1, 1))

    # Ratio + time
    re_ndvi_ratio = forms.FloatField(label="Re/NDVI ratio", widget=num_widget(0, 2))
    week = forms.IntegerField(
        label="Week",
        min_value=1,
        max_value=52,
        widget=num_widget(1, 52)
    )

    # ---------------------------------------------
    # Attach placeholders dynamically
    # ---------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["placeholder"] = PH.get(name, "")
