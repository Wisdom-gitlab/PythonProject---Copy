from django.contrib import admin

import food_items

# Register your models here.
admin.site.register(food_items.models.Category)
admin.site.register(food_items.models.Product)
admin.site.register(food_items.models.Order)
admin.site.register(food_items.models.OrderItem)
admin.site.register(food_items.models.Cart)
admin.site.register(food_items.models.CartItem)

