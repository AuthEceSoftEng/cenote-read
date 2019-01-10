package com.issel.cenote;


import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

import java.util.Map;

public class GetDataFromCassandraBolt extends ShellBolt implements IRichBolt {
  static final long serialVersionUID = 1L;

  GetDataFromCassandraBolt() {
    super("/usr/bin/python3", "GetDataFromCassandraBolt.py");
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("id", "row_of_data"));
  }

  @Override
  public Map<String, Object> getComponentConfiguration() {
    return null;
  }
}