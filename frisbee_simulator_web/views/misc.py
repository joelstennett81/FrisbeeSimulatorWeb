import random
from django.db.models import Avg
from faker import Faker
from frisbee_simulator_web.models import Player

fake = Faker()


def create_random_player(request, primary_line, primary_position):
    player = Player(
        first_name=generate_random_first_name(6),
        last_name=generate_random_last_name(50),
        jersey_number=random.randint(0, 99),
        height_in_inches=random.randint(60, 90),
        weight_in_lbs=random.randint(60, 90),
        speed=random.randint(60, 90),
        jumping=random.randint(60, 90),
        agility=random.randint(60, 90),
        deep_huck_cut_defense=random.randint(60, 90),
        short_huck_cut_defense=random.randint(60, 90),
        under_cut_defense=random.randint(60, 90),
        handle_mark_defense=random.randint(60, 90),
        handle_cut_defense=random.randint(60, 90),
        deep_huck_cut_offense=random.randint(60, 90),
        short_huck_cut_offense=random.randint(60, 90),
        under_cut_offense=random.randint(60, 90),
        handle_cut_offense=random.randint(60, 90),
        swing_throw_offense=random.randint(60, 90),
        under_throw_offense=random.randint(60, 90),
        short_huck_throw_offense=random.randint(60, 90),
        deep_huck_throw_offense=random.randint(60, 90),
        primary_line=primary_line,
        primary_position=primary_position
    )
    if primary_position == 'HYBRID':  # Has same rating on both offense and defense
        player.deep_huck_cut_defense = random.randint(60, 75)
        player.short_huck_cut_defense = random.randint(60, 75)
        player.under_cut_defense = random.randint(60, 75)
        player.handle_mark_defense = random.randint(60, 75)
        player.handle_cut_defense = random.randint(60, 75)
        player.deep_huck_cut_offense = random.randint(60, 75)
        player.short_huck_cut_offense = random.randint(60, 75)
        player.under_cut_offense = random.randint(60, 75)
        player.handle_cut_offense = random.randint(60, 75)
        player.swing_throw_offense = random.randint(60, 75)
        player.under_throw_offense = random.randint(60, 75)
        player.short_huck_throw_offense = random.randint(60, 75)
        player.deep_huck_throw_offense = random.randint(60, 75)
    if primary_line == 'OFFENSE':
        player.primary_line == 'OFFENSE'
        if primary_position == 'HANDLE':
            player.deep_huck_cut_defense = random.randint(50, 65)
            player.short_huck_cut_defense = random.randint(50, 65)
            player.under_cut_defense = random.randint(50, 65)
            player.handle_mark_defense = random.randint(60, 80)
            player.handle_cut_defense = random.randint(50, 65)
            player.deep_huck_cut_offense = random.randint(60, 75)
            player.short_huck_cut_offense = random.randint(60, 75)
            player.under_cut_offense = random.randint(60, 75)
            player.handle_cut_offense = random.randint(75, 90)
            player.swing_throw_offense = random.randint(75, 90)
            player.under_throw_offense = random.randint(75, 90)
            player.short_huck_throw_offense = random.randint(75, 90)
            player.deep_huck_throw_offense = random.randint(75, 90)
        elif primary_position == 'CUTTER':
            player.deep_huck_cut_defense = random.randint(60, 80)
            player.short_huck_cut_defense = random.randint(60, 80)
            player.under_cut_defense = random.randint(60, 80)
            player.handle_mark_defense = random.randint(50, 65)
            player.handle_cut_defense = random.randint(50, 65)
            player.deep_huck_cut_offense = random.randint(75, 90)
            player.short_huck_cut_offense = random.randint(75, 90)
            player.under_cut_offense = random.randint(75, 90)
            player.handle_cut_offense = random.randint(60, 75)
            player.swing_throw_offense = random.randint(60, 75)
            player.under_throw_offense = random.randint(60, 75)
            player.short_huck_throw_offense = random.randint(60, 75)
            player.deep_huck_throw_offense = random.randint(60, 75)
    elif primary_line == 'DEFENSE':
        if primary_position == 'HANDLE':
            player.deep_huck_cut_defense = random.randint(60, 75)
            player.short_huck_cut_defense = random.randint(60, 75)
            player.under_cut_defense = random.randint(60, 75)
            player.handle_mark_defense = random.randint(75, 90)
            player.handle_cut_defense = random.randint(75, 90)
            player.deep_huck_cut_offense = random.randint(50, 65)
            player.short_huck_cut_offense = random.randint(50, 65)
            player.under_cut_offense = random.randint(50, 65)
            player.handle_cut_offense = random.randint(60, 75)
            player.swing_throw_offense = random.randint(60, 75)
            player.under_throw_offense = random.randint(60, 75)
            player.short_huck_throw_offense = random.randint(60, 75)
            player.deep_huck_throw_offense = random.randint(60, 75)
        elif primary_position == 'CUTTER':
            player.deep_huck_cut_defense = random.randint(75, 90)
            player.short_huck_cut_defense = random.randint(75, 90)
            player.under_cut_defense = random.randint(75, 90)
            player.handle_mark_defense = random.randint(60, 75)
            player.handle_cut_defense = random.randint(60, 75)
            player.deep_huck_cut_offense = random.randint(60, 75)
            player.short_huck_cut_offense = random.randint(60, 75)
            player.under_cut_offense = random.randint(60, 75)
            player.handle_cut_offense = random.randint(50, 65)
            player.swing_throw_offense = random.randint(50, 65)
            player.under_throw_offense = random.randint(50, 65)
            player.short_huck_throw_offense = random.randint(50, 65)
            player.deep_huck_throw_offense = random.randint(50, 65)
    player.overall_handle_offense_rating = calculate_handle_offense_rating(player)
    player.overall_handle_defense_rating = calculate_handle_defense_rating(player)
    player.overall_cutter_offense_rating = calculate_cutter_offense_rating(player)
    player.overall_cutter_defense_rating = calculate_cutter_defense_rating(player)
    player.overall_rating = calculate_overall_player_rating(player)
    player.created_by = request.user.profile
    player.save()
    return player


