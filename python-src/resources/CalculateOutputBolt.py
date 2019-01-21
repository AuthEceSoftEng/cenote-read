import json

import storm
from CassandraHandler.utils.CassandraHandler import CassandraHandler
from CassandraHandler.DataRead import ReadData as rd


class CalculateOutputBolt(storm.BasicBolt):
  # Initialize this instance
  def __init__(self):
    self._context = None
    self._conf = None
    self.reader = None

  def initialize(self, conf, context):
    self._context = context
    self._conf = conf
    self.reader = rd()

  def process(self, tup):
    # ********** Read input arguments **********

    try:
      input_args = json.loads(tup.values[0])
    except:
      input_args = tup.values[0]
    ret_info = tup.values[1]

    # ********** Calculate results **********
    if "query_type" not in input_args:
      return storm.emit([json.dumps({"ok": False, "msg": 'No `query_type` param provided!'}), ret_info])
    query_type = input_args["query_type"].lower()
    if query_type == 'extraction':
      timeframe_start = ''
      timeframe_end = ''
      if "timeframe_start" in input_args: timeframe_start = input_args["timeframe_start"]
      if "timeframe_end" in input_args: timeframe_end = input_args["timeframe_end"]
      info = {
        "cenote": {
          "url": "/projects/" + input_args["PROJECT_ID"] + "/queries/" + input_args["event_collection"] + "/extraction",
          "timeframe_start": timeframe_start,
          "timeframe_end": timeframe_end
        }
      }
      if "target_property" in input_args:
        answer = self.reader.read_data('cenote', input_args["target_property"].split(","), json.dumps(info))
      else:
        answer = self.reader.read_data('cenote', None, json.dumps(info))
      return storm.emit([json.dumps({"ok": True, "msg": answer["data"]}), ret_info])
    else:
      return storm.emit([json.dumps({"ok": True, "msg": "Not implemented yet!"}), ret_info])

# Start the bolt when it's invoked
CalculateOutputBolt().run()
