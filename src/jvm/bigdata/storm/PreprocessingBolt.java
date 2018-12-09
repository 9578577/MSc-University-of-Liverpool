package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import java.util.Map;
import twitter4j.*;

public class PreprocessingBolt extends BaseRichBolt {
	private static final long serialVersionUID = 99;

	OutputCollector collector;

	@Override
	public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
		collector = outputCollector;
	}
	
	@Override
	public void execute(Tuple tuple) {
		Status status = (Status) tuple.getValue(0);
		String tweet = status.getText();
		
		tweet = tweet.trim().replaceAll(" +", " "); // Replace multiple spaces
		tweet = tweet.replaceAll("[\r\n]+", " "); // Replace new lines
		tweet = tweet.replace(",", ""); // Remove commas so CSV file writes correctly
		tweet = tweet.replace("\"", ""); // Remove speech marks

		collector.emit(new Values(tweet));
	}
	
	@Override 
	public void declareOutputFields(OutputFieldsDeclarer declarer) { 
		declarer.declare(new Fields("tweet"));
	}
	
}