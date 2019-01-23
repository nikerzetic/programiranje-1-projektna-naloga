from splinter import Browser

browser = Browser('firefox')

browser.visit('https://www.goodreads.com/user/sign_in')

browser.find_by_id('user_email').fill('jotopijo1@gmail.com')
browser.find_by_id('user_password').fill('geslo123')
browser.find_by_value('Sign in').first.click()

browser.visit('https://www.goodreads.com/shelf/show/fantasy?page=24')
with open('test.html', 'w', encoding='utf-8') as dat:
    dat.write(browser.html)

browser.quit()