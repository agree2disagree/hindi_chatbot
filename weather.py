
# tense = { 'past': [ 'WA', 'WI', 'We', 'WIM' ], 
#           'present': [ 'hE', 'hEM' ], 
#           'future': [ 'hogA', 'hogI', 'hoMge', 
#                       'padZegA', 'padZegI','padZeMge', 
#                       'calegA', 'calegI', 'caleMge',
#                       'rahegA', 'rahegI', 'raheMge' ] }

days = { 'zero': [ 'Aja' ], # for current day
         'one': [ 'kala', 'eka', '1' ],
         'two': [ 'parasoM', 'xo', '2' ],
         'three': [ 'wIna', '3' ],
         'four': [ 'cAra', '4' ],
         'five': [ 'pAzca', '5' ],
         'six': [ 'Caha', '6' ],
         'seven': [ 'sapwAha', 'haPZwA', 'haPZwe' ] } # for whole week

# question = { 'what': [ 'kya' ], 
#              'how': [ 'kEsA', 'kEsI' ],
#              'amt': [ 'kiwanA', 'kiwanI' ] }

describe = { 'feat': [ 'havA', 'XUpa', 'namI' ],
             'prcp': [ 'bAriSa', 'varRA', 'barPZa', 'himapAwa', 'ole' ],
             'wthr': [ 'mOsama' ],
             'temp': [ 'wApamAna', 'garamI', 'garama', 'sarxI', 
                       'TaMDI', 'TaMDA', 'TaMDa', 'TaMdI', 'TaMdA', 'TaMda' ] }

prompts = [ 'Ora kuCa?', 'koI Ora savAla?', 'koI Or praSna?' ]

negatives = [ 'nahIM', 'nA', 'na' ]

sign_offs = [ 'isa sevA kA upayoga karane ke lie XanyavAxa', 
              'hameM ApakI sahAyawA karane meM KuSI huI' ]

invalids = [ 'hamAre pAsa yaha jAnakArI nahIM hE, kqipayA koI Ora savAla pUcie', 
             'hameM ApakA savAla samaJa nahIM AyA, kyA Apa kuCa Or jAnanA cAheMge?' ]

loc_codes = { 'itanagar': 42308,
            #  'amravati': ,
             'dispur': 42410,
             'patna': 42492,
             'raipur': 42874,
             'panaji': 43192, 'panjim': 43192,
             'imphal': 42623,
             'gandhinagar': 42647,
             'chandigarh': 10,
             'shimla': 42083,
             'srinagar': 42027,
             'jammu': 42056,
             'ranchi': 42701,
             'shillong': 42516,
             'bengaluru': 43295, 'bangalore': 43295,
             'trivandrum': 43371, 'thiruvananthapuram': 43371,
             'mumbai': 43003, 'bombay': 43003,
             'aizwal': 42726, 
             'kohima': 42527,
             'bhubaneshwar': 42971,
             'jaipur': 42348,
             'gangtok': 42299,
             'chennai': 43279, 'madras': 43279,
             'bhopal': 42667, 
             'hyderabad': 43128,
             'agartala': 42724,
             'lucknow': 42369,
             'dehradun': 42111,
             'kolkata': 42807, 'calcutta': 42807,
             'port blair': 43333,
            #  'silvassa': ,
            #  'daman': , 'diu': ,
             'delhi': 42182, 'new delhi': 42182,
            #  'kavaratti': 43337,
             'pondicherry': 43328, 'puducherry': 43328 }
# limiting to list of capital cities

# max_t, dep_max, min_t, dep_min, rain, hum_morn, hum_even, avg_t, avg_h
day_data = []
# max_t, min_t, avg_t, avg_h
week_data = [] # indices 0-7 (size is 8)


import random
import requests
from bs4 import BeautifulSoup


def main():
    ''' executes the chatbot '''

    global loc_codes
    global prompts

    print('Apako kOnase sWAna kI jAnakArI cAhie?')
    loc = input()
    loc = loc.lower()
    while loc not in loc_codes:
        print('hamAre pAsa isa sWAna kI jAnakArI nahIM hE. kqpayA koI Ora sWAna ke bAre mEM pUCie.')
        loc = input()
        loc = loc.lower()
    fill_data(loc_codes[loc])
    
    flag = True
    print('Apa kyA jAnanA cAheMge?')
    query = input()
    response, flag = retrieve_data(query)
    print(response)

    # random prompt for additional questions
    # if response in negatives, set flag to false
    while(flag):
        r_no = random.randint(0, 2)
        print(prompts[r_no])
        query = input()
        response, flag = retrieve_data(query)
        print(response)
    
    # end of execution
    return


