from aiohttp import web

async def get_monthly(request):
    data = {
        'expenses': [{
            'name': 'Spotify subscription',
            'total': '16',
            'currencyCode': 'BGN'
        },{
            'name': 'Groceries',
            'total': '35',
            'currencyCode': 'BGN'
        }],
        'total': 41,
        'count': 2
    }
    return web.json_response(data=data, status=200)

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