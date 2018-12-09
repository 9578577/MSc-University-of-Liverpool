package bigdata.storm;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.topology.TopologyBuilder;

public class StormTopology {
	
	static final String TOPOLOGY_NAME = "storm-twitter-analysis";
	
	public static void main(String[] args) throws Exception {
		
		Config conf = new Config(); // Instantiate Config
		conf.setMessageTimeoutSecs(120);
		conf.setMaxTaskParallelism(1); // Use one thread		

		// Instantiate the TwitterSpout class
		TwitterSpout twitterSpout = new TwitterSpout(
				"RIfmhqAGTq9eTSl6gNVFlFRMp",
				"1RaxB5Ga5d9FeXdlyv7vrzRVhbfmdUFqWnapPJk5wAFEz5GG92",
				"438695350-bfUujSZqX8Cjqgrj72dcvW7XyWPqcz5ABLrTLWc3",
				"kFaNTonuunKTaCFz88zuxn0QEIjZiW6CFOzAR1MmS1V5n");
		
		TopologyBuilder b = new TopologyBuilder();

		// Twitter Spout
		b.setSpout("TwitterSpout", twitterSpout, 1);

		// Preprocessing Bolt
		b.setBolt("PreprocessingBolt", new PreprocessingBolt(), 1).shuffleGrouping("TwitterSpout");

		// Location Extraction Bolt - Extract the location of the tweet and write this to a CSV
		b.setBolt("LocationExtractionBolt", new LocationExtractionBolt("location.csv"), 1).globalGrouping("TwitterSpout");

		// File Writer Bolt - Only enabled when the Flask server isn't active
		// b.setBolt("FileWriterBolt", new FileWriterBolt("tweets.csv"), 1).globalGrouping("PreprocessingBolt");

		// Classification Bolt - Sends tweet to Flask server for classification/sentiment 
		b.setBolt("ClassificationBolt", new ClassificationBolt(), 1).globalGrouping("PreprocessingBolt");

		// Tally Writer Bolts - Writes the JSON output to a CSV file for postprocessing
		b.setBolt("TallyWriterBolt", new TallyWriterBolt("tally.csv"), 1).globalGrouping("ClassificationBolt");
		
		// Launch cluster in local mode
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