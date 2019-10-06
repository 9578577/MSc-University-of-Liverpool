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
import java.io.Serializable;
import java.util.Map;
import twitter4j.*;
import twitter4j.GeoLocation;

// This Bolt is modified from Connors "TwitterGeoBolt"
public class LocationExtractionBolt extends BaseRichBolt {
	private static final long serialVersionUID = 101;
	OutputCollector collector;

	PrintWriter writer;
    private String filename;

    public LocationExtractionBolt(String filename){
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
        Status status = (Status) tuple.getValue(0);
        GeoLocation g = status.getGeoLocation();

        if(g != null) {
            // Pull longitude and latitude
            Double latitude = g.getLatitude();
            Double longitude = g.getLongitude();

            // Write geolocation to CSV
            StringBuilder sb = new StringBuilder();
            sb.append(longitude);
            sb.append(",");
            sb.append(latitude);
            sb.append("\n");
            writer.write(sb.toString());
            writer.flush();

            System.out.println("Location recorded");
        } else {
            System.out.println("No Geolocation attached to tweet");
        }
	}

	@Override 
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}

	@Override
    public void cleanup() {
        writer.close();
    }
}