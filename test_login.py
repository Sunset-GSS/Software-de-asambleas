import urllib.request, urllib.parse, urllib.error, http.cookiejar, re

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

resp = opener.open('http://127.0.0.1:5001/auth/login')
html = resp.read().decode('utf-8')

match = re.search(r'name="csrf_token" value="([^"]+)"', html)
if not match:
    print('ERROR: no se encontro csrf_token en el HTML')
    exit(1)

token = match.group(1)
print('CSRF Token obtenido:', token[:20] + '...')

data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin', 'csrf_token': token}).encode()
req = urllib.request.Request('http://127.0.0.1:5001/auth/login', data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    resp2 = opener.open(req)
    final_url = resp2.geturl()
    body = resp2.read().decode('utf-8')
    print('Redirigido a:', final_url)
    if 'dashboard' in final_url or 'dashboard' in body.lower():
        print('LOGIN EXITOSO - llego al dashboard')
    elif 'incorrectos' in body.lower():
        print('LOGIN FALLIDO - credenciales incorrectas')
    else:
        print('Respuesta parcial:', body[:300])
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code, e.reason)
