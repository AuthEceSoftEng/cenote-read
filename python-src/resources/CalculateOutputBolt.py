import storm


class CalculateOutputBolt(storm.BasicBolt):
  # Initialize this instance
  def initialize(self, conf, context):
    self._conf = conf
    self._context = context

  def process(self, tup):
    message = str(tup.values[0])
    storm.emit([message])


# Start the bolt when it's invoked
CalculateOutputBolt().run()
