import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from technique.models import TechniqueType
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from notification.models import Notification
from .serializers import *
from notification.services import createNotification



class OrdersResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links':{
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            },
            'page_count':self.page.paginator.count,
            'results':data
        })

class OrdersSubscribe(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.GET.get('type') == 'add':
            t_type = TechniqueType.objects.get(id=request.GET.get('type_id'))
            request.user.subscribe_type.add(t_type)
            return Response(status=201)
        if request.GET.get('type') == 'del':
            t_type = TechniqueType.objects.get(id=request.GET.get('type_id'))
            request.user.subscribe_type.remove(t_type)
            return Response(status=200)

class OrderGet(generics.RetrieveAPIView):
    print('queryset')
    serializer_class = OrdersSerializer
    lookup_field = 'name_slug'
    queryset = Order.objects.filter()

class OrderLkGet(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'name_slug'
    queryset = Order.objects.filter()

class UserOrdersAcceptedGet(generics.ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = OrdersResultsPagination

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(worker=user)
        return orders

class UserOrdersApplyedGet(generics.ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = OrdersResultsPagination

    def get_queryset(self):
        user = self.request.user
        all_tech = TechniqueUnit.objects.filter(owner=user)
        orders = Order.objects.filter(apply_units__in=all_tech)
        return orders

class UserOrdersGet(generics.ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = OrdersResultsPagination
    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(owner=user).order_by('-worker')
        return orders

class OrdersGet(generics.ListAPIView):
    """Заявки по типу техники"""
    serializer_class = OrdersSerializer
    pagination_class = OrdersResultsPagination
    def get_queryset(self):
        type_slug = self.request.query_params.get('type_slug')
        city = self.request.query_params.get('city')
        if type_slug == 'all':
            orders = Order.objects.filter(is_moderated=True,
                                          is_active=True,
                                          is_finished=False,
                                          worker__isnull=True)
        else:
            orders = Order.objects.filter(type__name_slug=type_slug,
                                          is_moderated=True,
                                          is_finished=False,
                                          is_active=True,
                                          worker__isnull=True)
        if city != '0':
            orders = orders.filter(city_id=city)
        return orders



class OrderApplyAccept(APIView):
    def post(self, request):
        request_data = request.data
        order = Order.objects.get(id=request_data['order_id'])
        user = User.objects.get(id=request_data['worker_id'])
        order.worker = user
        unit = TechniqueUnit.objects.get(id=request_data['worker_unit_id'])
        order.worker_unit = unit
        unit.in_rent = True
        order.apply_units.clear()
        unit.save()
        order.save()
        createNotification('order',user,f'Вас выбрали исполнителем заявки №{order.id}',f'/lk/apply/{order.name_slug}')
        return Response(status=201)


class OrderApplyDecline(APIView):
    def post(self, request):
        request_data = request.data
        order = Order.objects.get(id=request_data['order_id'])
        user = User.objects.get(id=request_data['worker_id'])
        order.apply_units.remove(request_data['apply_unit_id'])
        createNotification('order', user, f'Вас не выбрали исполнителем заявки №{order.id}', f'/orders/{order.name_slug}')
        return Response(status=200)


class OrderApply(APIView):
    def post(self, request):
        request_data = request.data
        order = Order.objects.get(id=request_data['order_id'])
        order.apply_units.add(request_data['unit_id'])
        createNotification('order', order.owner, f'На заявку №{order.id} поступило предложение техники',
                           f'/lk/orders/{order.name_slug}')

        return  Response(status=201)

class OrderClose(APIView):
    def post(self, request):
        request_data = request.data
        order = Order.objects.get(id=request_data['order_id'])
        order.is_finished = True
        order.save()
        createNotification('order', order.worker, f'Заказчик завершил выполнение заявки №{order.id}.'
                                                  f' Вы можете оставить отзыв',
                           f'/lk/apply/{order.name_slug}')

        return Response(status=200)

class OrderDelete(APIView):
    def post(self, request):
        request_data = request.data
        order = Order.objects.get(id=request_data['order_id'])
        order.delete()
        return Response(status=200)


class OrderAdd(APIView):
    def post(self, request):

        rent_data = json.loads(request.data['rent_data'])
        order = json.loads(request.data['order'])
        filters = json.loads(request.data['filters'])
        print(order)
        type = TechniqueType.objects.get(name_slug=order['selectedType'])
        try:
            if rent_data['dates'] != '':
                new_order = Order.objects.create(type=type,
                                                 city_id=order['city_id'],
                                                 coords=order['coords'],
                                                 owner=request.user,
                                                 name=order['name'],
                                                 rent_type=order['rent_type'],
                                                 rentStartDate=rent_data['dates'][0],
                                                 rentEndDate=rent_data['dates'][1],
                                                 comment=order['description']
                                                 )
            else:
                new_order = Order.objects.create(type=type,
                                                 city_id=order['city_id'],
                                                 coords=order['coords'],
                                                 owner=request.user,
                                                 name=order['name'],
                                                 rent_type=order['rent_type'],
                                                 rentDate=rent_data['date'],
                                                 rentStartTime=rent_data['time'][0],
                                                 rentEndTime=rent_data['time'][1],
                                                 comment=order['description']
                                                 )
            for filter in filters:
                if filter['value'] != '':
                    for v in filter['values']:
                        if v['value'] == filter['value']:
                            new_order.filter_value.add(v['id'])
                    new_order.filter.add(filter['id'])
            allUsers=User.objects.all()
            for user in allUsers:
                print(user.subscribe_type.all())
                if type in user.subscribe_type.all():
                    createNotification('order', user, f'Добавлена новая заявка в раздел {type.name_lower}',
                                       f'/orders/{new_order.name_slug}')
            return Response(status=201)
        except:
            return Response(status=400)