package com.issel.cenote;


import org.apache.storm.Config;
import org.apache.storm.StormSubmitter;
import org.apache.storm.drpc.LinearDRPCTopologyBuilder;
import org.apache.storm.tuple.Fields;

public class ReadTopology {

  public static void main(String[] args) throws Exception {
    LinearDRPCTopologyBuilder builder = new LinearDRPCTopologyBuilder("read");
    builder.addBolt(new GetDataFromCassandraBolt(), 12);
    builder.addBolt(new CalculateOutputBolt(), 6).fieldsGrouping(new Fields("id"));
    builder.addBolt(new AggregatorBolt(), 3).fieldsGrouping(new Fields("id"));

    Config conf = new Config();
    conf.setNumWorkers(10);
    StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createRemoteTopology());
  }
}
