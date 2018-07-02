import requests
from django.apps import apps
from django.db.models import CharField, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from wagtailmodelchoosers.paginators import GenericModelPaginator
from wagtailmodelchoosers.utils import (
    get_chooser_options,
    get_query_keys_map,
    get_response_keys_map,
)


class ModelView(ListModelMixin, GenericViewSet):
    pagination_class = GenericModelPaginator
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)

    def get_params(self):
        return self.request.parser_context.get('kwargs')

    def do_search(self, cls, queryset):
        search = self.request.query_params.get('search', None)
        if not search:
            return queryset

        queries = []
        for field in cls._meta.get_fields():
            if isinstance(field, CharField):
                kwargs = {}
                param_name = '%s__icontains' % field.name
                kwargs[param_name] = search
                queries.append(Q(**kwargs))

        if len(queries):
            query = queries.pop()

            for item in queries:
                query |= item

            return queryset.filter(query)
        else:
            return queryset

    def do_filter(self, cls, queryset):
        for field in getattr(cls, 'rest_framework_filter_fields', []):
            value = self.request.query_params.get(field, None)
            if value is not None:
                kwargs = {}
                param_name = '%s' % field
                kwargs[param_name] = value
                queryset = queryset.filter(**kwargs)

        return queryset

    def get_queryset(self):
        params = self.get_params()
        app_name = params.get('app_name')
        model_name = params.get('model_name')
        cls = apps.get_model(app_name, model_name)

        queryset = cls.objects.all()
        queryset = self.do_search(cls, queryset)
        queryset = self.do_filter(cls, queryset)

        return queryset

    def get_serializer_class(self):
        params = self.get_params()
        app_name = params.get('app_name')
        model_name = params.get('model_name')

        cls = apps.get_model(app_name, model_name)
        return self.build_serializer(cls, model_name)

    def build_serializer(self, cls, model_name):
        """
        Dynamically build a model serializer class
        """
        class_name = "%sSerializer" % model_name
        meta_class = type('Meta', (), {'model': cls, 'fields': '__all__'})
        serializer_args = {'Meta': meta_class}

        if hasattr(cls, 'content_type'):
            serializer_args.update({
                'content_type': serializers.StringRelatedField()
            })

        model_serializer = type(class_name, (serializers.ModelSerializer,), serializer_args)

        return model_serializer


class RemoteResourceView(ViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    http_method_names = ('get', 'head', 'options')

    def get_params(self):
        return self.request.parser_context.get('kwargs')

    def get_remote_url(self, chooser_options):
        url = chooser_options['remote_endpoint']
        url_params = {}

        # Apply options.
        query_keys_map = get_query_keys_map(chooser_options)
        for chooser_key, remote_key in query_keys_map.items():
            value = self.request.query_params.get(chooser_key)
            if value is not None:
                url_params[remote_key] = value

        # Apply filters.
        query_filters = chooser_options.get('filters', [])
        for filter_ in query_filters:
            # Use the value from the url params, not from the options in case the front-end modified it.
            value = self.request.query_params.get(filter_['field'])
            if value is not None:
                url_params[filter_['field']] = value

        return url, url_params

    def convert_response(self, response, chooser_options):
        response_data = response.json()
        response_keys_map = get_response_keys_map(chooser_options)

        # Always include the `results` and `page` keys.
        requested_page = self.request.query_params.get('page', 1)
        data = {
            'results': response_data.get(response_keys_map['results']),
            'page': int(response_data.get(response_keys_map['page'], requested_page))
        }

        # Only include the other keys if they exists.
        for chooser_key, remote_key in response_keys_map.items():
            # Do not overwrite already present keys.
            if chooser_key in data:
                continue

            value = response_data.get(remote_key)
            if value is not None:
                data[chooser_key] = value

        return data

    def list(self, request, *args, **kwargs):
        params = self.get_params()
        chooser = params.get('chooser')
        chooser_options = get_chooser_options(chooser)

        url, url_params = self.get_remote_url(chooser_options)
        response = requests.get(url, url_params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            return Response({
                'status_code': e.response.status_code,
                'detail': str(e)
            })

        data = self.convert_response(response, chooser_options)
        return Response(data)
