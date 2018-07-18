from aiohttp import web
import json
from datetime import datetime, timedelta
from calendar import monthrange
from dateutil import tz
from handlers.constants import DEFAULT_LIMIT, DEFAULT_OFFSET

async def get(request):
    id = int(request.match_info.get('id'))
    result = request.app.db.budgets_repository.get_by_id(id)
    
    if result:
        return web.json_response(data=result.to_json(), status=200)
    else:
        return web.Response(text='Not Found', status=404)

async def post(request):
    try:
        data = await request.json()
        request.app.db.budgets_repository.add(data)
        response_obj = { 'status': 'success' }
        return web.Response(text=json.dumps(response_obj), status=201)
    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)

async def put(request):
    try:
        data = await request.json()
        id = int(request.match_info.get('id'))
        result = request.app.db.budgets_repository.update(data, id)

        if result:
            response_obj = { 'status': 'success' }
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            return web.Response(text='Not Found', status=404)

    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)

async def delete(request):
    try:
        data = await request.json()
        id = int(request.match_info.get('id'))
        result = request.app.db.budgets_repository.delete(id)

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
