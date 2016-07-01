from hotelBooking.core.exceptions import PointNotEnough


def get_customermember(request):
    try:
        return request.user.customermember
    except AttributeError:
        return None


def get_hotelPackageProduct(request):
    pass


def verifyPointEnough(customer, hotelPackageProduct):
    if customer.user.point <= hotelPackageProduct.need_point:
        raise PointNotEnough(detail='购买该套餐个所需积分不够')


def add_hotel_order(request):
    customer = get_customermember(request)
    hotelPackageProduct = get_hotelPackageProduct(request)
    order = None
    verifyPointEnough(customer,hotelPackageProduct)

