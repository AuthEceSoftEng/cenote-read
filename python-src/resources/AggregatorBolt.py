import storm


class AggregatorBolt(storm.BasicBolt):
  # Initialize this instance
  def initialize(self, conf, context):
    self._conf = conf
    self._context = context
    self.result = None

  def process(self, tup):
    self.message = str(tup.values[0])

  def finishBatch(self):
    storm.emit([self.result])


# Start the bolt when it's invoked
AggregatorBolt().run()
