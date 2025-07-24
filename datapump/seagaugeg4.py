import os
import requests
import sys
import json
from itertools import groupby, islice
from datetime import datetime, timedelta
import time
from time import mktime
import botocore
import boto3
from botocore.exceptions import ClientError

from psycopg_pool import ConnectionPool
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'), timeout=90)

import logging


# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = True
debug_all = False



#logging.basicConfig(level=logging.INFO)
#log = logging

logging.basicConfig(level=logging.ERROR)
log = logging

def get_xml_value(postdata, tag):
  
  startStr = "<" + tag + ">";
  endStr = "</" + tag + ">";
  startPos = -1
  endPos = -1

  #log.info("get_xml_value startStr %s  endStr %s", startStr, endStr )  

  startPos = postdata.find(startStr)
  #log.info("get_xml_value startPos %s ", startPos )  
  if startPos == -1:
    return ""

  startPos = startPos + len(startStr)

  endPos = postdata.find(endStr)
  #log.info("get_xml_value endPos %s", endPos )  
  if endPos == -1:
    return ""

  return postdata[startPos:endPos]

  log.info("set_seasmart_device_xml pulsexml %s", pulsexml)  
  return  




def get_hex2_from_tag(postdata, tag):

  try:
    
    index =int(get_xml_value(postdata, tag))

    log.info("get_hex2_from_tag index %s", index)  

    #return '0x' + format(index, '02x')
    return '0x' + '{:02X}'.format(index & ((1 << 8)-1))
  
  except:
    return '0xFF'

    
def get_hex4_from_tag(postdata, tag):
  
  try:

    log.info("get_hex4_from_tag index1 %s", get_xml_value(postdata, tag))
    
    index =int(get_xml_value(postdata, tag))  

    log.info("get_hex4_from_tag index2 %s", index)
    
    #return format(index, '#010x')
    return '0x' + '{:04X}'.format(index & ((1 << 16)-1))
  
  except:
    return '0xFFFF'
  
def get_hex8_from_tag(postdata, tag):
  
  try:
    
    index =int(get_xml_value(postdata, tag))  

    log.info("get_hex8_from_tag index %s", index)
    
    #return format(index, '#010x')
    return '0x' + '{:08X}'.format(index & ((1 << 32)-1))
  
  except:
    return '0xFFFFFFFF'
  
def get_pgnhex_from_tag(postdata, tag):

  """
  switch(PGNNumber )
      {
          case 0x1F201: // engine dynamic
          return 1;

          case 0x1F214: // battery status
          return 2;    

          case 0x1F211: // fluid level
          return 3;

          case 0x1F205: // Transmission dynamic
          return 4;

          case 0x1FD0A: // pressure
          return 5;

          case 0x1FD07: // temperature
          return 6;

          case 0x1FD08: // temperature
          return 7;

          case 0x1FD0C: // temperature extended
          return 8;

          case 0x1F10D: // rudder angle
          return 9;

          case 0x1F200: // rudder angle
          return 10;
          
          case 0x0FEEE: // J1939 Engine temperature 65262
          return 16;

          case 0x0FEEF: // J1939 Engine pressures 65263
          return 17;

          case 0x0FEF7: // J1939 Volts 65271
          return 18;

          case 0x0FEFC: // J1939 Fluids 65276
          return 19;

          case 0x0FEF8: // J1939 Transmission 65272
          return 20;

          default:
          return 0;
      }
  """

  index =int(get_xml_value(postdata, tag))

  if index == 0:
    return "0x000000"

  elif index ==1:
    return "0x1F201"

  elif index ==2:
    return "0x1F214"

  elif index ==3:
    return "0x1F211"

  elif index ==4:
    return "0x1F205"

  elif index ==5:
    return "0x1FD0A"

  elif index ==6:
    return "0x1FD07"

  elif index ==7:
    return "0x1FD08"

  elif index ==8:
    return "0x1FD0C"

  elif index ==9:
    return "0x1F10D"

  elif index == 10:
    return "0x1F200"

  elif index ==11:
    return "0x000000"

  elif index ==12:
    return "0x000000"

  elif index ==13:
    return "0x000000"

  elif index ==14:
    return "0x000000"

  elif index ==15:
    return "0x000000"

  elif index ==16:
    return "0x0FEEE"

  elif index ==17:
    return "0x0FEEF"

  elif index ==18:
    return "0x0FEF7"

  elif index ==19:
    return "0x0FEFC"
  
  elif index == 20:
    return "0x0FEF8"

  else:
    return "0x000000"

def add_seagauge_xml(request):

  #log.info("add_seagauge_xml postdata %s", postdata)

  userid = request.args.get('UserIDXML','')
  deviceid = request.args.get('DeviceIDXML','')
  prefname = request.args.get('PrefNameXML','')

  
  log.info("add_seagauge_xml userid %s deviceid %s prefname %s", userid, deviceid, prefname)

  
  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " insert into user_sgg4configxml ( useridkey, deviceid, prefname) values (%s, %s, %s);" 
  cursor.execute(sqlstr, (userid, deviceid, prefname, ))   
  conn.commit()

  db_pool.putconn(conn)

 
  #log.info("set_seasmart_device_xml pulsexml %s", pulsexml)  
  return

def delete_seagauge_xml(request):

  #log.info("add_seagauge_xml postdata %s", postdata)


  prefidkey = request.args.get('PrefKeyXML','')

  log.info("delete_seagauge_xml prefkey %s", prefidkey)

  if prefidkey == "":
    return

  if int(prefidkey) == 0:
    return  

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " delete from user_sgg4configxml where  prefidkey = %s;" 
  cursor.execute(sqlstr, (int(prefidkey), ))   
  conn.commit()

  db_pool.putconn(conn)

 
  #log.info("set_seasmart_device_xml pulsexml %s", pulsexml)  
  return


def create_seasmart_resets_xml(postdata):

  log.info("create_seasmart_device_xml postdata %s", postdata)


  xmlfile = ''
  
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  
  xmlfile = xmlfile + '<configgroup name = "RuntimePulse">\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configgroup name = "RuntimePIO">\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal03"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle03"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile


