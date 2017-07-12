from .dateutils import formatStrToDate


def getDateRange(request):
    data = request.data
    data.get('startDate')
    startDate = formatStrToDate(data.get('startDate'))
    endDate = formatStrToDate(data.get('endDate'))
    return startDate,endDate