def generate_random_first_name(length):
    return fake.name()[:length]


def generate_random_last_name(length):
    return fake.last_name()[:length]


def generate_random_city(length):
    return fake.city()[:length]


def generate_random_mascot():
    animals = ['Aardvarks', 'Albatrosses', 'Alligators', 'Alpacas', 'Ants', 'Anteaters', 'Antelopes', 'Apes',
               'Armadillos', 'Asp', 'Baboons', 'Badgers', 'Barracudas', 'Bass', 'Bats', 'Bears', 'Beavers', 'Bees',
               'Bison', 'Boars', 'Buffaloes', 'Butterflies', 'Camels', 'Carp', 'Caterpillars', 'Cheetahs', 'Chickens',
               'Chimpanzees', 'Cobras', 'Cockroaches', 'Cods', 'Cougars', 'Cows', 'Coyotes', 'Crabs', 'Cranes',
               'Crocodiles', 'Crows', 'Deer',
               'Dingos', 'Dolphins', 'Donkeys', 'Doves', 'Dragonflies', 'Ducks', 'Eagles', 'Echidna', 'Eels',
               'Elephants',
               'Emus', 'Falcons', 'Ferrets', 'Fishes', 'Flamingos', 'Flies', 'Foxes', 'Frogs', 'Gazelles', 'Geckos',
               'Gerbils', 'Giraffes',
               'Goats',
               'Goldfish',
               'Geese', 'Gorillas', 'Grasshoppers', 'Grizzlies', 'Guinea pigs', 'Hamsters', 'Hares', 'Hawks',
               'Hippopotamuses',
               'Horses', 'Hummingbirds', 'Hyenas', 'Iguanas', 'Impalas', 'Jackals', 'Jaguars', 'Jellyfish', 'Kangaroos',
               'Koalas', 'Koi', 'Komodo dragons', 'Kou-preys', 'Kudus', 'Ladybirds', 'Lapwings', 'Lemurs', 'Leopards',
               'Lions',
               'Llamas', 'Lobsters', 'Loris', 'Louses', 'Lynxes', 'Mallards', 'Mammoths', 'Manatees', 'Mandrills',
               'Mantises',
               'Martens', 'Meerkats', 'Minks', 'Moles', 'Mongooses', 'Monkeys', 'Moose', 'Mosquitoes', 'Moths', 'Mice',
               'Mules',
               'Narwhals', 'Newts', 'Nightingales', 'Octopuses', 'Okapis', 'Opossums', 'Ostriches', 'Otters', 'Owls',
               'Oxes',
               'Oysters', 'Pandas', 'Panthers', 'Parrots', 'Partridges', 'Peacocks', 'Pelicans', 'Penguins',
               'Pheasants', 'Pigs',
               'Pigeons', 'Pikas', 'Polar bears', 'Porcupines', 'Porpoises', 'Possums', 'Prairie dogs', 'Prawns',
               'Puffins',
               'Pumas', 'Pythons', 'Quails', 'Queleas', 'Quokkas', 'Rabbits', 'Raccoons', 'Rails', 'Rams', 'Rats',
               'Ravens',
               'Red deer', 'Red pandas', 'Reindeer', 'Rhinoceroses', 'Right whales', 'Roadrunners', 'Rooks',
               'Rottweilers',
               'Ruffs', 'Salamanders', 'Salmon', 'Sandpipers', 'Sardines', 'Scorpions', 'Seahorses', 'Seals', 'Sharks',
               'Sheep',
               'Shrews', 'Shrimps', 'Snakes', 'Snails', 'Sparrows', 'Spiders', 'Spoonbills', 'Squids', 'Squirrels',
               'Starfish',
               'Stingrays', 'Stinkpots', 'Stoats', 'Sturgeons', 'Swallows', 'Swans', 'Tapirs', 'Tarsiers', 'Termites',
               'Tigers',
               'Toads', 'Trouts', 'Turkeys', 'Turtles', 'Vipers', 'Vultures', 'Walruses', 'Wasps', 'Water buffaloes',
               'Weasels',
               'Whales', 'Whippets', 'Wildebeests', 'Wolves', 'Wolverines', 'Wombats', 'Woodpeckers', 'Worms', 'Wrens',
               'Yaks',
               'Zebras']

    return random.choice(animals)