def create_seasmart_pulse_xml(postdata):

  log.info("create_seasmart_pulse_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "PULSE">\r\n'
  xmlfile = xmlfile + '<configitem name="PulseMode"><value>'+  get_xml_value(postdata, "PULSEMODE") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse0Scale"><value>'+  get_xml_value(postdata, "PULSESCALE0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse1Scale"><value>'+  get_xml_value(postdata, "PULSESCALE2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse2Scale"><value>'+  get_xml_value(postdata, "PULSESCALE2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseInterval"><value>'+  get_xml_value(postdata, "PINTERVAL") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FlowPulseInterval"><value>'+  get_xml_value(postdata, "FINTERVAL") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse0Filter"><value>'+  get_xml_value(postdata, "PFLT0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse1Filter"><value>'+  get_xml_value(postdata, "PFLT1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse2Filter"><value>'+  get_xml_value(postdata, "PFLT2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'


  return  xmlfile


def set_seasmart_pulse_xml(request):

  #log.info("set_seasmart_pulse_xml postdata", request.args)
  
  """
<DeviceID>AC1518EF5FA0</DeviceID>
<VersionInfo>1.9.3.7.12</VersionInfo>
<PULSEMODE>4</PULSEMODE>
<PULSESCALE0>1500</PULSESCALE0>
<PULSESCALE1>1500</PULSESCALE1>
<PULSESCALE2>5400</PULSESCALE2>
<PINTERVAL>1000</PINTERVAL>
<FINTERVAL>4000</FINTERVAL>
<PFLT0>0</PFLT0>
<PFLT1>0</PFLT1>
<PFLT2>3</PFLT2>
<FUELTOTAL>0</FUELTOTAL>
  """

  prefidkey = request.args.get('PrefKeyXML',0)
  prefName = request.args.get('PrefNameXML','')

  pulsexml = ""
  pulsexml = pulsexml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  pulsexml = pulsexml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  pulsexml = pulsexml +  '<PULSEMODE>'    +  request.args.get('PULSEModeDD','')  + '</PULSEMODE>'
  pulsexml = pulsexml +  '<PULSESCALE0>'    +  request.args.get('PULSE0SCALE','')  + '</PULSESCALE0>'  
  pulsexml = pulsexml +  '<PULSESCALE1>'    +  request.args.get('PULSE1SCALE','')  + '</PULSESCALE1>'  
  pulsexml = pulsexml +  '<PULSESCALE2>'    +  request.args.get('PULSE2SCALE','')  + '</PULSESCALE2>'  
  #pulsexml = pulsexml +  '<PINTERVAL>'    +  request.args.get('SDLogFName','')  + '</PINTERVAL>'  
  #pulsexml = pulsexml +  '<FINTERVAL>'    +  request.args.get('SDLogFName','')  + '</FINTERVAL>'
  pulsexml = pulsexml +  '<PINTERVAL>'    +  '1000'  + '</PINTERVAL>'  
  pulsexml = pulsexml +  '<FINTERVAL>'    +  '4000'  + '</FINTERVAL>'  
  pulsexml = pulsexml +  '<PFLT0>'    +  request.args.get('PULSE0FILTER','')  + '</PFLT0>'  
  pulsexml = pulsexml +  '<PFLT1>'    +  request.args.get('PULSE1FILTER','')  + '</PFLT1>'  
  pulsexml = pulsexml +  '<PFLT2>'    +  request.args.get('PULSE2FILTER','')  + '</PFLT2>'  
  pulsexml = pulsexml +  '<FUELTOTAL>'    +  request.args.get('FUELTACHTOTAL','')  + '</FUELTOTAL>'  

 

  log.info("set_seasmart_device_xml pulsexml %s", pulsexml)  


  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET pulsexml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (pulsexml, prefidkey, ))   
  conn.commit()


  db_pool.putconn(conn)
 

  return  





  
def create_seasmart_pgn_xml(postdata):

  log.info("create_seasmart_pgn_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "N2KPGNLists">\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN00"><value>' + get_pgnhex_from_tag(postdata, "PGNN0") + ',' + get_hex2_from_tag(postdata, "PGNI0") + ',' +  get_hex2_from_tag(postdata, "PGNP0") +',' + get_hex8_from_tag(postdata, "PGNS0") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN1") + ',' + get_hex2_from_tag(postdata, "PGNI1") + ',' +  get_hex2_from_tag(postdata, "PGNP1") +',' + get_hex8_from_tag(postdata, "PGNS1") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN2") + ',' + get_hex2_from_tag(postdata, "PGNI2") + ',' +  get_hex2_from_tag(postdata, "PGNP2") +',' + get_hex8_from_tag(postdata, "PGNS2") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN3") + ',' + get_hex2_from_tag(postdata, "PGNI3") + ',' +  get_hex2_from_tag(postdata, "PGNP3") +',' + get_hex8_from_tag(postdata, "PGNS3") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN4") + ',' + get_hex2_from_tag(postdata, "PGNI4") + ',' +  get_hex2_from_tag(postdata, "PGNP4") +',' + get_hex8_from_tag(postdata, "PGNS4") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN5") + ',' + get_hex2_from_tag(postdata, "PGNI5") + ',' +  get_hex2_from_tag(postdata, "PGNP5") +',' + get_hex8_from_tag(postdata, "PGNS5") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN6") + ',' + get_hex2_from_tag(postdata, "PGNI6") + ',' +  get_hex2_from_tag(postdata, "PGNP6") +',' + get_hex8_from_tag(postdata, "PGNS6") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN7") + ',' + get_hex2_from_tag(postdata, "PGNI7") + ',' +  get_hex2_from_tag(postdata, "PGNP7") +',' + get_hex8_from_tag(postdata, "PGNS7") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN8") + ',' + get_hex2_from_tag(postdata, "PGNI8") + ',' +  get_hex2_from_tag(postdata, "PGNP8") +',' + get_hex8_from_tag(postdata, "PGNS8") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN9") + ',' + get_hex2_from_tag(postdata, "PGNI9") + ',' +  get_hex2_from_tag(postdata, "PGNP9") +',' + get_hex8_from_tag(postdata, "PGNS9") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN10") + ',' + get_hex2_from_tag(postdata, "PGNI10") + ',' +  get_hex2_from_tag(postdata, "PGNP10") +',' + get_hex8_from_tag(postdata, "PGNS10") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN11") + ',' + get_hex2_from_tag(postdata, "PGNI11") + ',' +  get_hex2_from_tag(postdata, "PGNP11") +',' + get_hex8_from_tag(postdata, "PGNS11") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "N2KCalibrationTables">\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL00"><value>'+  get_xml_value(postdata, "CAL0") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL01"><value>'+  get_xml_value(postdata, "CAL1") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL02"><value>'+  get_xml_value(postdata, "CAL2") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL03"><value>'+  get_xml_value(postdata, "CAL3") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL04"><value>'+  get_xml_value(postdata, "CAL4") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL05"><value>'+  get_xml_value(postdata, "CAL5") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL06"><value>'+  get_xml_value(postdata, "CAL6") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL07"><value>'+  get_xml_value(postdata, "CAL7") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL08"><value>'+  get_xml_value(postdata, "CAL8") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL09"><value>'+  get_xml_value(postdata, "CAL9") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL10"><value>'+  get_xml_value(postdata, "CAL10") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL11"><value>'+  get_xml_value(postdata, "CAL11") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "ADCAlarms">\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM00"><value>'+ get_hex2_from_tag(postdata, "ADCAM0") + ',' +  get_hex4_from_tag(postdata, "ADCAL0") + ',' + get_hex4_from_tag(postdata, "ADCAH0")+ ',' + get_hex2_from_tag(postdata, "ADCAA0") + ',' + get_hex2_from_tag(postdata, "ADCAP0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM01"><value>'+ get_hex2_from_tag(postdata, "ADCAM1") + ',' +  get_hex4_from_tag(postdata, "ADCAL1") + ',' + get_hex4_from_tag(postdata, "ADCAH1")+ ',' + get_hex2_from_tag(postdata, "ADCAA1") + ',' + get_hex2_from_tag(postdata, "ADCAP1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM02"><value>'+ get_hex2_from_tag(postdata, "ADCAM2") + ',' +  get_hex4_from_tag(postdata, "ADCAL2") + ',' + get_hex4_from_tag(postdata, "ADCAH2")+ ',' + get_hex2_from_tag(postdata, "ADCAA2") + ',' + get_hex2_from_tag(postdata, "ADCAP2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM03"><value>'+ get_hex2_from_tag(postdata, "ADCAM3") + ',' +  get_hex4_from_tag(postdata, "ADCAL3") + ',' + get_hex4_from_tag(postdata, "ADCAH3")+ ',' + get_hex2_from_tag(postdata, "ADCAA3") + ',' + get_hex2_from_tag(postdata, "ADCAP3") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM04"><value>'+ get_hex2_from_tag(postdata, "ADCAM4") + ',' +  get_hex4_from_tag(postdata, "ADCAL4") + ',' + get_hex4_from_tag(postdata, "ADCAH4")+ ',' + get_hex2_from_tag(postdata, "ADCAA4") + ',' + get_hex2_from_tag(postdata, "ADCAP4") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM05"><value>'+ get_hex2_from_tag(postdata, "ADCAM5") + ',' +  get_hex4_from_tag(postdata, "ADCAL5") + ',' + get_hex4_from_tag(postdata, "ADCAH5")+ ',' + get_hex2_from_tag(postdata, "ADCAA5") + ',' + get_hex2_from_tag(postdata, "ADCAP5") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM06"><value>'+ get_hex2_from_tag(postdata, "ADCAM6") + ',' +  get_hex4_from_tag(postdata, "ADCAL6") + ',' + get_hex4_from_tag(postdata, "ADCAH6")+ ',' + get_hex2_from_tag(postdata, "ADCAA6") + ',' + get_hex2_from_tag(postdata, "ADCAP6") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM07"><value>'+ get_hex2_from_tag(postdata, "ADCAM7") + ',' +  get_hex4_from_tag(postdata, "ADCAL7") + ',' + get_hex4_from_tag(postdata, "ADCAH7")+ ',' + get_hex2_from_tag(postdata, "ADCAA7") + ',' + get_hex2_from_tag(postdata, "ADCAP7") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM08"><value>'+ get_hex2_from_tag(postdata, "ADCAM8") + ',' +  get_hex4_from_tag(postdata, "ADCAL8") + ',' + get_hex4_from_tag(postdata, "ADCAH8")+ ',' + get_hex2_from_tag(postdata, "ADCAA8") + ',' + get_hex2_from_tag(postdata, "ADCAP8") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM09"><value>'+ get_hex2_from_tag(postdata, "ADCAM9") + ',' +  get_hex4_from_tag(postdata, "ADCAL9") + ',' + get_hex4_from_tag(postdata, "ADCAH9")+ ',' + get_hex2_from_tag(postdata, "ADCAA9") + ',' + get_hex2_from_tag(postdata, "ADCAP9") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM10"><value>'+ get_hex2_from_tag(postdata, "ADCAM10") + ',' +  get_hex4_from_tag(postdata, "ADCAL10") + ',' + get_hex4_from_tag(postdata, "ADCAH10")+ ',' + get_hex2_from_tag(postdata, "ADCAA10") + ',' + get_hex2_from_tag(postdata, "ADCAP10") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM11"><value>'+ get_hex2_from_tag(postdata, "ADCAM11") + ',' +  get_hex4_from_tag(postdata, "ADCAL11") + ',' + get_hex4_from_tag(postdata, "ADCAH11")+ ',' + get_hex2_from_tag(postdata, "ADCAA11") + ',' + get_hex2_from_tag(postdata, "ADCAP11") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM12"><value>'+ get_hex2_from_tag(postdata, "ADCAM12") + ',' +  get_hex4_from_tag(postdata, "ADCAL12") + ',' + get_hex4_from_tag(postdata, "ADCAH12")+ ',' + get_hex2_from_tag(postdata, "ADCAA12") + ',' + get_hex2_from_tag(postdata, "ADCAP12") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM13"><value>'+ get_hex2_from_tag(postdata, "ADCAM13") + ',' +  get_hex4_from_tag(postdata, "ADCAL13") + ',' + get_hex4_from_tag(postdata, "ADCAH13")+ ',' + get_hex2_from_tag(postdata, "ADCAA13") + ',' + get_hex2_from_tag(postdata, "ADCAP13") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM14"><value>'+ get_hex2_from_tag(postdata, "ADCAM14") + ',' +  get_hex4_from_tag(postdata, "ADCAL14") + ',' + get_hex4_from_tag(postdata, "ADCAH14")+ ',' + get_hex2_from_tag(postdata, "ADCAA14") + ',' + get_hex2_from_tag(postdata, "ADCAP14") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM15"><value>'+ get_hex2_from_tag(postdata, "ADCAM15") + ',' +  get_hex4_from_tag(postdata, "ADCAL15") + ',' + get_hex4_from_tag(postdata, "ADCAH15")+ ',' + get_hex2_from_tag(postdata, "ADCAA15") + ',' + get_hex2_from_tag(postdata, "ADCAP15") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM16"><value>'+ get_hex2_from_tag(postdata, "ADCAM16") + ',' +  get_hex4_from_tag(postdata, "ADCAL16") + ',' + get_hex4_from_tag(postdata, "ADCAH16")+ ',' + get_hex2_from_tag(postdata, "ADCAA16") + ',' + get_hex2_from_tag(postdata, "ADCAP16") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM17"><value>'+ get_hex2_from_tag(postdata, "ADCAM17") + ',' +  get_hex4_from_tag(postdata, "ADCAL17") + ',' + get_hex4_from_tag(postdata, "ADCAH17")+ ',' + get_hex2_from_tag(postdata, "ADCAA17") + ',' + get_hex2_from_tag(postdata, "ADCAP17") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM18"><value>'+ get_hex2_from_tag(postdata, "ADCAM18") + ',' +  get_hex4_from_tag(postdata, "ADCAL18") + ',' + get_hex4_from_tag(postdata, "ADCAH18")+ ',' + get_hex2_from_tag(postdata, "ADCAA18") + ',' + get_hex2_from_tag(postdata, "ADCAP18") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM19"><value>'+ get_hex2_from_tag(postdata, "ADCAM19") + ',' +  get_hex4_from_tag(postdata, "ADCAL19") + ',' + get_hex4_from_tag(postdata, "ADCAH19")+ ',' + get_hex2_from_tag(postdata, "ADCAA19") + ',' + get_hex2_from_tag(postdata, "ADCAP19") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'



  return  xmlfile


def set_seasmart_pgn_xml(request):

  #log.info("set_seasmart_pgn_xml postdata", request.args)
  
  """
<DeviceID>AC1518EF5FA0</DeviceID>
<VersionInfo>1.9.3.7.12</VersionInfo>
<PULSEMODE>4</PULSEMODE>
<PULSESCALE0>1500</PULSESCALE0>
<PULSESCALE1>1500</PULSESCALE1>
<PULSESCALE2>5400</PULSESCALE2>
<PINTERVAL>1000</PINTERVAL>
<FINTERVAL>4000</FINTERVAL>
<PFLT0>0</PFLT0>
<PFLT1>0</PFLT1>
<PFLT2>3</PFLT2>
<FUELTOTAL>0</FUELTOTAL>
  """
  prefidkey = request.args.get('PrefKeyXML',0)
  prefName = request.args.get('PrefNameXML','')


  pgnxml = ""
  pgnxml = pgnxml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  pgnxml = pgnxml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  pgnxml = pgnxml +  '<ADCAA0>'    +  request.args.get('ADCAA0','')  + '</ADCAA0>'
  pgnxml = pgnxml +  '<ADCAA1>'    +  request.args.get('ADCAA1','')  + '</ADCAA1>'
  pgnxml = pgnxml +  '<ADCAA2>'    +  request.args.get('ADCAA2','')  + '</ADCAA2>'
  pgnxml = pgnxml +  '<ADCAA3>'    +  request.args.get('ADCAA3','')  + '</ADCAA3>'
  pgnxml = pgnxml +  '<ADCAA4>'    +  request.args.get('ADCAA4','')  + '</ADCAA4>'
  pgnxml = pgnxml +  '<ADCAA5>'    +  request.args.get('ADCAA5','')  + '</ADCAA5>'
  pgnxml = pgnxml +  '<ADCAA6>'    +  request.args.get('ADCAA6','')  + '</ADCAA6>'
  pgnxml = pgnxml +  '<ADCAA7>'    +  request.args.get('ADCAA7','')  + '</ADCAA7>'
  pgnxml = pgnxml +  '<ADCAA8>'    +  request.args.get('ADCAA8','')  + '</ADCAA8>'
  pgnxml = pgnxml +  '<ADCAA9>'    +  request.args.get('ADCAA9','')  + '</ADCAA9>'
  pgnxml = pgnxml +  '<ADCAA10>'    +  request.args.get('ADCAA10','')  + '</ADCAA10>'
  pgnxml = pgnxml +  '<ADCAA11>'    +  request.args.get('ADCAA11','')  + '</ADCAA11>'
  pgnxml = pgnxml +  '<ADCAA12>'    +  request.args.get('ADCAA12','')  + '</ADCAA12>'
  pgnxml = pgnxml +  '<ADCAA13>'    +  request.args.get('ADCAA13','')  + '</ADCAA13>'
  pgnxml = pgnxml +  '<ADCAA14>'    +  request.args.get('ADCAA14','')  + '</ADCAA14>'
  pgnxml = pgnxml +  '<ADCAA15>'    +  request.args.get('ADCAA15','')  + '</ADCAA15>'
  pgnxml = pgnxml +  '<ADCAA16>'    +  request.args.get('ADCAA16','')  + '</ADCAA16>'
  pgnxml = pgnxml +  '<ADCAA17>'    +  request.args.get('ADCAA17','')  + '</ADCAA17>'
  pgnxml = pgnxml +  '<ADCAA18>'    +  request.args.get('ADCAA18','')  + '</ADCAA18>'
  pgnxml = pgnxml +  '<ADCAA19>'    +  request.args.get('ADCAA19','')  + '</ADCAA19>'
  
  pgnxml = pgnxml +  '<ADCAH0>'    +  request.args.get('ADCAH0','')  + '</ADCAH0>'
  pgnxml = pgnxml +  '<ADCAH1>'    +  request.args.get('ADCAH1','')  + '</ADCAH1>'
  pgnxml = pgnxml +  '<ADCAH2>'    +  request.args.get('ADCAH2','')  + '</ADCAH2>'
  pgnxml = pgnxml +  '<ADCAH3>'    +  request.args.get('ADCAH3','')  + '</ADCAH3>'
  pgnxml = pgnxml +  '<ADCAH4>'    +  request.args.get('ADCAH4','')  + '</ADCAH4>'
  pgnxml = pgnxml +  '<ADCAH5>'    +  request.args.get('ADCAH5','')  + '</ADCAH5>'
  pgnxml = pgnxml +  '<ADCAH6>'    +  request.args.get('ADCAH6','')  + '</ADCAH6>'
  pgnxml = pgnxml +  '<ADCAH7>'    +  request.args.get('ADCAH7','')  + '</ADCAH7>'
  pgnxml = pgnxml +  '<ADCAH8>'    +  request.args.get('ADCAH8','')  + '</ADCAH8>'
  pgnxml = pgnxml +  '<ADCAH9>'    +  request.args.get('ADCAH9','')  + '</ADCAH9>'
  pgnxml = pgnxml +  '<ADCAH10>'    +  request.args.get('ADCAH10','')  + '</ADCAH10>'
  pgnxml = pgnxml +  '<ADCAH11>'    +  request.args.get('ADCAH11','')  + '</ADCAH11>'
  pgnxml = pgnxml +  '<ADCAH12>'    +  request.args.get('ADCAH12','')  + '</ADCAH12>'
  pgnxml = pgnxml +  '<ADCAH13>'    +  request.args.get('ADCAH13','')  + '</ADCAH13>'
  pgnxml = pgnxml +  '<ADCAH14>'    +  request.args.get('ADCAH14','')  + '</ADCAH14>'
  pgnxml = pgnxml +  '<ADCAH15>'    +  request.args.get('ADCAH15','')  + '</ADCAH15>'
  pgnxml = pgnxml +  '<ADCAH16>'    +  request.args.get('ADCAH16','')  + '</ADCAH16>'
  pgnxml = pgnxml +  '<ADCAH17>'    +  request.args.get('ADCAH17','')  + '</ADCAH17>'
  pgnxml = pgnxml +  '<ADCAH18>'    +  request.args.get('ADCAH18','')  + '</ADCAH18>'
  pgnxml = pgnxml +  '<ADCAH19>'    +  request.args.get('ADCAH19','')  + '</ADCAH19>'  
 
  pgnxml = pgnxml +  '<ADCAL0>'    +  request.args.get('ADCAL0','')  + '</ADCAL0>'
  pgnxml = pgnxml +  '<ADCAL1>'    +  request.args.get('ADCAL1','')  + '</ADCAL1>'
  pgnxml = pgnxml +  '<ADCAL2>'    +  request.args.get('ADCAL2','')  + '</ADCAL2>'
  pgnxml = pgnxml +  '<ADCAL3>'    +  request.args.get('ADCAL3','')  + '</ADCAL3>'
  pgnxml = pgnxml +  '<ADCAL4>'    +  request.args.get('ADCAL4','')  + '</ADCAL4>'
  pgnxml = pgnxml +  '<ADCAL5>'    +  request.args.get('ADCAL5','')  + '</ADCAL5>'
  pgnxml = pgnxml +  '<ADCAL6>'    +  request.args.get('ADCAL6','')  + '</ADCAL6>'
  pgnxml = pgnxml +  '<ADCAL7>'    +  request.args.get('ADCAL7','')  + '</ADCAL7>'
  pgnxml = pgnxml +  '<ADCAL8>'    +  request.args.get('ADCAL8','')  + '</ADCAL8>'
  pgnxml = pgnxml +  '<ADCAL9>'    +  request.args.get('ADCAL9','')  + '</ADCAL9>'
  pgnxml = pgnxml +  '<ADCAL10>'    +  request.args.get('ADCAL10','')  + '</ADCAL10>'
  pgnxml = pgnxml +  '<ADCAL11>'    +  request.args.get('ADCAL11','')  + '</ADCAL11>'
  pgnxml = pgnxml +  '<ADCAL12>'    +  request.args.get('ADCAL12','')  + '</ADCAL12>'
  pgnxml = pgnxml +  '<ADCAL13>'    +  request.args.get('ADCAL13','')  + '</ADCAL13>'
  pgnxml = pgnxml +  '<ADCAL14>'    +  request.args.get('ADCAL14','')  + '</ADCAL14>'
  pgnxml = pgnxml +  '<ADCAL15>'    +  request.args.get('ADCAL15','')  + '</ADCAL15>'
  pgnxml = pgnxml +  '<ADCAL16>'    +  request.args.get('ADCAL16','')  + '</ADCAL16>'
  pgnxml = pgnxml +  '<ADCAL17>'    +  request.args.get('ADCAL17','')  + '</ADCAL17>'
  pgnxml = pgnxml +  '<ADCAL18>'    +  request.args.get('ADCAL18','')  + '</ADCAL18>'
  pgnxml = pgnxml +  '<ADCAL19>'    +  request.args.get('ADCAL19','')  + '</ADCAL19>'  
 

  pgnxml = pgnxml +  '<ADCAM0>'    +  request.args.get('ADCAM0','')  + '</ADCAM0>'
  pgnxml = pgnxml +  '<ADCAM1>'    +  request.args.get('ADCAM1','')  + '</ADCAM1>'
  pgnxml = pgnxml +  '<ADCAM2>'    +  request.args.get('ADCAM2','')  + '</ADCAM2>'
  pgnxml = pgnxml +  '<ADCAM3>'    +  request.args.get('ADCAM3','')  + '</ADCAM3>'
  pgnxml = pgnxml +  '<ADCAM4>'    +  request.args.get('ADCAM4','')  + '</ADCAM4>'
  pgnxml = pgnxml +  '<ADCAM5>'    +  request.args.get('ADCAM5','')  + '</ADCAM5>'
  pgnxml = pgnxml +  '<ADCAM6>'    +  request.args.get('ADCAM6','')  + '</ADCAM6>'
  pgnxml = pgnxml +  '<ADCAM7>'    +  request.args.get('ADCAM7','')  + '</ADCAM7>'
  pgnxml = pgnxml +  '<ADCAM8>'    +  request.args.get('ADCAM8','')  + '</ADCAM8>'
  pgnxml = pgnxml +  '<ADCAM9>'    +  request.args.get('ADCAM9','')  + '</ADCAM9>'
  pgnxml = pgnxml +  '<ADCAM10>'    +  request.args.get('ADCAM10','')  + '</ADCAM10>'
  pgnxml = pgnxml +  '<ADCAM11>'    +  request.args.get('ADCAM11','')  + '</ADCAM11>'
  pgnxml = pgnxml +  '<ADCAM12>'    +  request.args.get('ADCAM12','')  + '</ADCAM12>'
  pgnxml = pgnxml +  '<ADCAM13>'    +  request.args.get('ADCAM13','')  + '</ADCAM13>'
  pgnxml = pgnxml +  '<ADCAM14>'    +  request.args.get('ADCAM14','')  + '</ADCAM14>'
  pgnxml = pgnxml +  '<ADCAM15>'    +  request.args.get('ADCAM15','')  + '</ADCAM15>'
  pgnxml = pgnxml +  '<ADCAM16>'    +  request.args.get('ADCAM16','')  + '</ADCAM16>'
  pgnxml = pgnxml +  '<ADCAM17>'    +  request.args.get('ADCAM17','')  + '</ADCAM17>'
  pgnxml = pgnxml +  '<ADCAM18>'    +  request.args.get('ADCAM18','')  + '</ADCAM18>'
  pgnxml = pgnxml +  '<ADCAM19>'    +  request.args.get('ADCAM19','')  + '</ADCAM19>'

  
  pgnxml = pgnxml +  '<ADCAP0>'    +  request.args.get('ADCAP0','')  + '</ADCAP0>'
  pgnxml = pgnxml +  '<ADCAP1>'    +  request.args.get('ADCAP1','')  + '</ADCAP1>'
  pgnxml = pgnxml +  '<ADCAP2>'    +  request.args.get('ADCAP2','')  + '</ADCAP2>'
  pgnxml = pgnxml +  '<ADCAP3>'    +  request.args.get('ADCAP3','')  + '</ADCAP3>'
  pgnxml = pgnxml +  '<ADCAP4>'    +  request.args.get('ADCAP4','')  + '</ADCAP4>'
  pgnxml = pgnxml +  '<ADCAP5>'    +  request.args.get('ADCAP5','')  + '</ADCAP5>'
  pgnxml = pgnxml +  '<ADCAP6>'    +  request.args.get('ADCAP6','')  + '</ADCAP6>'
  pgnxml = pgnxml +  '<ADCAP7>'    +  request.args.get('ADCAP7','')  + '</ADCAP7>'
  pgnxml = pgnxml +  '<ADCAP8>'    +  request.args.get('ADCAP8','')  + '</ADCAP8>'
  pgnxml = pgnxml +  '<ADCAP9>'    +  request.args.get('ADCAP9','')  + '</ADCAP9>'
  pgnxml = pgnxml +  '<ADCAP10>'    +  request.args.get('ADCAP10','')  + '</ADCAP10>'
  pgnxml = pgnxml +  '<ADCAP11>'    +  request.args.get('ADCAP11','')  + '</ADCAP11>'
  pgnxml = pgnxml +  '<ADCAP12>'    +  request.args.get('ADCAP12','')  + '</ADCAP12>'
  pgnxml = pgnxml +  '<ADCAP13>'    +  request.args.get('ADCAP13','')  + '</ADCAP13>'
  pgnxml = pgnxml +  '<ADCAP14>'    +  request.args.get('ADCAP14','')  + '</ADCAP14>'
  pgnxml = pgnxml +  '<ADCAP15>'    +  request.args.get('ADCAP15','')  + '</ADCAP15>'
  pgnxml = pgnxml +  '<ADCAP16>'    +  request.args.get('ADCAP16','')  + '</ADCAP16>'
  pgnxml = pgnxml +  '<ADCAP17>'    +  request.args.get('ADCAP17','')  + '</ADCAP17>'
  pgnxml = pgnxml +  '<ADCAP18>'    +  request.args.get('ADCAP18','')  + '</ADCAP18>'
  pgnxml = pgnxml +  '<ADCAP19>'    +  request.args.get('ADCAP19','')  + '</ADCAP19>'


  pgnxml = pgnxml +  '<PGNN0>'    +  request.args.get('PGNN0','')  + '</PGNN0>'
  pgnxml = pgnxml +  '<PGNN1>'    +  request.args.get('PGNN1','')  + '</PGNN1>'
  pgnxml = pgnxml +  '<PGNN2>'    +  request.args.get('PGNN2','')  + '</PGNN2>'
  pgnxml = pgnxml +  '<PGNN3>'    +  request.args.get('PGNN3','')  + '</PGNN3>'
  pgnxml = pgnxml +  '<PGNN4>'    +  request.args.get('PGNN4','')  + '</PGNN4>'
  pgnxml = pgnxml +  '<PGNN5>'    +  request.args.get('PGNN5','')  + '</PGNN5>'
  pgnxml = pgnxml +  '<PGNN6>'    +  request.args.get('PGNN6','')  + '</PGNN6>'
  pgnxml = pgnxml +  '<PGNN7>'    +  request.args.get('PGNN7','')  + '</PGNN7>'
  pgnxml = pgnxml +  '<PGNN8>'    +  request.args.get('PGNN8','')  + '</PGNN8>'
  pgnxml = pgnxml +  '<PGNN9>'    +  request.args.get('PGNN9','')  + '</PGNN9>'
  pgnxml = pgnxml +  '<PGNN10>'    +  request.args.get('PGNN10','')  + '</PGNN10>'
  pgnxml = pgnxml +  '<PGNN11>'    +  request.args.get('PGNN11','')  + '</PGNN11>'

  
  pgnxml = pgnxml +  '<PGNI0>'    +  request.args.get('PGNI0','')  + '</PGNI0>'
  pgnxml = pgnxml +  '<PGNI1>'    +  request.args.get('PGNI1','')  + '</PGNI1>'
  pgnxml = pgnxml +  '<PGNI2>'    +  request.args.get('PGNI2','')  + '</PGNI2>'
  pgnxml = pgnxml +  '<PGNI3>'    +  request.args.get('PGNI3','')  + '</PGNI3>'
  pgnxml = pgnxml +  '<PGNI4>'    +  request.args.get('PGNI4','')  + '</PGNI4>'
  pgnxml = pgnxml +  '<PGNI5>'    +  request.args.get('PGNI5','')  + '</PGNI5>'
  pgnxml = pgnxml +  '<PGNI6>'    +  request.args.get('PGNI6','')  + '</PGNI6>'
  pgnxml = pgnxml +  '<PGNI7>'    +  request.args.get('PGNI7','')  + '</PGNI7>'
  pgnxml = pgnxml +  '<PGNI8>'    +  request.args.get('PGNI8','')  + '</PGNI8>'
  pgnxml = pgnxml +  '<PGNI9>'    +  request.args.get('PGNI9','')  + '</PGNI9>'
  pgnxml = pgnxml +  '<PGNI10>'    +  request.args.get('PGNI10','')  + '</PGNI10>'
  pgnxml = pgnxml +  '<PGNI11>'    +  request.args.get('PGNI11','')  + '</PGNI11>'

  pgnxml = pgnxml +  '<PGNP0>'    +  request.args.get('PGNP0','')  + '</PGNP0>'
  pgnxml = pgnxml +  '<PGNP1>'    +  request.args.get('PGNP1','')  + '</PGNP1>'
  pgnxml = pgnxml +  '<PGNP2>'    +  request.args.get('PGNP2','')  + '</PGNP2>'
  pgnxml = pgnxml +  '<PGNP3>'    +  request.args.get('PGNP3','')  + '</PGNP3>'
  pgnxml = pgnxml +  '<PGNP4>'    +  request.args.get('PGNP4','')  + '</PGNP4>'
  pgnxml = pgnxml +  '<PGNP5>'    +  request.args.get('PGNP5','')  + '</PGNP5>'
  pgnxml = pgnxml +  '<PGNP6>'    +  request.args.get('PGNP6','')  + '</PGNP6>'
  pgnxml = pgnxml +  '<PGNP7>'    +  request.args.get('PGNP7','')  + '</PGNP7>'
  pgnxml = pgnxml +  '<PGNP8>'    +  request.args.get('PGNP8','')  + '</PGNP8>'
  pgnxml = pgnxml +  '<PGNP9>'    +  request.args.get('PGNP9','')  + '</PGNP9>'
  pgnxml = pgnxml +  '<PGNP10>'    +  request.args.get('PGNP10','')  + '</PGNP10>'
  pgnxml = pgnxml +  '<PGNP11>'    +  request.args.get('PGNP11','')  + '</PGNP11>'

  pgnxml = pgnxml +  '<PGNS0>'    +  request.args.get('PGNS0','')  + '</PGNS0>'
  pgnxml = pgnxml +  '<PGNS1>'    +  request.args.get('PGNS1','')  + '</PGNS1>'
  pgnxml = pgnxml +  '<PGNS2>'    +  request.args.get('PGNS2','')  + '</PGNS2>'
  pgnxml = pgnxml +  '<PGNS3>'    +  request.args.get('PGNS3','')  + '</PGNS3>'
  pgnxml = pgnxml +  '<PGNS4>'    +  request.args.get('PGNS4','')  + '</PGNS4>'
  pgnxml = pgnxml +  '<PGNS5>'    +  request.args.get('PGNS5','')  + '</PGNS5>'
  pgnxml = pgnxml +  '<PGNS6>'    +  request.args.get('PGNS6','')  + '</PGNS6>'
  pgnxml = pgnxml +  '<PGNS7>'    +  request.args.get('PGNS7','')  + '</PGNS7>'
  pgnxml = pgnxml +  '<PGNS8>'    +  request.args.get('PGNS8','')  + '</PGNS8>'
  pgnxml = pgnxml +  '<PGNS9>'    +  request.args.get('PGNS9','')  + '</PGNS9>'
  pgnxml = pgnxml +  '<PGNS10>'    +  request.args.get('PGNS10','')  + '</PGNS10>'
  pgnxml = pgnxml +  '<PGNS11>'    +  request.args.get('PGNS11','')  + '</PGNS11>'  


  pgnxml = pgnxml +  '<CAL0>'    +  request.args.get('CALFILE0','')  + '</CAL0>'
  pgnxml = pgnxml +  '<CAL1>'    +  request.args.get('CALFILE1','')  + '</CAL1>'
  pgnxml = pgnxml +  '<CAL2>'    +  request.args.get('CALFILE2','')  + '</CAL2>'
  pgnxml = pgnxml +  '<CAL3>'    +  request.args.get('CALFILE3','')  + '</CAL3>'
  pgnxml = pgnxml +  '<CAL4>'    +  request.args.get('CALFILE4','')  + '</CAL4>'
  pgnxml = pgnxml +  '<CAL5>'    +  request.args.get('CALFILE5','')  + '</CAL5>'
  pgnxml = pgnxml +  '<CAL6>'    +  request.args.get('CALFILE6','')  + '</CAL6>'
  pgnxml = pgnxml +  '<CAL7>'    +  request.args.get('CALFILE7','')  + '</CAL7>'
  pgnxml = pgnxml +  '<CAL8>'    +  request.args.get('CALFILE8','')  + '</CAL8>'
  pgnxml = pgnxml +  '<CAL9>'    +  request.args.get('CALFILE9','')  + '</CAL9>'
  pgnxml = pgnxml +  '<CAL10>'    +  request.args.get('CALFILE10','')  + '</CAL10>'
  pgnxml = pgnxml +  '<CAL11>'    +  request.args.get('CALFILE11','')  + '</CAL11>'

  
  log.info("set_seasmart_device_xml pgnxml %s", pgnxml)  

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET pgnsxml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (pgnxml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 

  return  

def create_seasmart_device_xml(postdata):

  log.info("create_seasmart_device_xml postdata %s", postdata)


  xmlfile = ''
  
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2K_STATUS_BUFF"><value>65535</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Dimmer_Type"><value>'+  get_xml_value(postdata, "DIMMERTYPE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Switch_PGN_Instance"><value>'+  get_xml_value(postdata, "DIMMERINSTANCE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CAN_Mode"><value>'+  get_xml_value(postdata, "CANMODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CANFILTERHB"><value>4294967295</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CANFILTERLB"><value>4294967295</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart0_Mode"><value>'+  get_xml_value(postdata, "UART0MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart1_Mode"><value>'+  get_xml_value(postdata, "UART1MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart2_Mode"><value>'+  get_xml_value(postdata, "UART2MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SDLogEnable"><value>'+  get_xml_value(postdata, "SDLogEnable") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SDLogInterval"><value>'+  get_xml_value(postdata, "SDLogInterval") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Sample_Interval"><value>2</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="RTCEnable"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="TimeSource"><value>'+  get_xml_value(postdata, "TimeSource") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="HTTP_POST_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="HTTP_SD_POST_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SD_LOG_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile

def set_seasmart_device_xml(request):

  #log.info("set_seasmart_device_xml postdata", request.args)
  prefidkey = request.args.get('PrefKeyXML',0)
  prefName = request.args.get('PrefNameXML','')

  devicexml = ""
  devicexml = devicexml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  devicexml = devicexml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  devicexml = devicexml +  '<SDLogEnable>'    +  request.args.get('SDLogFName','')  + '</SDLogEnable>'
  devicexml = devicexml +  '<SDLogInterval>'    +  request.args.get('SDLogInterval','')  + '</SDLogInterval>'
  devicexml = devicexml +  '<UartInterval>'    +  request.args.get('UartInterval','')  + '</UartInterval>'
  devicexml = devicexml +  '<UART0MODE>'    +  request.args.get('UART0ModeDD','')  + '</UART0MODE>'
  devicexml = devicexml +  '<UART1MODE>'    +  request.args.get('UART1ModeDD','')  + '</UART1MODE>'
  devicexml = devicexml +  '<UART2MODE>'    +  request.args.get('UART2ModeDD','')  + '</UART2MODE>'
  devicexml = devicexml +  '<CANMODE>'    +  request.args.get('CANModeDD','')  + '</CANMODE>'
  #devicexml = devicexml +  '<CANFILTERHB>'    +  request.args.get('WIFINetType_CB','')  + '</CANFILTERHB>'
  #devicexml = devicexml +  '<CANFILTERLB>'    +  request.args.get('WIFINetType_CB','')  + '</CANFILTERLB>'
  devicexml = devicexml +  '<CANFILTERHB>'    +  '4294967295'  + '</CANFILTERHB>'
  devicexml = devicexml +  '<CANFILTERLB>'    +  '4294967295'  + '</CANFILTERLB>'
  devicexml = devicexml +  '<DIMMERTYPE>'    +  request.args.get('DimmerTypeDD','')  + '</DIMMERTYPE>'
  devicexml = devicexml +  '<DIMMERINSTANCE>'    +  request.args.get('DimmerInstanceDD','')  + '</DIMMERINSTANCE>'
  devicexml = devicexml +  '<DIMMERSCALE>'    +  request.args.get('DIMMERSCALE','')  + '</DIMMERSCALE>'
  devicexml = devicexml +  '<DIMMERPON>'    +  request.args.get('DimmerPONDD','')  + '</DIMMERPON>'
  devicexml = devicexml +  '<DIMMERTXRATE>'    +  request.args.get('DimmerTXDD','')  + '</DIMMERTXRATE>'
  devicexml = devicexml +  '<TIMERMODE>'    +  request.args.get('TimerModeDD','')  + '</TIMERMODE>'
  devicexml = devicexml +  '<TimeSource>'    +  request.args.get('TimeStampSource','')  + '</TimeSource>'

 
  log.info("set_seasmart_device_xml networkxml %s", devicexml)  

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET devicexml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (devicexml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 

  return  

    

def create_seasmart_network_xml(postdata):

  log.info("create_seasmart_network_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "Network">\r\n'
  xmlfile = xmlfile + '<configitem name="DHCP"><value>'+  get_xml_value(postdata, "DHCP") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="IPAddress"><value>'+  get_xml_value(postdata, "IPAddress") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SubNet"><value>'+  get_xml_value(postdata, "IPMask") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Gateway"><value>'+  get_xml_value(postdata, "IPGateway") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="DNS1"><value>'+  get_xml_value(postdata, "DNS1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="DNS2"><value>'+  get_xml_value(postdata, "DNS2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "WIFI">\r\n'
  xmlfile = xmlfile + '<configitem name="WiFiType"><value>'+  get_xml_value(postdata, "WIFIType") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASSID"><value>'+  get_xml_value(postdata, "STAWIFISSID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASECTYPE"><value>'+  get_xml_value(postdata, "APWIFIMode") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASECKEY"><value>'+  get_xml_value(postdata, "STAWIFIPW") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSSID"><value>'+  get_xml_value(postdata, "APWIFISSID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSECTYPE"><value>'+  get_xml_value(postdata, "APWIFIMode") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSECKEY"><value>'+  get_xml_value(postdata, "APWIFIPW") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "UDP">\r\n'
  xmlfile = xmlfile + '<configitem name="UDPEnable"><value>'+  get_xml_value(postdata, "UDPBroadcastEnable") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="UDPPort"><value>'+  get_xml_value(postdata, "UDPClientPort") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configgroup name = "TCP">\r\n'
  xmlfile = xmlfile + '<configitem name="TCPEnable"><value>'+  get_xml_value(postdata, "TCPEnable") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="TCPPort"><value>'+  get_xml_value(postdata, "TCPServerPort") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "HTTPPOST">\r\n'
  xmlfile = xmlfile + '<configitem name="PostType"><value>'+  get_xml_value(postdata, "HTTPPostMenu") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PostInterval"><value>'+  get_xml_value(postdata, "HpptPostInterval") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile

def set_seasmart_network_xml(request):

  #log.info("set_seasmart_network_xml postdata", request.args)

  prefidkey = request.args.get('PrefKeyXML',0)
  prefName = request.args.get('PrefNameXML','')

  networkxml = ""
  networkxml = networkxml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  networkxml = networkxml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  networkxml = networkxml +  '<WIFIType>'    +  request.args.get('WIFINetType_CB','')  + '</WIFIType>'
  networkxml = networkxml +  '<STAWIFISSID>'    +  request.args.get('SSID','')  + '</STAWIFISSID>\r\n'
  networkxml = networkxml +  '<STAWIFIPW>'    +  request.args.get('STAPASSWORD','')  + '</STAWIFIPW>'
  networkxml = networkxml +  '<APWIFISSID>'    +  request.args.get('APSSID','')  + '</APWIFISSID>'
  networkxml = networkxml +  '<APWIFIPW>'    +  request.args.get('APSECKEY','')  + '</APWIFIPW>'
  networkxml = networkxml +  '<APWIFIMode>'    +  request.args.get('APSECTYPE','')  + '</APWIFIMode>'
  networkxml = networkxml +  '<MESHCHANNEL>'    +  request.args.get('MESHCHANNEL','')  + '</MESHCHANNEL>'
  networkxml = networkxml +  '<MESHID>'    +  request.args.get('MESHID','')  + '</MESHID>'
  networkxml = networkxml +  '<CIPAddress>'    +  request.args.get('IPaddressXML','')  + '</CIPAddress>'
  networkxml = networkxml +  '<CIPMask>'    +  request.args.get('IPMaskXML','')  + '</CIPMask>'
  networkxml = networkxml +  '<CIPGW>'    +  request.args.get('IPGatewayXML','')  + '</CIPGW>'
  networkxml = networkxml +  '<DHCP>'    +  request.args.get('DHCPCLIENT_ON_CB','')  + '</DHCP>'
  networkxml = networkxml +  '<IPAddress>'    +  request.args.get('IPADDR','')  + '</IPAddress>'
  networkxml = networkxml +  '<IPMask>'    +  request.args.get('SUBNET','')  + '</IPMask>'
  networkxml = networkxml +  '<IPGateway>'    +  request.args.get('GATEWAY','')  + '</IPGateway>'
  networkxml = networkxml +  '<DNS1>'    +  request.args.get('DNS1','')  + '</DNS1>'
  networkxml = networkxml +  '<DNS2>'    +  request.args.get('DNS2','')  + '</DNS2>'
  networkxml = networkxml +  '<HpptPostInterval>'    +  request.args.get('HttpPostInterval','')  + '</HpptPostInterval>'
  networkxml = networkxml +  '<HTTPPostMenu>'    +  request.args.get('HTTPPostMenu','')  + '</HTTPPostMenu>'
  networkxml = networkxml +  '<SSIDDefault>'    +  request.args.get('SSID','')  + '</SSIDDefault>'
  networkxml = networkxml +  '<NETTYPE>'    +  request.args.get('NetTypeXML','')  + '</NETTYPE>'
  networkxml = networkxml +  '<TCPServerPort>'    +  request.args.get('TCPSERVERPORT','')  + '</TCPServerPort>'
  networkxml = networkxml +  '<TCPEnable>'    +  request.args.get('TCPSERVER_ON_CB','')  + '</TCPEnable>'
  networkxml = networkxml +  '<UDPClientPort>'    +  request.args.get('UDPBROADPORT','')  + '</UDPClientPort>'
  networkxml = networkxml +  '<UDPBroadcastEnable>'    +  request.args.get('UDPBROADCAST_ON_CB','')  + '</UDPBroadcastEnable>'


  log.info("set_seasmart_network_xml networkxml %s", networkxml)  

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET networkxml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (networkxml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 

  return  
