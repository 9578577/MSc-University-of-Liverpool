package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Map;

public class FileWriterBolt extends BaseRichBolt {
    private static final long serialVersionUID = 109;
    OutputCollector collector;
	
    PrintWriter writer;
    private String filename;

    public FileWriterBolt(String filename){
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
        String tweet = tuple.getString(0);
        StringBuilder sb = new StringBuilder();
        sb.append(tweet);
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