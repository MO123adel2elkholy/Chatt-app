from django.shortcuts import render
from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from django.db.models import Count

from .models import Server
from .serializer import ServerSeralizer
from .schema import (
    server_list_schema,
    SERVER_LIST_QUERY_PARAMETERS,
    SERVER_LIST_RESPONSES,
)


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

    @server_list_schema(
        operation_summary="List servers",
        operation_description="Return servers filtered by category, user membership, ID, or quantity.",
        manual_parameters=SERVER_LIST_QUERY_PARAMETERS,
        responses=SERVER_LIST_RESPONSES,
    )
    def list(self, request):
        category = request.GET.get('category')
        by_user = request.GET.get('by_user') == 'true'
        quaintity = request.GET.get('qty')
        server_id = request.GET.get('server_id')
        with_num_members = request.GET.get('subcriper') == 'true'

        queryset = self.queryset

        if (by_user or server_id) and not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed()

        if category:
            queryset = queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            queryset = queryset.filter(members=user_id)

        if quaintity:
            queryset = queryset[:int(quaintity)]

        if server_id:
            try:
                queryset = queryset.filter(id=server_id)
                if not queryset.exists():
                    raise exceptions.ValidationError(
                        detail=f' server with this  id  {server_id} Dosnot exist '
                    )
            except ValueError:
                raise exceptions.ValidationError(
                    detail=f' server with this  id  {server_id} Dosnot exist '
                )

        if with_num_members:
            queryset = queryset.annotate(subscriper=Count("members"))

        serializer = ServerSeralizer(queryset, many=True, context={
            'subscriper': with_num_members
        })

        return Response({
            'success': True,
            'data': serializer.data
        })
