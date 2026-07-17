from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TimeSlotForm, TurfForm
from .models import Sport, Turf


def manager_required(view):
    """Allow staff/superusers and turf owners into venue management."""
    @login_required
    def wrapped(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_owner:
            return view(request, *args, **kwargs)
        raise PermissionDenied("Turf management is available to owners only.")
    return wrapped


def managed_turfs(user):
    queryset = Turf.objects.prefetch_related("sports", "slots")
    return queryset if user.is_superuser else queryset.filter(owner=user)


def turf_list(request):
    turfs = Turf.objects.filter(is_active=True).prefetch_related("sports", "amenities")
    q = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    sport = request.GET.get("sport", "").strip()
    if q: turfs = turfs.filter(Q(name__icontains=q) | Q(area__icontains=q) | Q(city__icontains=q))
    if city: turfs = turfs.filter(city__iexact=city)
    if sport: turfs = turfs.filter(sports__id=sport)
    return render(request, "turfs/list.html", {"turfs": turfs.distinct(), "sports": Sport.objects.all()})


def turf_detail(request, slug):
    turf = get_object_or_404(Turf.objects.prefetch_related("sports", "amenities", "slots", "images"), slug=slug, is_active=True)
    return render(request, "turfs/detail.html", {"turf": turf})


@manager_required
def manage_list(request):
    return render(request, "turfs/manage/list.html", {"turfs": managed_turfs(request.user)})


@manager_required
def manage_create(request):
    form = TurfForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        turf = form.save(commit=False)
        turf.owner = request.user
        turf.save()
        form.save_m2m()
        messages.success(request, "Turf created. Add slots so customers can book it.")
        return redirect("turfs:manage_edit", pk=turf.pk)
    return render(request, "turfs/manage/form.html", {"form": form, "page_title": "Add a turf"})


@manager_required
def manage_edit(request, pk):
    turf = get_object_or_404(managed_turfs(request.user), pk=pk)
    form = TurfForm(request.POST or None, instance=turf)
    slot_form = TimeSlotForm(request.POST or None, prefix="slot")
    if request.method == "POST" and "save_turf" in request.POST and form.is_valid():
        form.save()
        messages.success(request, "Turf details updated.")
        return redirect("turfs:manage_edit", pk=turf.pk)
    if request.method == "POST" and "add_slot" in request.POST and slot_form.is_valid():
        slot = slot_form.save(commit=False)
        slot.turf = turf
        slot.save()
        messages.success(request, "Time slot added.")
        return redirect("turfs:manage_edit", pk=turf.pk)
    return render(request, "turfs/manage/form.html", {"form": form, "slot_form": slot_form, "turf": turf, "page_title": f"Edit {turf.name}"})


@manager_required
def manage_delete(request, pk):
    turf = get_object_or_404(managed_turfs(request.user), pk=pk)
    if request.method == "POST":
        turf.delete()
        messages.success(request, "Turf deleted.")
        return redirect("turfs:manage_list")
    return render(request, "turfs/manage/confirm_delete.html", {"turf": turf})
