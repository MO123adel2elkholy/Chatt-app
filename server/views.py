from django.shortcuts import render
from rest_framework import viewsets, exceptions
from .models import (Category, Server)
from rest_framework.response import Response
from .serializer import (CategorySeralizer, ServerSeralizer, ChnnelSeralizer)
from django.db.models import Count
# Create your views here.


#  DOC  STRING
""" 
this Class is end end point for 
filtring servers by category 


Keyword arguments: category
argument -- specific category 
Return: list of server associated with specfic category 
"""


class ServerListView(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.GET.get('category')
        by_user = request.GET.get('by_user') == 'true'
        quaintity = request.GET.get('qty')
        server_id = request.GET.get('server_id')
        with_num_members = request.GET.get('subcriper')

        print('category', category)
        if by_user or server_id and not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed()
        if category:
            # self.queryset = self.queryset.filter(category=category)
            self.queryset = self.queryset.filter(category__name=category)
            print('Servers ', self.queryset)
        if by_user:
            user_id = request.user.id
            print(user_id, ' <= id ')
            self.queryset = self.queryset.filter(members=user_id)
        if quaintity:
            self.queryset = self.queryset[:int(quaintity)]
        if server_id:
            print('server Id  ', server_id)
            try:
                self.queryset = self.queryset.filter(id=server_id)
                print('Your Servers ===>', self.queryset)
                if not self.queryset.exists():
                    raise exceptions.ValidationError(
                        detail=f' server with this  id  {server_id} Dosnot exist '
                    )
            except ValueError:
                raise exceptions.ValidationError(
                    detail=f' server with this  id  {server_id} Dosnot exist ')
            if with_num_members:
                self.queryset = self.queryset.annotate(
                    subscriper=Count("members")
                )
                print(self.queryset)
        print('subcriper ==> ', self.queryset[0])
        serializer = ServerSeralizer(self.queryset, many=True, context={
            'subscriper': with_num_members
        })
        return Response(
            {'success': True,
             'data': serializer.data}
        )
