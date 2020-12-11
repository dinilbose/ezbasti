EZBASTI -- A python package that allows you to query and download BASTI isochrones directly from their website
=======================================================================================================
Basti Website: http://basti-iac.oa-abruzzo.inaf.it/isocs.html

**version: 0.1 (beta) Under testing, No issues found yet.**

Installation
------------
Install with pip

```
pip install git+https://github.com/dinilbose/ezbasti
```
(`--user` if you want to install it in your user profile)


USAGE
-----
* Basic example of downloading a single isochrones
```python
data=get_one_isochrone(model='01',FeH=0.1,age=16e6,photometry='HR')
```
gives astropy table. To convert to pandas table use
```
dataframe=data.to_pandas()
```
* Isochrone with GAIA bands
```python
data=get_one_isochrone(model='13',FeH=0.1,age=16e6,photometry='GAIADR2')
```



Parameters
-----

* model

8 models of isochrone are available from the BASTI website. Select model using the model number

```
model=01,Solar-Scaled[alpha/Fe]=0.0,Overshooting:No,Diffusion:No,Mass loss:n=0.0,He=0.247
model=02,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.0,He=0.247
model=03,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:No,Mass loss:n=0.3,He=0.247
model=04,Solar-Scaled[alpha/Fe]=0.0,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247
model=11,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.247
model=12,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.275
model=13,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.300
model=14,Alpha-enhanced[alpha/Fe]=+0.4,Overshooting:Yes,Diffusion:Yes,Mass loss:n=0.3,He=0.320
```

* photometry

The available photometric systems are follows for more info visit

http://basti-iac.oa-abruzzo.inaf.it/helpisocs.html


```
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
```

### Inspiration
This package is similar to

ezpadova: https://github.com/mfouesneau/ezpadova

ezmist: https://github.com/mfouesneau/ezmist/
