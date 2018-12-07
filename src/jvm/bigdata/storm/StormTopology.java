package bigdata.storm;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.topology.TopologyBuilder;

public class StormTopology {
	
	static final String TOPOLOGY_NAME = "storm-twitter-analysis";
	
	public static void main(String[] args) throws Exception {
		
		Config conf = new Config();
		conf.setMessageTimeoutSecs(120);

		TwitterSpout twitterSpout = new TwitterSpout(
				"RIfmhqAGTq9eTSl6gNVFlFRMp",
				"1RaxB5Ga5d9FeXdlyv7vrzRVhbfmdUFqWnapPJk5wAFEz5GG92",
				"438695350-bfUujSZqX8Cjqgrj72dcvW7XyWPqcz5ABLrTLWc3",
				"kFaNTonuunKTaCFz88zuxn0QEIjZiW6CFOzAR1MmS1V5n");
		
		TopologyBuilder b = new TopologyBuilder();
		b.setSpout("TwitterSpout", twitterSpout, 1);
		b.setBolt("PreprocessingBolt", new PreprocessingBolt(), 1).shuffleGrouping("TwitterSpout");
		// b.setBolt("FileWriterBolt", new FileWriterBolt("tweets.csv"), 1).globalGrouping("PreprocessingBolt");
		b.setBolt("ClassificationBolt", new ClassificationBolt(), 1).globalGrouping("PreprocessingBolt");
		
		final LocalCluster cluster = new LocalCluster();
		cluster.submitTopology(TOPOLOGY_NAME, conf, b.createTopology());

		Runtime.getRuntime().addShutdownHook(new Thread() {
			@Override
			public void run() {
				cluster.killTopology(TOPOLOGY_NAME);
				cluster.shutdown();
			}
		});
	}
	
}