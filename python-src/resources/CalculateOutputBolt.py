import storm
import json

class CalculateOutputBolt(storm.BasicBolt):
  # Initialize this instance
  def initialize(self, conf, context):
    self._conf = conf
    self._context = context

  def process(self, tup):
    # ********** Read input arguments **********
    try:
      input_args = json.loads(tup.values[0])
    except:
      input_args = tup.values[0]
    ret_info = tup.values[1]

    # ********** Calculate results **********
    answer = 42

    # ********** Return results **********
    storm.emit([json.dumps(answer), ret_info])

# Start the bolt when it's invoked
CalculateOutputBolt().run()
