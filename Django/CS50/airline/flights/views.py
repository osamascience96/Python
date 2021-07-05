import flights
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    return render(request, "flight/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    # Way One
    # This is one way of saying that the primary key to get a specific data instead of id
    # flight = Flight.objects.get(pk=flight_id)

    # Way Two
    # but i am more fond of say get me that particular data of id
    flight = Flight.objects.get(id=flight_id)
    return render(request, "flight/flight.html", {
        # passing the flights to this view
        # passing the passengers of that flight(reverse relation)
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if(request.method == "POST"):
        # get the flight that i want to book with customer
        flight = Flight.objects.get(pk=flight_id)
        # get the passenger that i want to book the flight to 
        passenger = Passenger.objects.get(pk=int(request.POST["passengers"]))
        # add the flight to the reference of that prticular passenger flight list
        passenger.flights.add(flight)
        # redirect the user to that particular flight page 
        return HttpResponseRedirect(reverse("flights:flight", args=(flight.id,)))

