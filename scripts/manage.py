#!/usr/bin/env python3

import sys, os, re
import json
import yaml
from pathlib import Path
import argparse
import traceback
from jinja2 import Template 

home = Path.home() / ".netrics-config"

if not home.exists():
  print("INFO: writing HOME dir")
  ( home / "data" / "backup" ) .mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(description='Config Netrics Deployments on FLOTO.')

parser.add_argument(
        '-i', '--input',
        default=False,
        type=str,
        help='Process the output of `balena devices -j` (json) as INPUT to generate a config database.',
)

parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List devices and their info.',
)

args = parser.parse_args()

print("///////////////////////////////////////////////////////////////////////")
print("nm-mgmt-config: Manage nm-exp-active-netrics.toml for FLOTO deployment.")
print("///////////////////////////////////////////////////////////////////////")
blacklist = None
if Path.exists( home / "data" / "database-blacklist.yaml" ):
  with open(home / "data" / "database-blacklist.yaml", "r") as stream:
      try:
          blacklist = yaml.safe_load(stream)
          blacklist_summary = {}
          for k in blacklist:
             try:
                blacklist_summary[blacklist[k]['fleet']]+=1
             except:
                blacklist_summary[blacklist[k]['fleet']]=0
          if args.list:
            print("Blacklisted:")
            for k in blacklist_summary:
                print(f"{k}:{blacklist_summary[k]}")
            print("")
          else:
            print("INFO: blacklist loaded OK.") 
      except yaml.YAMLError as exc:
          print(exc)

template = None
template_path = home / 'templates' / 'default' / \
               'nm-exp-active-netrics.template.toml.jinja';
if Path.exists( template_path ):
   print("INFO: Template default present.")
   with open(template_path) as f: 
      template = Template(f.read()) 
else:
   print(f"INFO: missing default template at "
         f"{(home / 'templates' / 'default' / 'nm-exp-active-netrics.template.toml.jinja')}.")
   sys.exit(1)


def gen_config(dev, fleet):
   """ Temporary config for Netrics V1 """
   result = {
      'TOPIC': fleet,
      'GITLOG': "new config",
      'DATAVER': 1,
      'DEBHASH': "0001",
      'log': "/var/nm/nm-exp-active-netrics/log/log.txt",
      'enable_ndev': "",
      'no_ipquery': "",
      'upload': "",
      'limit_consumption': "--limit-consumption",
      'SPEEDTEST_TIME': "0",
      'speedtest_hour': "0",
      'VCA_TIME': "0",
      'VCA_TIME_2': "0",
      'IPERF_TIME': "0",
      'iperf_hour': "0",
      'max_monthly_consumption_gb' : "200",
      'max_monthly_tests' : "200",
      'iperf_host': "abbott.cs.uchicago.edu",
      'IPERF_PORT': "33301"
      }
   return result

def generate_data_from(input_yaml, dst):
   """ Generate data (final yaml/toml config files) at dst folder """
   with open(input_yaml, "r") as stream:
      database = None
      try:
         database = yaml.safe_load(stream)
      except yaml.YAMLError as exc:
         print(exc)
      if database is not None:
         for k in database.keys():
            #print(k)
            if template is not None:
              output=template.render(database[k]['config'])
              (dst / k).mkdir(parents=True, exist_ok=True)
              with open( dst / k / "nm-exp-active-netrics.toml", "w") as f:
                 f.write(output)

def process_json(input_json):
   """ Process a typical json output from `balena devices -j` command """
   database = None
   database_new = {}
   if Path.exists( home / "data" / "database.yaml" ):
      with open(home / "data" / "database.yaml", "r") as stream:
         try:
            database = yaml.safe_load(stream)
         except yaml.YAMLError as exc:
            print(exc)

   with open(home / "data" / "database.yaml.new", "w" ) as dbnew:
      for k in input_json:
         existing = None
         if blacklist is not None:
            if k['uuid'] in blacklist.keys(): continue
         if database is not None:
            if k['uuid'] in database.keys():
               if not database[k['uuid']]['overwrite']:
                 print(f"Skipping [{k['uuid']}]")
                 existing = database[k['uuid']]
         
         fleet_canonical = re.sub(r'^[a-z]+/', '',k['fleet']).split("-")[0]

         if existing is not None:
            database_new[k['uuid']] = existing
         else:
            database_new[k['uuid']] = \
            { 
               'fleet' : fleet_canonical,
               'device_name' : k['device_name'],
               'overwrite' : True,
               'config' : gen_config(k, fleet_canonical)
            }
            
      output = yaml.dump(database_new)
      dbnew.write(output)
      print(output)

if args.input:
   input = vars(args)['input']
   print(f"INFO: processing [{input}]...")
   input_json = None
   with open(input) as f:
      try:
         input_json = json.load(f)
         print(f"INFO: {input} loaded.")
         process_json(input_json)
         generate_data_from( home / "data" / "database.yaml.new", home / "data" / "s3" )
      except Exception as ex:
         exc_type, _, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         print("ERROR: invalid input ({0}) {1} {2} {3}".format(str(ex), exc_type, fname, exc_tb.tb_lineno))
         traceback.print_exc()
         sys.exit(1)
      


