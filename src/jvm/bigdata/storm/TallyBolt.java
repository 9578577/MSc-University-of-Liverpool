package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import java.util.Map;

public class TallyBolt extends BaseRichBolt {
	private static final long serialVersionUID = 101;

	OutputCollector collector;

	@Override
	public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
		collector = outputCollector;
	}
	
	@Override
	public void execute(Tuple tuple) {
		String lang = tuple.getStringByField("language");
		System.out.println("lang");
		
	}

	@Override 
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}
}