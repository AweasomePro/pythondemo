
def generate_hotel_min_price_cache_key(hotel,date):
    return 'hotel_min_pirce_cache_{}_{}'.format(hotel.id,date)