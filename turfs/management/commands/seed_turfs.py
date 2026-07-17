from datetime import time
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from turfs.models import Amenity, Sport, TimeSlot, Turf


TURFS = [
    ("Greenfield Arena", "Velachery", "A bright, well-kept football ground built for energetic evening matches.", "Football", 900),
    ("Skyline Sports Hub", "Anna Nagar", "A premium rooftop box cricket venue with clean changing rooms and city views.", "Box Cricket", 1200),
    ("Goal Rush Turf", "Tambaram", "A lively five-a-side football arena with professional floodlights.", "Football", 850),
    ("Smash Point Court", "T Nagar", "A polished indoor badminton court for relaxed rallies and competitive games.", "Badminton", 700),
    ("Boundary Box", "Medavakkam", "A spacious box cricket venue made for weekend teams and big hits.", "Box Cricket", 1100),
    ("Ace Arena", "Adyar", "A calm tennis court with a smooth surface and comfortable spectator seating.", "Tennis", 950),
    ("Hoop House", "Nungambakkam", "An indoor basketball court designed for fast-paced pickup games.", "Basketball", 800),
    ("Volley Vista", "Perambur", "A breezy volleyball court with quality nets and ample team space.", "Volleyball", 750),
    ("Pitch Perfect", "Porur", "A full-service football turf with safe turfing and a friendly local vibe.", "Football", 1000),
    ("Power Play Sports", "Guindy", "A versatile multi-sport space for cricket practice and football fixtures.", "Cricket", 950),
    ("Net Ninjas", "Thoraipakkam", "Modern badminton courts with high ceilings and glare-free lighting.", "Badminton", 650),
    ("Strike Zone", "Ambattur", "A cricket-focused arena with a firm wicket and wide hitting lanes.", "Cricket", 900),
    ("Urban Kickoff", "Sholinganallur", "A contemporary football turf that stays cool under powerful night lights.", "Football", 1050),
    ("Rally Republic", "Mylapore", "A welcoming table tennis studio for quick games after work.", "Table Tennis", 500),
    ("Champions Court", "Koyambedu", "A large basketball facility with a tournament-style playing surface.", "Basketball", 850),
    ("Weekend Warriors", "Pallikaranai", "A group-friendly box cricket spot with plenty of room to relax between overs.", "Box Cricket", 1000),
    ("Sunrise Sports Park", "ECR", "An open-air sports venue ideal for early-morning football and cricket.", "Football", 950),
    ("Court Kings", "Vadapalani", "A centrally located badminton venue with reliable courts and easy access.", "Badminton", 700),
    ("All Star Arena", "Mogappair", "A well-equipped multi-sport arena for teams that want a smooth booking experience.", "Volleyball", 800),
    ("Victory Grounds", "Chromepet", "A dependable neighbourhood football ground for regular league games.", "Football", 850),
]


class Command(BaseCommand):
    help = "Create 20 sample TurfArena venues, amenities, and slots."

    def handle(self, *args, **options):
        user_model = get_user_model()
        owner, _ = user_model.objects.get_or_create(username="turfarena_owner", defaults={"role": "OWNER", "email": "owner@turfarena.local"})
        sports = {name: Sport.objects.get_or_create(name=name)[0] for name in {item[3] for item in TURFS}}
        amenities = {name: Amenity.objects.get_or_create(name=name)[0] for name in ["Parking Available", "Drinking Water", "Changing Room", "Floodlights", "Washroom", "First Aid"]}
        for index, (name, area, description, sport_name, price) in enumerate(TURFS, start=1):
            turf, created = Turf.objects.get_or_create(
                slug=name.lower().replace(" ", "-").replace(".", ""),
                defaults={"owner": owner, "name": name, "description": description, "address": f"{index} Sports Lane, {area}, Chennai", "city": "Chennai", "area": area, "base_price": Decimal(price), "capacity": 12, "size": "5-a-side", "rules": "Non-marking shoes required. Please arrive 10 minutes before your slot.", "is_featured": True},
            )
            turf.sports.add(sports[sport_name])
            turf.amenities.add(*amenities.values())
            for start_hour in (6, 7, 18, 19, 20):
                TimeSlot.objects.get_or_create(turf=turf, start_time=time(start_hour), end_time=time((start_hour + 1) % 24), defaults={"price": Decimal(price)})
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Kept'}: {name}"))