def calculate_overall_player_rating(player):
    rating_attributes = [
        player.speed, player.jumping, player.agility, player.deep_huck_cut_defense, player.short_huck_cut_defense,
        player.under_cut_defense, player.handle_mark_defense, player.handle_cut_defense, player.deep_huck_cut_offense,
        player.short_huck_cut_offense, player.under_cut_offense, player.handle_cut_offense, player.swing_throw_offense,
        player.under_throw_offense, player.short_huck_throw_offense, player.deep_huck_throw_offense
    ]
    rating_sum = sum(rating_attributes)
    overall_rating = rating_sum / len(rating_attributes)
    return overall_rating


def calculate_handle_offense_rating(player):
    rating_attributes = [
        player.handle_cut_offense, player.swing_throw_offense, player.under_throw_offense,
        player.short_huck_throw_offense, player.deep_huck_throw_offense
    ]
    rating_sum = sum(rating_attributes)
    overall_handle_offense_rating = rating_sum / len(rating_attributes)
    return overall_handle_offense_rating


def calculate_handle_defense_rating(player):
    rating_attributes = [
        player.handle_mark_defense, player.handle_cut_defense
    ]
    rating_sum = sum(rating_attributes)
    overall_handle_defense_rating = rating_sum / len(rating_attributes)
    return overall_handle_defense_rating


def calculate_cutter_offense_rating(player):
    rating_attributes = [
        player.deep_huck_cut_offense, player.short_huck_cut_offense, player.under_cut_offense,
    ]
    rating_sum = sum(rating_attributes)
    overall_cutter_offense_rating = rating_sum / len(rating_attributes)
    return overall_cutter_offense_rating


def calculate_cutter_defense_rating(player):
    rating_attributes = [
        player.deep_huck_cut_defense, player.short_huck_cut_defense, player.under_cut_defense
    ]
    rating_sum = sum(rating_attributes)
    overall_cutter_defense_rating = rating_sum / len(rating_attributes)
    return overall_cutter_defense_rating


def calculate_overall_team_rating(team):
    overall_rating = team.players.all().aggregate(Avg('overall_rating')).get('overall_rating__avg')
    print('team players: ', team.players.all())
    print('overall rating: ', overall_rating)
    return overall_rating
