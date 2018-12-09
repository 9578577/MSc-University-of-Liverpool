package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Map;

public class TallyWriterBolt extends BaseRichBolt {
	private static final long serialVersionUID = 101;
	OutputCollector collector;

	PrintWriter writer;
    private String filename;

    public TallyWriterBolt(String filename){
        this.filename = filename;
    }

	@Override
	public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
		collector = outputCollector;
		try {
            writer = new PrintWriter(filename, "UTF-8");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
	}
	
	@Override
	public void execute(Tuple tuple) {
		// Pull fields from tuple
		String language = tuple.getStringByField("language");
		int retweet = tuple.getIntegerByField("retweet");
		int candidate = tuple.getIntegerByField("candidate");
		int sentiment = tuple.getIntegerByField("sentiment");

		// Variables to hold tally data
		int gaddafiCount = 0;
		int haftarCount = 0;
		int gadaffiSentiment = 0;
		int haftarSentiment = 0;
		int englishTweet = 0;
		int arabicTweet = 0;

		// Determine candidate and increment the count variable
		// Also add the sentiment to the respective sentiment variable
		if(candidate == 0) {
			gaddafiCount += 1;
			gadaffiSentiment += sentiment;
		} else {
			haftarCount += 1;
			haftarSentiment += sentiment;
		}
		
		// Determine language and increment the variable
		if(language == "en") {
			englishTweet += 1;
		} else {
			arabicTweet += 1;
		}

		StringBuilder sb = new StringBuilder();
		sb.append(gaddafiCount);
		sb.append(",");
		sb.append(haftarCount);
		sb.append(",");
		sb.append(gadaffiSentiment);
		sb.append(",");
		sb.append(haftarSentiment);
		sb.append(",");
		sb.append(englishTweet);
		sb.append(",");
		sb.append(arabicTweet);
		sb.append(",");
		sb.append(retweet);
		sb.append("\n");

		writer.write(sb.toString());
        writer.flush();
	}

	@Override 
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}

	@Override
    public void cleanup() {
        writer.close();
    }
}