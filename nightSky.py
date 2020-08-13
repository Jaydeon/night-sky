import bs4, requests, sys

if len(sys.argv) == 1:
    raise Exception('You need to name a city, by typing it after "nightSky"')

city = ''
for i in range (1,len(sys.argv)):
    city = city + sys.argv[i]
if ',' in city:
    [city,state] = city.split(',')

def nightSky(cityName):
    print('Loading time and weather data.. [0%]')
    clockres = requests.get('https://www.timeanddate.com/worldclock/usa/' + cityName)
    clocksoup = bs4.BeautifulSoup(clockres.text, 'html.parser')

    print('Loading Moon and Sun data.. [25%]')
    astrores = requests.get('https://www.timeanddate.com/astronomy/usa/' + cityName)
    astrosoup = bs4.BeautifulSoup(astrores.text, 'html.parser')

    print('Loading Moon phase data.. [50%]')
    moonres = requests.get('https://www.timeanddate.com/moon/usa/' + cityName)
    moonsoup = bs4.BeautifulSoup(moonres.text, 'html.parser')

    print('Loading eclipse data.. [75%]')
    eclipseres = requests.get('https://www.timeanddate.com/eclipse/in/usa/' + cityName)
    eclipsesoup = bs4.BeautifulSoup(eclipseres.text, 'html.parser')

    print('Loading complete. [100%]\n')

    name = clocksoup.select('body > div.wrapper > div.main-content-div > header > div.bn-header__wrap.fixed > div > section.headline-banner__wrap > div > h1')
    name = name[0].text.split('in ')
    print('The selected city is ' + name[1] + '.')

    time = moonsoup.select('#smct')
    print('The time is ' + time[0].text +'.')

    weather = clocksoup.select('#wt-tp')
    climate = clocksoup.select('#wt-3d > p:nth-child(5)')
    [climate,highlow] = climate[0].text.split('.')
    print('Currently, the temperature is ' + weather[0].text + ' and the condition is ' + climate + '.\n')

    sunrise = astrosoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(2) > td')
    [sunrise,waste] = sunrise[0].text.split('m')
    sunrise = sunrise + 'm'
    sunset = astrosoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(3) > td')
    [sunset,waste] = sunset[0].text.split('m')
    sunset = sunset + 'm'
    print('Today, the sun will rise at ' + sunrise + ' and set at ' + sunset + '.')

    moonset = astrosoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(5) > td')
    [moonset,waste] = moonset[0].text.split('m')
    moonset = moonset + 'm'
    moonrise = moonsoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(7) > td')
    moonrise = moonrise[0].text
    print('Today, the moon will set at ' + moonset + '.')
    print('The moon will next rise ' + moonrise + '.\n')

    percent = moonsoup.select('#cur-moon-percent')
    print('Currently, the moon is ' + percent[0].text + ' covered.')
    
    phase = moonsoup.select('#qlook > a')
    print('Tonight, the moon\'s phase is ' + phase[0].text + '.')

    new = moonsoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(5) > td')
    new = new[0].text
    full = moonsoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(6) > td')
    full = full[0].text
    print('The next new moon is ' + new + ' and the next full moon is ' + full + '.\n')

    globalevent = eclipsesoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(1) > td > a')
    globalevent = globalevent[0].text
    localtype = eclipsesoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(2) > td')
    localtype = localtype[0].text
    print('The next global eclipse is a ' + globalevent + ', and it will be a ' + localtype + '.')
    
    maximum = eclipsesoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(4) > td')
    [maximum, waste] = maximum[0].text.split('m')
    maximum = maximum + 'm'
    duration = eclipsesoup.select('body > div.wrapper > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(6) > td')
    duration = duration[0].text
    print('This eclipse\'s maximum is at ' + maximum + ' and it will last for ' + duration + '.\n') 

nightSky(city)