def retrieve_data(qu):
    ''' function to check for keywords and fill frame to produce response '''

    global negatives
    global invalids
    global sign_offs
    global describe
    global days
    global day_data
    global week_data

    # no more questions
    if qu in negatives:
        r_no = random.randint(0, 1)
        reply = sign_offs[r_no]
        return reply, False
    
    # evaluate type of query and provide response
    words = qu.split()
    known = 0

    if any(i in words for i in days['one']):
        known = 1
    elif any(i in words for i in days['two']):
        known = 2
    elif any(i in words for i in days['three']):
        known = 3
    elif any(i in words for i in days['four']):
        known = 4
    elif any(i in words for i in days['five']):
        known = 5
    elif any(i in words for i in days['six']):
        known = 6
    elif any(i in words for i in days['seven']):
        known = 7
    else:
        pass

    if known == 0:
        # not a query on future data
        max_t = day_data[0]
        min_t = day_data[2]
        avg_t = day_data[7]
        hum_morn = day_data[5]
        
        if hum_morn < 50:
            prob = 'kama'
            amnt = 'kama'
        elif hum_morn < 70:
            prob = 'maXyama'
            amnt = 'halkI'
        else:
            prob = 'ucca'
            amnt = 'wejZa'
        
        if max_t >= 35  and avg_t >= 30:
            sun = 'kadZI'
            tmp = 'garama'
        else:
            sun = 'halkI'
            tmp = 'TaMdA'
        
        # known == 0
        for word in words:
            if word in describe['temp']:
                reply1 = 'Aja kA wApamAna ' + str(min_t) + u'\u2103' + '  se ' + str(max_t) + u'\u2103' + '  ke bIca meM rahegA'
                reply2 = '\nxina kA Osawa wApamAna ' + str(avg_t) + u'\u2103' + '  hE' + '\nmOsama ' + tmp + ' hogA'
                known = 0
                break
            elif word in describe['prcp']:
                reply1 = 'Aja subaha kI namI ' + str(hum_morn) + '% hE'
                reply2 = '\n' + amnt + ' bAriSa hogI'
                known = 0
                break
            elif word in describe['feat']:
                reply1 = 'Aja ke xina ' + sun + ' XUpa hogI' + ' Ora ' + amnt + ' havA calegI'
                reply2 = '\namI ' + hum_morn + '% hogI'
                known = 0
                break
            elif word in describe['wthr']:
                reply1 = 'Aja kA Osawa wApamAna ' + str(avg_t) + u'\u2103' + '  hE'
                reply2 = '\nvarRA hone kI ' + prob + ' saMBAvanA hE'
                known = 0
                break
            else:
                known = -1
    
    if known < 0:
        r_no = random.randint(0, 1)
        reply = invalids[r_no]
    else:
        if known > 0:
            reply1 = 'Osawa wApamAna ' + str(week_data[known][2]) + u'\u2103' + '  hogA'
            reply2 = '\nnamI ' + str(week_data[known][3]) + '% hogI'
            if week_data[known][2] > 27:
                reply2 = reply2 + '\nmOsama garama hogA'
            elif week_data[known][2] > 17:
                reply2 = reply2 + '\nmOsama suhAnA hogA'
            else:
                reply2 = reply2 + '\nmOsama TaMdA hogA'
        reply = reply1 + reply2
    
    return reply, True


def fill_data(loc):
    ''' function to retrieve data from site, fill data structure '''

    global day_data
    global week_data

    url = 'http://city.imd.gov.in/citywx/city_weather.php?id=' + str(loc)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # extract from table here
    whole = soup.find('table')
    table = whole.find('table')
    # max_t, dep_max, min_t, dep_min, rain, hum_morn, hum_even, sunset, sunrise, moonrise, moonset
    # last 4 not required -> 2, 4, 6, 8, 10, 12, 14
    values = table.find_all('font')
    # day_data = []
    for x in range(2, 15, 2):
        val = values[x].get_text()
        val = val.replace('\n', '')
        if val == 'NIL':
            val = 0
        val = float(val)
        day_data.append(val)

    avg_t = (day_data[0] + day_data[2])/2.0
    day_data.append(avg_t)
    avg_h = (day_data[5] + day_data[6])/2.0
    day_data.append(avg_h)

    week_data = gen_week_data(day_data[0], day_data[2], avg_t, avg_h)

    # preliminary data obtained
    return


def gen_week_data(max_0, min_0, avg_0, hum_0):
    ''' function to generate dummy data for the weekly forecast '''

    # first element is current day ('zero')
    dummy = [ max_0, min_0, avg_0, hum_0 ]
    dummy_list = []
    dummy_list.append(dummy)

    # for following days in the week ('one' to 'six')
    for i in range(1, 7):
        dummy = [ max_0+i, min_0+i, avg_0+i, hum_0+i ]
        dummy_list.append(dummy)
    
    # last element is the overall data for the week ('seven')
    dummy = [ max_0+6, min_0, avg_0+3, hum_0+3 ]
    dummy_list.append(dummy)

    # weekly forecast generated
    return dummy_list


if __name__ == "__main__":
    exit (main())