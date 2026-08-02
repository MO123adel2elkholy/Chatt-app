from django.shortcuts import render
from rest_framework import viewsets, exceptions
from .models import (Category, Server)
from rest_framework.response import Response
from .serializer import (CategorySeralizer, ServerSeralizer, ChnnelSeralizer)
from django.db.models import Count
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def server_list_schema(**kwargs):
    return swagger_auto_schema(**kwargs)

SERVER_LIST_QUERY_PARAMETERS = [
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
]

SERVER_LIST_RESPONSES = {
    200: openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
            },
        ),
    ),
    401: "Authentication required",
    400: "Invalid request",
}
