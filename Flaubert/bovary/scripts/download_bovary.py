import requests
import time
import socks
import socket

socks.setdefaultproxy(
    proxy_type=socks.PROXY_TYPE_SOCKS5,
    addr="127.0.0.1",
    port=9050)
socket.socket = socks.socksocket

for i in range(4989, 5029):
    folio = str(i)
    url = 'http://www.bovary.fr/folio_visu_trans.php?folio={}'.format(folio)
    print(url)
    html = requests.get(url).text
    with open('folios/{}.html'.format(folio), 'w') as f:
        f.write(html)
    time.sleep(2)
