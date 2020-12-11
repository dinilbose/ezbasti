"""
EZBASTI -- A python package that allows you to download BASTI isochrones directly from the BASTI
directly website

based on EZPADOVA and EZBASTI

:version: 0.1
:author: Dinil Bose
"""


from __future__ import print_function, unicode_literals, division

import sys
import os
import inspect
import time
from io import StringIO, BytesIO
import zlib
import re
import json



if sys.version_info[0] > 2:
    py3k = True
    from urllib.parse import urlencode
    from urllib import request
    from urllib.request import urlopen
else:
    py3k = False
    from urllib import urlencode
    from urllib2 import urlopen


from io import BytesIO
import urllib.request
import tarfile
from astropy.table import Table



list_model=[['model=01,Solar-Scaled[alpha/Fe]=0.0,Overshooting:No,Diffusion:No,Mass loss:n=0.0,He=0.247','P00','P00O0D0E0Y247',],
['model=02,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.0,He=0.247','P00','P00O1D0E0Y247',],
['model=03,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.3,He=0.247','P00','P00O1D0E1Y247',],
['model=04,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247','P00','P00O1D1E1Y247',],
['model=11,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247','P04','P04O1D1E1Y247',],
['model=12,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.275','P04','P04O1D1E1Y275',],
['model=13,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.300','P04','P04O1D1E1Y300',],
['model=14,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.320','P04','P04O1D1E1Y320']]


def get_one_isochrone(model='01',FeH=0.0,age=16e6,photometry='HR'):
    '''
    Get Basti Iscohrone from the website:

    model:str Get model number using print_model
    FeH:float Mettallicity
    Age:float in years
    photometry:str Get photometric system using print_photometric_system()

    model:

    model=01,Solar-Scaled[alpha/Fe]=0.0,Overshooting:No,Diffusion:No,Mass loss:n=0.0,He=0.247
    model=02,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.0,He=0.247
    model=03,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.3,He=0.247
    model=04,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247
    model=11,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247
    model=12,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.275
    model=13,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.300
    model=14,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.320

    photometry:

    "HR":HR diagram
    "2MASS":2MASS
    "DECAM":DECam
    "Euclid":Euclid (VIS+NISP)
    "GAIADR1":GAIA DR1
    "GAIADR2":GAIA DR2
    "GAIADR3":GAIA DR3
    "GALEX":GALEX
    "Tycho":Hipparcos+Tycho
    "WFPC2":HST (WFPC2)
    "ACS":HST (ACS)
    "WFC3":HST (WFC3)
    "JPLUS":JPLUS
    "JohnsonCousins":JohnsonCousins
    "JWST_NIRCam":JWST (NIRCam)
    "JWST_NIRISS":JWST (NIRISS)
    "Kepler":Kepler
    "PanSTARSS1":PanSTARSS1
    "SAGE":SAGE
    "SkyMapper":SkyMapper
    "Sloan":Sloan
    <!"Spitzer_IRAC":Spitzer (IRAC)
    :"Stromgren":Strömgren
    "Subaru_HSC":Subaru (HSC)
    "SWIFT_UVOT":SWIFT (UVOT)
    "TESS":TESS
    "UVIT":UVIT (FUV+NUV+VIS)
    "LSST":Vera C. Rubin Obs. (LSST)
    "VISTA":VISTA
    "WFIRST":WFIRST (WFI)
    "WISE":WISE

    '''


    download_url='http://basti-iac.oa-abruzzo.inaf.it/TEMP/'

    url=_query(model=model,FeH=FeH,age=age,photometry=photometry)

    print('Interrogating {0}...'.format(url))
    print('Request...', end='')
    c = urlopen(url).read()
    c=c.decode()
    fname = re.compile('href=".*z').findall(c)[0].split('/')[2]


    min_age,max_age=_check_age(c)


    if (age>=min_age) & (age<=max_age):

#        furl = _cfg['download_url'] + fname
        furl = download_url + fname

        tarfile_url = furl



        print('Request...', end='')
        ftpstream = urllib.request.urlopen(tarfile_url)
        tmpfile = BytesIO()
        while True:
            s = ftpstream.read(16384)
            if not s:
                break
            tmpfile.write(s)
        ftpstream.close()
        tmpfile.seek(0)
        tfile = tarfile.open(fileobj=tmpfile, mode="r:gz")
        tfile_members2 = [filename for filename in tfile.getnames()]
        tfile_extract1 = tfile.extractfile(tfile_members2[0])
        tfile_extract_text = tfile_extract1.read().decode()
        tfile.close()
        tmpfile.close()
        print('decompressing archive...')

        text=tfile_extract_text.split('\n')
        #print(text)

        lines = [line_num for line_num, line_content in enumerate(text) if 'M/Mo(ini) ' in line_content]

        header_full=text[lines[0]].split(' ')
        header = [string for string in header_full if (string != "") & (string != "#")]
        data=Table.read(text,format='ascii',names=header)

        headline = [line_content for line_num, line_content in enumerate(text) if 'Np' in line_content]
        if len(headline)>0:
            lines = [line_content.replace('=',':').replace(" ","") for line_num, line_content in enumerate(headline[0].split('  ')) if '=' in line_content]
            dict_key={}
            for line in lines:
                dict_key.update({line.split(':')[0]:float(line.split(':')[1])})
                data[line.split(':')[0]]=float(line.split(':')[1])

        print("done.")
        return data

    else:
        print('Age not with in Range')
        print('Min Age:',min_age,'yr')
        print('Max Age:',max_age,'yr')
        return 0

