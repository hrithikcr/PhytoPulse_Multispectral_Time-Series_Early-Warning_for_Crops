# from django.shortcuts import render
# from .forms import ManualInputForm
# from .utils import predict_one

# def home(request):
#     return render(request, "home.html", {})

# def form_view(request):
#     form = ManualInputForm(request.POST or None)
#     ctx = {"manual_form": form}
#     if request.method == "POST" and form.is_valid():
#         data = form.cleaned_data
#         prob, label, band = predict_one(data)
#         prob_pct = round(prob * 100, 1)
#         band_class = band.lower()  # "low" | "moderate" | "high"
#         return render(request, "result.html", {
#             "mode": "manual",
#             "prob": round(prob, 4),
#             "prob_pct": prob_pct,
#             "label": label,
#             "band": band,
#             "band_class": band_class,
#             "inputs": data,
#         })
#     return render(request, "form.html", ctx)

# def about(request):
#     return render(request, "about.html", {})

from django.shortcuts import render
from .forms import ManualInputForm
from .utils import predict_one

def home(request):
    return render(request, "home.html", {})

def form_view(request):
    form = ManualInputForm(request.POST or None)
    ctx = {"manual_form": form}

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        result = predict_one(data)

        band_class = result["severity"].lower()  # low | medium | high

        return render(request, "result.html", {
            "mode": "manual",
            "severity": result["severity"],
            "severity_id": result["severity_id"],
            "confidence": result["confidence"],
            "probs": result["probs"],
            "band_class": band_class,
            "inputs": data,
        })

    return render(request, "form.html", ctx)

def about(request):
    return render(request, "about.html", {})
