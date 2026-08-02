from django.shortcuts import render
from rest_framework import viewsets, exceptions
from .models import (Category, Server)
from rest_framework.response import Response
from .serializer import (CategorySeralizer, ServerSeralizer, ChnnelSeralizer)
from django.db.models import Count
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


#  DOC  STRING


class ServerListView(viewsets.ViewSet):
    """
    Retrieve a list of servers.

    Query Parameters:
        - category (str): Filter servers by category name.
        - by_user (bool): If true, return servers joined by the authenticated user.
        - qty (int): Limit the number of returned servers.
        - server_id (int): Return the server matching the given ID.
        - subcriper (bool): If true, include the number of members for each server.

    Authentication:
        - `by_user=true` or `server_id` requires authentication.

    Responses:
        - 200: Successful response with server data.
        - 401: Authentication failed.
        - 400: Invalid server ID or no matching server found.
    """
    queryset = Server.objects.all()

    @swagger_auto_schema(
        operation_summary="List servers",
        operation_description="Return servers filtered by category, user membership, ID, or quantity.",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter servers by category name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'by_user',
                openapi.IN_QUERY,
                description="Return only servers joined by the authenticated user",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'qty',
                openapi.IN_QUERY,
                description="Limit the number of results returned",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'server_id',
                openapi.IN_QUERY,
                description="Get a specific server by ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'subcriper',
                openapi.IN_QUERY,
                description="Include the number of members for each server",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={
            200: "Successful response",
            401: "Authentication required",
            400: "Invalid request"
        }
    )
    def list(self, request):
        category = request.GET.get('category')
        by_user = request.GET.get('by_user') == 'true'
        quaintity = request.GET.get('qty')
        server_id = request.GET.get('server_id')
        with_num_members = request.GET.get('subcriper')== 'true'

        print('category', category)
        #  retriving server based on server id given
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
                if not self.queryset.exists():
                    raise exceptions.ValidationError(
                        detail=f' server with this  id  {server_id} Dosnot exist '
                    )
            except ValueError:
                raise exceptions.ValidationError(
                    detail=f' server with this  id  {server_id} Dosnot exist '
                )
        if with_num_members:
            self.queryset = self.queryset.annotate(subscriper=Count("members"))
            print(self.queryset)
        print('subcriper ==> ', self.queryset[0])
        serializer = ServerSeralizer(self.queryset, many=True, context={
            'subscriper': with_num_members
        })
        return Response(
            {'success': True,
             'data': serializer.data}
        )
