from aiohttp import web
import json
from datetime import datetime, timedelta
from calendar import monthrange
from dateutil import tz
from handlers.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from auth.decorators import authorized, authenticated

@authorized(['test'])
async def get_monthly(request):
    limit, offset = _get_special_params(request)

    today = datetime.utcnow().date()
    _, days_in_month = monthrange(today.year, today.month)
    start = datetime(today.year, today.month, 1, tzinfo=tz.tzutc())
    end = datetime(today.year, today.month, days_in_month, tzinfo=tz.tzutc()) + timedelta(1)

    results = request.app.db.expenses_repository.get_by_period(start, end, limit, offset)
    json_data =[r.to_json() for r in results]
    return web.json_response(data=json_data, status=200)

@authenticated
async def get_today(request):
    limit, offset = _get_special_params(request)

    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
    end = start + timedelta(1)

    results = request.app.db.expenses_repository.get_by_period(start, end, limit, offset)
    json_data =[r.to_json() for r in results]
    return web.json_response(data=json_data, status=200)

@authenticated
async def get(request):
    id = int(request.match_info.get('id'))
    result = request.app.db.expenses_repository.get_by_id(id)
    
    if result:
        return web.json_response(data=result.to_json(), status=200)
    else:
        return web.Response(text='Not Found', status=404)

@authenticated
async def post(request):
    try:
        data = await request.json()
        request.app.db.expenses_repository.add(data)
        response_obj = { 'status': 'success' }
        return web.Response(text=json.dumps(response_obj), status=201)
    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)

@authenticated
async def put(request):
    try:
        data = await request.json()
        id = int(request.match_info.get('id'))
        result = request.app.db.expenses_repository.update(data, id)

        if result:
            response_obj = { 'status': 'success' }
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            return web.Response(text='Not Found', status=404)

    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)

@authenticated
async def delete(request):
    try:
        data = await request.json()
        id = int(request.match_info.get('id'))
        result = request.app.db.expenses_repository.delete(id)

        if result:
            response_obj = { 'status': 'success' }
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            return web.Response(text='Not Found', status=404)

    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)

def _get_special_params(request):
    limit = int(request.query.get('limit')) if request.query.get('limit') else DEFAULT_LIMIT
    offset = int(request.query.get('offset')) if request.query.get('offset') else DEFAULT_OFFSET

    if limit <= 0:
        limit = DEFAULT_LIMIT

    return limit, offset