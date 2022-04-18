import requests
import bs4
import re
import os
import sqlite3
import time
import random
from datetime import datetime

cdt = datetime.now()

def main(**kwargs):
    print("initiating job scrape process..")
    c = 0
    p = kwargs.get('pages')
    uri = kwargs.get('uri')
    label = kwargs.get('label')
    table = kwargs.get('table')
    vpn = kwargs.get('vpn')

    nlist = []
    for i in range(p):
        res = requests.get(
            f'{uri}&start={c}')
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % exc)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        elems = str(soup.select('body > script:nth-child(3)'))
        jobkey = re.compile(r"jobKeysWithInfo\['(.*?)']")
        keys = jobkey.findall(elems)
        nlist.extend(keys)
        print(keys)
        c += 50

    print(c)
    print(len(nlist))
    print("scrape complete..")

    jkey = conn.execute(f"SELECT JKEY, Url from '{table}'")
    klist = []

    print("building delta list..")
    for k in jkey:
        klist.append(k[0])
    print('--', len(klist), '--')

    dist = [i for n, i in enumerate(nlist) if i not in nlist[:n]]
    print('adding delta list to db..')
    cnt = 0
    for d in dist:
        if d not in klist:
            conn.execute(                                                                   #  ↓ replace www with uk if needed ex: uk.indeed.com
                f"INSERT INTO '{table}' (JKEY, Url, Category, Created) VALUES ('{d}','https://www.indeed.com/viewjob?jk={d}','{label}', '{cdt}')")
            conn.commit()
            cnt += 1

    print(cnt)
    print("executing full job post scraping process..")
    jkey = conn.execute(f"SELECT JKEY, Url,Title from '{table}'")
    limit = 0
    nflist = 0
    maxlist = [*range(1, 5000, random.randint(150, 280))]
    for i, u, t in jkey:
        if t is not None:
            continue
        if limit in maxlist:
            os.chdir(f'{vpn}')
            cmd = "nordvpn -c"
            os.system(cmd)
            time.sleep(10)
        res = requests.get(f'{u}')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        try:
            title = soup.find('h1', 'jobsearch-JobInfoHeader-title').text.strip().replace(
                "\n", " ").replace("'", "").replace("'", "").replace("’", "")
            conn.execute(fr"UPDATE '{table}' set Title = '{title}' where JKEY = '{i}'")
        except AttributeError:
            nflist += 1

        try:
            salary = soup.find(
                'span', 'icl-u-xs-mr--xs attribute_snippet').text.strip()
            conn.execute(
                fr"UPDATE '{table}' set Salary = '{salary}' where JKEY = '{i}'")
        except AttributeError:
            nflist += 1

        try:
            jobdet = soup.find_all('div', 'jobsearch-jobDescriptionText')
            jdet = [j.text.strip().replace("\n", " ").replace(
                "'", "").replace("'", "").replace("’", "") for j in jobdet][0]
            conn.execute(fr"UPDATE '{table}' set Body = '{jdet}' where JKEY = '{i}'")
        except AttributeError:
            nflist += 1
        except IndexError:
            jobdet = soup.find_all('div', 'jobsearch-jobDescriptionText')
            jdet = [j.text.strip().replace("\n", " ").replace(
                "'", "").replace("'", "").replace("’", "") for j in jobdet]
            conn.execute(fr"UPDATE '{table}' set Body = '{jdet}' where JKEY = '{i}'")
            nflist += 1
        conn.commit()
        print("#", limit, ": successfully collected -- ", i)
        limit += 1

    print(limit)
    print("job scraping completed.")
    conn.close()
    os.chdir(f'{vpn}')
    cmd = "nordvpn -c"
    os.system(cmd)
    time.sleep(10)
