package com.issel.cenote;


import org.apache.storm.Config;
import org.apache.storm.StormSubmitter;
import org.apache.storm.drpc.DRPCSpout;
import org.apache.storm.drpc.ReturnResults;
import org.apache.storm.topology.TopologyBuilder;

public class ReadTopology {

  public static void main(String[] args) throws Exception {
    Config conf = new Config();
    TopologyBuilder builder = new TopologyBuilder();

    builder.setSpout("drpc-spout", new DRPCSpout("read"), 2).setNumTasks(2);
    builder.setBolt("calculate-data", new CalculateOutputBolt(), 4).setNumTasks(4).shuffleGrouping("drpc-spout");
    builder.setBolt("return", new ReturnResults(), 4).setNumTasks(4).shuffleGrouping("calculate-data");

    conf.setNumWorkers(10);
    StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createTopology());
  }
}
