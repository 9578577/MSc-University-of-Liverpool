package bigdata.storm;

import backtype.storm.Config;
import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;
import backtype.storm.utils.Utils;
import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;
import java.util.Map;
import java.util.concurrent.LinkedBlockingQueue;

@SuppressWarnings({ "rawtypes", "serial" })
public class TwitterSpout extends BaseRichSpout {
	
    // Oauth credentials
	private final String consumerKey, consumerSecret;
	private final String accessKey, accessSecret;

    // Storm4j settings
	private SpoutOutputCollector collector;
	private TwitterStream twitterStream;
	private LinkedBlockingQueue<Status> queue = null;
	
	/*
	 *  
	 */
	public TwitterSpout(String conKey, String conSecret, String accKey, String accSecret) 
	{
		if (conKey == null || conSecret == null || accKey == null || accSecret == null) {
			throw new RuntimeException("Please set OAuth details in Topology");
		}
		
		consumerKey = conKey;
		consumerSecret = conSecret;
		accessKey = accKey;
		accessSecret = accSecret;
	}

    /*
     *
     */
    private class TweetListener implements StatusListener {
        @Override
        public void onStatus(Status status) {
            queue.offer(status);
        }

        @Override
        public void onDeletionNotice(StatusDeletionNotice sdn) {
        }

        @Override
        public void onTrackLimitationNotice(int i) {
        }

        @Override
        public void onScrubGeo(long l, long l1) {
        }

        @Override
        public void onStallWarning(StallWarning stallWarning) {
        }

        @Override
        public void onException(Exception e) {
            e.printStackTrace();
        }
    }
	
	@Override
	public void open(Map conf, TopologyContext context, SpoutOutputCollector spoutOutputCollector) {
		queue = new LinkedBlockingQueue<Status>(1000);
		collector = spoutOutputCollector;

		// Initiate configuration builder
        ConfigurationBuilder cb = new ConfigurationBuilder();
		// Set the authentication credentials that were provided in the StormTopology class
        cb.setDebugEnabled(true)
                .setOAuthConsumerKey(consumerKey)
                .setOAuthConsumerSecret(consumerSecret)
                .setOAuthAccessToken(accessKey)
                .setOAuthAccessTokenSecret(accessSecret);
		
		TwitterStreamFactory factory = new TwitterStreamFactory(cb.build());
		twitterStream = factory.getInstance();

		// Initiate listener
		twitterStream.addListener(new TweetListener());

		// Set up filters
		FilterQuery twitterFilter = new FilterQuery();
		String[] keywordsArray = {
			"سيف الإسلام القذافي", "القذافي", "خليفة حفتر", "حفتر",
			"Saif al-Islam Gaddafi", "Saif Gaddafi", "Gaddafi", "Khalifa Haftar", "Haftar"
		};
		twitterFilter.track(keywordsArray); // Filter for key words defined above
		twitterFilter.language(new String[]{"en, ar"}); // Search for English and Arabic tweets

		// Initiate filter
		twitterStream.filter(twitterFilter);
	}

	@Override
	public void nextTuple() {
		Status ret = queue.poll();
		
		if (ret == null) {
			Utils.sleep(50);
            return;
		}
		
        collector.emit(new Values(ret));
	}

	@Override
	public void close() {
		twitterStream.shutdown();
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		Config ret = new Config();
		ret.setMaxTaskParallelism(1);
		return ret;
	}

	@Override
	public void ack(Object id) {
	}

	@Override
	public void fail(Object id) {
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("tweet"));
	}
}