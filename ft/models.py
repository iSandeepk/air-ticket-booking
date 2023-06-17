from django.db import models
import random
import datetime
class ft(models.Model):
    date_of_journey = models.DateField()
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seats_available = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    company_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.source} to {self.destination} - {self.date_of_journey} ({self.company_name})"

    class Meta:
        verbose_name_plural = "fts"
# Create your models here.

company_names = ['Indigo', 'Air India', 'SpiceJet', 'Vistara', 'GoAir']
cities_in_india = ['Mumbai', 'Delhi', 'Kolkata', 'Chennai', 'Bengaluru', 'Hyderabad', 'Jaipur', 'Ahmedabad', 'Pune', 'Lucknow']

sample_ft = []
start_date = datetime.date.today() + datetime.timedelta(days=1)

# Generate sample planes with different dates and random source/destination within India
for i in range(20):
    date_of_journey = start_date + datetime.timedelta(days=i)
    source = random.choice(cities_in_india)
    destination = random.choice(cities_in_india)

    seats_available = random.randint(0, 60)
    price = round(random.uniform(2000, 4000), 2)
    company_name = random.choice(company_names)

    ft_instance = ft.objects.create(
        date_of_journey=date_of_journey,
        source=source,
        destination=destination,
        seats_available=seats_available,
        price=price,
        company_name=company_name
    )
    sample_ft.append(ft_instance)


from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plane = models.ForeignKey(ft, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    # other booking fields

    def __str__(self):
        return f"{self.user.username} - {self.plane}"

