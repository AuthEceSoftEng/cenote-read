package com.issel.cenote;

import java.util.Map;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

public class AggregatorBolt extends ShellBolt implements IRichBolt {
  static final long serialVersionUID = 3L;

  AggregatorBolt() {
    super("/usr/bin/python3", "AggregatorBolt.py");
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("id", "read"));
  }

  @Override
  public Map<String, Object> getComponentConfiguration() {
    return null;
  }
}