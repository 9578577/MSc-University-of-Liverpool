package bigdata.storm;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import java.util.Map;
import java.util.ArrayList;
import java.io.*;
import org.json.*;

public class ClassificationBolt extends BaseRichBolt {
	OutputCollector collector;

    @Override
    public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
        collector = outputCollector;
    }

    // ReadAll function from https://en.proft.me/2013/12/5/how-parse-json-java/
    // Allows us to take the JSON input from the flask server
    public static String readAll(Reader rd) throws IOException {
        StringBuilder sb = new StringBuilder();
        int cp;
        while ((cp = rd.read()) != -1) {
            sb.append((char) cp);
        }
        return sb.toString();
    }

    @Override
    public void execute(Tuple tuple) {
        String tweet = tuple.getString(0);

        String s = null;
        String jsonText = null;
        JSONObject obj = null;

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

            // Read JSON response from server
            jsonText = readAll(stdInput);
            if (jsonText != null) { // Make sure the reponse isn't null
                obj = new JSONObject(jsonText); // Set the response equal to a JSON object
                JSONObject res = obj.getJSONObject("results"); // Extract results object from response
                int error = res.getInt("Error"); // Pull the error code from the response
    
                // If there is an error, output the error message
                // TO DO: Emit the error code to the Tally bolt
                if(error > 0) {
                    System.out.println("[ERROR] " + res.getString("errMessage"));
                
                // If there is no error, pull the data from the JSON object
                // These are then emitted to the Tally bolt for counting
                } else {
                    System.out.println("[SUCCESS] " + res.getString("ClassifiedTweet"));
                    String language = res.getString("Language");
                    int retweet = res.getInt("Retweet");
                    int candidate = res.getInt("Candidate");
                    int sentiment = res.getInt("Sentiment");
                    collector.emit(new Values(language, retweet, candidate, sentiment));
                }
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
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("language", "retweet", "candidate", "sentiment"));
    }
}