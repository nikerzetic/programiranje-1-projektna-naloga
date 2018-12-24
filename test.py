import requests

url = 'https://www.goodreads.com/user/sign_in'
payload = {'user[email]': 'jotopijo1@gmail.com', 'user[password]': 'geslo123'}

with requests.Session() as s:
    p = s.post(url, data=payload)

    r1 = s.get('https://www.goodreads.com/shelf/show/fantasy', headers={'Authorization': 'access_token myToken'})

    r = s.get('https://www.goodreads.com/shelf/show/fantasy?page=25', headers={'Authorization': 'access_token myToken'})
    with open('test.html', 'w', encoding='utf-8') as dat:
        dat.write(r.text)
