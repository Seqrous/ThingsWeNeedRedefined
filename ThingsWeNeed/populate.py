import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ThingsWeNeed.settings')

import django
django.setup()

from faker import Faker
fake = Faker()

import random

from shopping_app import models

HOUSEHOLD_NAMES = [
    'HouseholdOne', 'OurPlace', 'Treehouse',
    'Submarine', 'Nuclear Bunker', 'Akudama',
    'The House of Wolves', 'Cave', 'PiggyHouse']

PRODUCT_NAMES = [
    'charger', 'candy wrapper', 'pillow', 'carrots', 'clothes', 'blouse',
    'ice cube tray', 'vase', 'wallet', 'tire swing', 'sandal', 'chapter book', 
    'thread', 'outlet', 'rug', 'couch', 'floor', 'keys', 'bowl', 'purse',
    'tweezers', 'cat', 'photo album', 'door', 'pencil', 'magnet', 'flag',
    'plastic fork', 'ring', 'computer', 'helmet', 'cup', 'nail clippers',
    'greeting card', 'eraser', 'conditioner', 'sticky note', 'headphones',
    'clamp', 'sailboat', 'rubber duck', 'keyboard', 'screw', 'sun glasses',
    'nail file', 'glasses', 'stop sign', 'slipper', 'checkbook', 'brocolli',
    'model car', 'newspaper', 'candle', 'teddies', 'soap', 'street lights',
    'clock', 'tree', 'CD', 'seat belt', 'water bottle', 'phone', 'clay pot', 
    'key chain', 'lamp shade', 'box', 'apple', 'video games', 'wagon', 
    'button', 'toilet', 'truck', 'pool stick', 'banket', 'monitor', 
    'washing machine', 'perfume', 'shirt', 'cell phone', 'twister'
]

USER_LIST = []
HOUSEHOLD_LIST = []

def populate_user(n_users=20):
    for i in range(n_users):
        print(f'New user ({i+1}/{n_users})')
        username = fake.name
        email = fake.email
        password = fake.password(length=12)

        new_user = models.User.objects.get_or_create(
            is_superuser='False', password=password, 
            username=username, email=email
        )[0]
        new_user.save()
        USER_LIST.append(new_user)

def populate_household(n_households=7):
    for i in range(n_households):
        print(f'New household ({i+1}/{n_households})')
        name = HOUSEHOLD_NAMES[i]
        address = models.Address.objects.get_or_create(
            country = fake.country(),
            city = fake.city(),
            postal_code = fake.postcode(),
            street_address = fake.street_address()
        )[0]
        created_by = USER_LIST[random.randint(0, len(USER_LIST)-1)]

        new_household = models.Household.objects.get_or_create(
            name = name, 
            address = address,
            created_by = created_by
        )[0]
        new_household.save()
        HOUSEHOLD_LIST.append(new_household)

def populate_household_member():
    for i, household in enumerate(HOUSEHOLD_LIST):
        print(f'New household membership ({i+1}/{len(HOUSEHOLD_LIST)})')
        # Make the creator a member
        membership = models.HouseholdMember.objects.get_or_create(
            user = household.created_by,
            household = household
        )[0]
        membership.save()

        # Random amount of members, select unique and add to membership
        users_number = random.randint(0, 5)
        users = random.sample(USER_LIST, users_number)
        for user in users:
            membership = models.HouseholdMember.objects.get_or_create(
                user = user,
                household = household
            )[0]
            membership.save()

def populate_product(n_products=80):
    for i in range(n_products):
        print(f'New product ({i+1}/{n_products})')
        name = PRODUCT_NAMES[i]
        max_price = float(random.randint(10, 300))
        actual_price = float(random.randint(10, 300))
        quantity = random.randint(1, 20)
        info = fake.catch_phrase() if random.randint(0, 1) == 1 else ""
        is_wish = True if random.randint(0, 1) == 1 else False
        household = HOUSEHOLD_LIST[random.randint(0, len(HOUSEHOLD_LIST)-1)]
        posted_by = USER_LIST[random.randint(0, len(USER_LIST)-1)]
        bought_by = USER_LIST[random.randint(0, len(USER_LIST)-1)] if random.randint(0, 1) == 1 else None

        new_product = models.Product.objects.get_or_create(
            name = name, max_price = max_price,
            actual_price = actual_price, quantity=quantity,
            info = info, is_wish = is_wish,
            household = household, posted_by = posted_by,
            bought_by = bought_by
        )[0]
        new_product.save()

if __name__=="__main__":
    print('Populating..')
    populate_user()
    populate_household()
    populate_household_member()
    populate_product()
    print('Finished')