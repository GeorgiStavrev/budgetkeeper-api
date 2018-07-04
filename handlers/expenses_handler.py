from aiohttp import web
import json
#from serialization import ExpenseSchema

async def get_monthly(request):
    results = request.app.db.expenses_repository.get_all()
    json_data =[r.to_json() for r in results]
    return web.json_response(data=json_data, status=200)

async def get_today(request):
    data = {
        'expenses': [{
            'name': 'Spotify subscription',
            'total': '16',
            'currencyCode': 'BGN'
        }],
        'total': 16,
        'count': 1
    }
    return web.json_response(data=data, status=200)

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