"""
views.py
    Written by: Andrew McDonald
    Initial: 03.08.21
    Updated: 02.09.21
    version: 1.5

Logic:
    Handles API http requests

Calls on:
    serializers.py
    models.py
    
Referenced by:
    urls.py
"""

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from django.http import HttpResponse
from django.conf import settings

from .serializers import *
from .models import Extracted, Report
from api.scripts import table_extract
from api.scripts.logging import Logging

from pathlib import Path, PurePath
import datetime as date

# processing time
from timeit import default_timer as timer
from humanfriendly import format_timespan

from rest_framework.renderers import JSONRenderer


class ReportViewSet(viewsets.ModelViewSet):
    """
    serializer based viewset for Report model [WORKING]

    Upload and Extract a report:    POST    api/upload/
    List all reports:               GET     api/reports/
    Retrieve report by id:          GET     api/reports/{id}/
    Retrieve report by name:        GET     api/reports/?name=
    Update existing report:         PUT     api/reports/{id}/
    Update part of report:          PATCH   api/reports/{id}/
    Remove report by id:            DELETE  api/reports/{id}/
    Remove report by name:          DELETE  api/reports/?name=
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]  # test set attributes to filter by


class ExtractedViewSet(viewsets.ModelViewSet):
    """
    serializer based viewset for Extracted model [WORKING]

    List all extractions:           GET     api/extracted/
    Retrieve extraction by id:      GET     api/extracted/{id}/
    Update existing extraction:     PUT     api/extracted/{id}/
    Update part of extraction:      PATCH   api/extracted/{id}/
    Remove extraction by id:        DELETE  api/extracted/{id}/
    Remove extraction by name:      DELETE  api/extracted/?name=
    """

    queryset = Extracted.objects.all()
    serializer_class = ExtractedSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "f_type"]  # test set attributes to filter by


class UploadView(APIView):
    """
    url based upload view with extraction function [WORKING]
    Add a new report and extract: POST api/upload/
    """

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        report_serializer = ReportSerializer(
            data=request.data, context={"request": request}
        )

        # check for valid request
        if not report_serializer.is_valid():
            return Response(report_serializer, status=status.HTTP_400_BAD_REQUEST)

        # create log object
        log = Logging()

        # create Report database model instance
        report_serializer.save()

        # uploaded file url location
        file_url = report_serializer.data["document"]

        # get pages info
        start_page = report_serializer.data["start_page"]
        end_page = report_serializer.data["end_page"]

        # django upload root dir
        media_root_dir = settings.MEDIA_ROOT

        # build file path name and path location
        full_path = Path(file_url)
        base_dir = full_path.parts[3]
        file_name = full_path.name
        file_path = PurePath(media_root_dir, base_dir, file_name)

        # get newly created Report db instance and update name and file_type fields
        r = Report.objects.get(document__endswith=file_name)
        r.name = base_dir
        r.f_type = file_name.split(".")[1]
        r.save()

        # clean media root of any empty folders
        log.output("INFO", "cleaning /documents of empty directories")

        walk = list(os.walk(media_root_dir))
        for path, _, _ in walk[::-1]:
            if len(os.listdir(path)) == 0:
                Path.rmdir(Path(path))

        # log output
        log.output("INFO", "/documents cleaned")
        log.output("INFO", "sending file for extraction...")

        # start stopwatch
        start = timer()

        try:
            # run extraction script, set output_type: ['json','csv','xlsx', 'all']
            # 'all' currently only set to json, csv
            # returns dictionary
            extracted = table_extract.extract(file_path, start_page, end_page)

        except Exception as e:
            error_output = "".join(["Extraction script: ", str(e)])
            log.output("ERROR", error_output)
            return HttpResponse(error_output, status=500)  # 500 Internal Server Error

        # end stopwatch and log time
        end = timer()
        log.output("INFO", f'extraction completed in" {format_timespan(end - start)}')

        return Response(extracted, status=status.HTTP_201_CREATED)
