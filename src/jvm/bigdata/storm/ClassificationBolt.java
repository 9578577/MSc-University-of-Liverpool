package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;
import java.util.Map;
import java.io.*;


public class ClassificationBolt extends BaseRichBolt {
	OutputCollector collector;

    @Override
    public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
        collector = outputCollector;
    }

    @Override
    public void execute(Tuple tuple) {
        String tweet = tuple.getString(0);

        String s = null;

        // Call Python script to connect to the flask server
        try {
            System.out.println("Attempting to send tweet to flask server..");

            // Define command to execute when calling Python script
            String[] cmd = {
                "python",
                "/vagrant/BigDataAssignment/src/flask/flaskRequest.py",
                tweet
            };

            // Setup a process to execute the command and receive values returned from server
            Process p = Runtime.getRuntime().exec(cmd);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));

            // Print the output before sending to ?? bolt
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);
            }
            
            // Print the error
            while ((s = stdError.readLine()) != null) {
                System.out.println("[ERROR] " + s);
            }
        } catch(IOException e) {
            System.out.println("[ERROR] " + e);
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
    }
}