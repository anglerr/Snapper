
class BadRequestException(Exception):
    def __init__(self, msg=None, status=None):
        self.msg = msg
        self.status = status


def verify_request(request, RequestFormat, many=False):
    data = RequestFormat(data=request.data, many=many)
    if not data.is_valid():
        raise BadRequestException(msg=data.errors, status=400)
    return data.validated_data
