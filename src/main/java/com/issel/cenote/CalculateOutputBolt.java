package com.issel.cenote;

import java.util.Map;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

public class CalculateOutputBolt extends ShellBolt implements IRichBolt {
  static final long serialVersionUID = 2L;

  CalculateOutputBolt() {
    super("/usr/bin/python3", "CalculateOutputBolt.py");
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("result", "return-info"));
  }

  @Override
  public Map<String, Object> getComponentConfiguration() {
    return null;
  }
}