def _select_model(model):

    list_model=[['model=01,Solar-Scaled[alpha/Fe]=0.0,Overshooting:No,Diffusion:No,Mass loss:n=0.0,He=0.247','P00','P00O0D0E0Y247',],
    ['model=02,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.0,He=0.247','P00','P00O1D0E0Y247',],
    ['model=03,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.3,He=0.247','P00','P00O1D0E1Y247',],
    ['model=04,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247','P00','P00O1D1E1Y247',],
    ['model=11,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247','P04','P04O1D1E1Y247',],
    ['model=12,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.275','P04','P04O1D1E1Y275',],
    ['model=13,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.300','P04','P04O1D1E1Y300',],
    ['model=14,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.320','P04','P04O1D1E1Y320']]


    dict_model={'01':list_model[0],'02':list_model[1],'03':list_model[2],'04':list_model[3],'05':list_model[4],'06':list_model[5],'07':list_model[6],'08':list_model[7]}

    return dict_model[model]

def _query(model='01',FeH=0.0,age=1e6,photometry='HR'):

    curr=_select_model(model)
    age=str(age/1e6)
    url='http://basti-iac.oa-abruzzo.inaf.it/cgi-bin/isoc-get.py?alpha='+curr[1]+'&grid='+curr[2]+'&metal=None&imetal=&imetalh='+str(FeH)+'&iage='+str(age)+'&bcsel='+str(photometry)

    return url

def _check_age(website):

    fname = re.compile(': age.*').findall(website)[0].replace('</h2>',"").split('--')
#    min_age=float(re.sub('\D', '', fname[0]))*1e6
#    max_age=float(re.sub('\D', '', fname[1]))*1e6

    min_age=float(re.findall('\d*\.?\d+',fname[0])[0])*1e6
    max_age=float(re.findall('\d*\.?\d+',fname[1])[0])*1e6

    return min_age,max_age

def print_model():
    for i in range(len(list_model)):
        print(list_model[i][0])

def print_photometric_system():
    '''
    "HR":HR diagram\n
    "2MASS":2MASS\n
    "DECAM":DECam\n
    "Euclid":Euclid (VIS+NISP)\n
    "GAIADR1":GAIA DR1\n
    "GAIADR2":GAIA DR2\n
    "GAIADR3":GAIA DR3\n
    "GALEX":GALEX\n
    "Tycho":Hipparcos+Tycho\n
    "WFPC2":HST (WFPC2)\n
    "ACS":HST (ACS)\n
    "WFC3":HST (WFC3)\n
    "JPLUS":JPLUS\n
    "JohnsonCousins":JohnsonCousins\n
    "JWST_NIRCam":JWST (NIRCam)\n
    "JWST_NIRISS":JWST (NIRISS)\n
    "Kepler":Kepler\n
    "PanSTARSS1":PanSTARSS1\n
    "SAGE":SAGE\n
    "SkyMapper":SkyMapper\n
    "Sloan":Sloan\n
    "Spitzer_IRAC":Spitzer (IRAC)\n:
    "Stromgren":Strömgren\n
    "Subaru_HSC":Subaru (HSC)\n
    "SWIFT_UVOT":SWIFT (UVOT)\n
    "TESS":TESS\n
    "UVIT":UVIT (FUV+NUV+VIS)\n
    "LSST":Vera C. Rubin Obs. (LSST)\n
    "VISTA":VISTA\n
    "WFIRST":WFIRST (WFI)\n
    "WISE":WISE\n
    '''
    print('"HR":HR diagram\n"2MASS":2MASS\n"DECAM":DECam\n"Euclid":Euclid (VIS+NISP)\n"GAIADR1":GAIA DR1\n"GAIADR2":GAIA DR2\n"GAIADR3":GAIA DR3\n"GALEX":GALEX\n"Tycho":Hipparcos+Tycho\n"WFPC2":HST (WFPC2)\n"ACS":HST (ACS)\n"WFC3":HST (WFC3)\n"JPLUS":JPLUS\n"JohnsonCousins":JohnsonCousins\n"JWST_NIRCam":JWST (NIRCam)\n"JWST_NIRISS":JWST (NIRISS)\n"Kepler":Kepler\n"PanSTARSS1":PanSTARSS1\n"SAGE":SAGE\n"SkyMapper":SkyMapper\n"Sloan":Sloan\n<!"Spitzer_IRAC":Spitzer (IRAC)\n:"Stromgren":Strömgren\n"Subaru_HSC":Subaru (HSC)\n"SWIFT_UVOT":SWIFT (UVOT)\n"TESS":TESS\n"UVIT":UVIT (FUV+NUV+VIS)\n"LSST":Vera C. Rubin Obs. (LSST)\n"VISTA":VISTA\n"WFIRST":WFIRST (WFI)\n"WISE":WISE\n')
