from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # Add more fields as per your requirements, e.g., age, gender, etc.

    def __str__(self):
        return self.username

    def full_name(self):
        return f"{self.first_name} {self.last_name if self.last_name else ''}"

from django.db import models

class CalorieIntake(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    intake_date = models.DateField()
    morning_calories = models.IntegerField(default=0)
    mid_morning_calories = models.IntegerField(default=0)
    afternoon_calories = models.IntegerField(default=0)
    mid_afternoon_calories = models.IntegerField(default=0)
    evening_calories = models.IntegerField(default=0)

    def total_calories(self):
        return (
            self.morning_calories +
            self.mid_morning_calories +
            self.afternoon_calories +
            self.mid_afternoon_calories +
            self.evening_calories
        )

    def __str__(self):
        return f"{self.customer.username}'s Calorie Intake on {self.intake_date}"
    
from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.FloatField()  # in grams
    carbohydrates = models.FloatField()  # in grams
    fats = models.FloatField()  # in grams

    def __str__(self):
        return self.name

    def nutrient_summary(self):
        return f"{self.name}: {self.calories} kcal, {self.protein}g protein, {self.carbohydrates}g carbs, {self.fats}g fats"

class Consumption(models.Model):
    intake = models.ForeignKey('CalorieIntake', on_delete=models.CASCADE)
    time_of_day = models.CharField(max_length=20)  # e.g., "morning", "mid-morning", etc.
    food_items = models.ManyToManyField('FoodItem', through='ConsumedFood')

    def total_calories(self):
        total = 0
        for consumed_food in self.consumed_food.all():
            total += consumed_food.food_item.calories * consumed_food.quantity
        return total

    def __str__(self):
        return f"{self.intake.customer.first_name} consumed at {self.time_of_day}"

class ConsumedFood(models.Model):
    consumption = models.ForeignKey(Consumption, related_name='consumed_food', on_delete=models.CASCADE)
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_calories(self):
        return self.food_item.calories * self.quantity

    def __str__(self):
        return f"{self.consumption.intake.customer.first_name} consumed {self.quantity} {self.food_item.name}"


