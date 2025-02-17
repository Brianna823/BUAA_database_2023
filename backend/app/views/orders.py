from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreateOrder(APIView):
    def post(self, req: Request):
        data = req.data
        buyer_name = data['username']
        commodity_id = data['commodity_id']
        value = 1
        id = -1
        try:
            # 在order表中增添记录
            post_id = Commodity.objects.get(id=commodity_id).post.id  # 查询商品所属的帖子
            saler = Post.objects.get(id=post_id).user  # 查询帖子所属的用户
            buyer = User.objects.get(username=buyer_name)
            order = Order.objects.create(
                saler=saler,
                buyer=buyer,
            )
            # 在commodity表中将commodity和order关联起来
            c0 = Commodity.objects.get(id=commodity_id)
            c0.order = order
            c0.save()  # 保存
            value = 0
            id = order.id
        except Exception as e:
            print(e)
        return Response({
            'value': value,
            'order_id': id,
        })


class CancelOrder(APIView):
    def post(self, req: Request):
        data = req.data
        order_id = data['order_id']
        value = -1
        try:

            Order.objects.get(id=order_id).delete()  # 删除order元组
            # 其实好像 on_delete=models.SET_NULL 自动就会设置了
            # c0 = Commodity.objects.get(order=order)  # 修改commodity元组
            # todo 检查一下会不会
            # c0.order = None
            # c0.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value})


class GetOrder(APIView):
    def post(self, req: Request):
        data = req.data
        order_id = data['order_id']
        value = 0
        saler_name = ''
        buyer_name = ''
        commodity_id = -1
        try:
            order = Order.objects.get(id=order_id)
            saler = order.saler
            saler_name = saler.username
            buyer_name = order.buyer.username
            commodity = Commodity.objects.get(order=order)
            commodity_id = commodity.id
        except Exception as e:
            value = 1
            print(e)
        return Response({
            'value': value,
            'time': order.time.isoformat(),
            'saler_name': saler_name,
            'buyer_name': buyer_name,
            'commodity_id': commodity_id,
        })



