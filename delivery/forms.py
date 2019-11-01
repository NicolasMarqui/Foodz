from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente