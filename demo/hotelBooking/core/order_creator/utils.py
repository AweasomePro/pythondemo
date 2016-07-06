from hotelBooking import Product
from hotelBooking.core.exceptions import PointNotEnough
from hotelBooking.core.models.orders import Order,HotelPackageOrder,HotelPackageOrderSnapShot
from hotelBooking.core.models.plugins import HotelOrderNumberGenerator
from hotelBooking.core.models.products import HousePackage
from hotelBooking.core.serializers.orders import CustomerOrderSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


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


def get_customer_member_object( request):
    if not request.user.is_customer_member:
        return DefaultJsonResponse(res_data='你还不是会员', code=-100)
    return request.user

def is_hotel_package(product):
    # return product.name == '酒店套餐'
    # todo 判断类型
    return True


def generateHotelPackageProductOrder(request):
    member_user = get_customer_member_object(request)
    productId = request.POST.get('productId')
    require_notes = request.POST.get('require_notes',default=None)
    try:
        product = Product.objects.get(id=productId)
    except Product.DoesNotExist:
        return DefaultJsonResponse(res_data='不存在该商品', code=403)
    # todo 判断是该类型的商品
    is_hotel_package(product)
    try:
        house_package = product.housepackage
    except HousePackage.DoesNotExist:
        return DefaultJsonResponse(res_data='不存在该商品', code=403)
    print('product id is {}'.format(productId))
    hotel_package_order = None
    order = None
    order = Order.objects.create(
        customer = member_user,
        franchisee = product.owner,
        product = product,
    )
    hotel_package_order = HotelPackageOrder.objects.create(
        order = order,
        require_notes =require_notes
    )
    hotel_package_order.save()
    try:
        order_numbers = HotelOrderNumberGenerator.objects.get(id="order_number")
    except HotelOrderNumberGenerator.DoesNotExist:
        order_numbers = HotelOrderNumberGenerator.objects.create(id="order_number")
    # new Order
    try:
        order_numbers.init(request,order)
    except AttributeError:
        pass
    order.number = order_numbers.get_next()
    order.save()
    hotel_package_order.save()
    snapshot = HotelPackageOrderSnapShot()
    snapshot.hotel_package_order = hotel_package_order
    snapshot.create_from_source(house_package)
    snapshot.save()
    return hotel_package_order


def add_hotel_order(request):
    print('print user')
    user = get_customer_member_object(request)
    productId = request.POST.get('productId')
    try:
        product = Product.objects.get(id=productId)
    except Product.DoesNotExist:
        return DefaultJsonResponse(res_data='不存在该商品', code=403)
    # todo 判断是该类型的商品
    is_hotel_package(product)
    try:
        house_package = product.housepackage
    except HousePackage.DoesNotExist:
        return DefaultJsonResponse(res_data='不存在该商品', code=403)
    print('product id is {}'.format(productId))
    hotelPackageOrder = generateHotelPackageProductOrder(request)
    # return DefaultJsonResponse(res_data='订购成功,id 是{0}'.format(hotelPackageOrder.order.number))
    serializer = CustomerOrderSerializer(hotelPackageOrder)

    return DefaultJsonResponse(res_data=serializer.data)

