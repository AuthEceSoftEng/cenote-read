import datetime
import json
import re

import storm
from CassandraHandler.DataRead import ReadData as rd
from CassandraHandler.utils.CassandraHandler import CassandraHandler as ch


def datetimeParser(o):
  if isinstance(o, datetime.datetime):
    return o.__str__()


class CalculateOutputBolt(storm.BasicBolt):
  # Initialize this instance
  def __init__(self):
    self._context = None
    self._conf = None
    self.reader = None
    self.handler = None

  def initialize(self, conf, context):
    self._context = context
    self._conf = conf
    self.reader = rd()
    self.handler = ch()

  def process(self, tup):
    # ********** Read input arguments **********

    try:
      input_args = json.loads(tup.values[0])
    except:
      input_args = tup.values[0]
    ret_info = tup.values[1]

    # ********** Calculate results **********

    # Construct required variables
    if "query_type" not in input_args:
      return storm.emit([json.dumps({"ok": False, "msg": "No `query_type` param provided!"}), ret_info])
    query_type = input_args["query_type"].lower()

    if query_type == "collections":
      answer = self.handler.describe_collections('cenote', input_args["PROJECT_ID"])
      return storm.emit([json.dumps({"ok": True, "msg": answer}), ret_info])

    timeframe_start = ""
    timeframe_end = ""
    if "timeframe_start" in input_args:
      timeframe_start = input_args["timeframe_start"]
    if "timeframe_end" in input_args:
      timeframe_end = input_args["timeframe_end"]
    info = {
      "cenote": {
        "url": "/projects/" + input_args["PROJECT_ID"] + "/queries/" + input_args["event_collection"] + "/extraction",
        "timeframe_start": timeframe_start,
        "timeframe_end": timeframe_end
      }
    }
    columns = None
    if "target_property" in input_args:
      columns = input_args["target_property"].split(",")

    # Execute corresponding query
    if query_type == "extraction":
      answer = self.reader.read_data("cenote", columns, json.dumps(info))
    elif query_type in ["count", "min", "max", "sum", "average", "median"]:
      answer = self.reader.perform_operation("cenote", columns, query_type, json.dumps(info))
    elif query_type == "percentile":
      info["cenote"]["percentile"] = int(input_args["percentile"])
      answer = self.reader.perform_operation("cenote", columns, query_type, json.dumps(info))
    else:
      answer = {"data": "Not implemented yet!"}

    # Return results
    if "response" in answer and answer["response"] == 200:
      # Hack-ia to turn "system.<someoperation>(<column>)" to "<column>"
      answer = json.loads(re.sub(r'system\.\w*\(|\)', "", json.dumps(answer, default=datetimeParser)))
      return storm.emit([json.dumps({"ok": True, "msg": answer["data"]}), ret_info])
    else:
      try:
        problem = answer["exception"]
      except:
        problem = answer["data"]
      return storm.emit([json.dumps({"ok": False, "msg": problem}), ret_info])


# Start the bolt when it's invoked
CalculateOutputBolt().run()
