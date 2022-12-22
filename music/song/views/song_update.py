from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def song_update():
    try:
        a = 1/0
    except ZeroDivisionError as error:
        return Response({"error": error.__str__()}, status=HTTP_400_BAD_REQUEST)

    return Response(status=HTTP_200_OK)
