import json

import storm
from CassandraHandler.utils.CassandraHandler import CassandraHandler


class CalculateOutputBolt(storm.BasicBolt):
  # Initialize this instance
  def initialize(self, conf, context):
    self._conf = conf
    self._context = context
    self.cql = CassandraHandler().execute_query

  def process(self, tup):
    # ********** Read input arguments **********
    try:
      input_args = json.loads(tup.values[0])
    except:
      input_args = tup.values[0]
    ret_info = tup.values[1]

    # ********** Calculate results **********
    answer = 42
    if ("cql" in input_args):
      if input_args["cql"]["mode"].lower() == "select":
        answer = list(self.cql(
            'select ' + input_args["cql"]["columns"] + ' from cenote.' + input_args["cql"]["table"])[0].items())

    # ********** Return results **********
    storm.emit([json.dumps(answer), ret_info])

# Start the bolt when it's invoked
CalculateOutputBolt().run()
