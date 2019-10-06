// Modified from Apache Hadoops 'Wordcount Example'
// Wordcount Ex. Source: http://hadoop.apache.org/docs/r2.5.2/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;


public class csv_BigramWordCount {
  public static class TokenizerMapper extends Mapper<Text, Text, Text, IntWritable>{
    public final IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
      // Tokenise "values" ready for mapping
      StringTokenizer itr = new StringTokenizer(value.toString());

      String previous = null;
      while(itr.hasMoreTokens()) {
        // Set current token
        String current = itr.nextToken();

        // Check that we have a bigram (i.e. a previous and current token)
        if (previous != null) {
          // Output "DOI : Bigram"
          word.set(key + ":" + previous + " " + current);
          context.write(word, one);
        }
        previous = current;
      }
    }
  }

  public static class IntSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values,  Context context) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    conf.set("mapreduce.input.keyvaluelinerecordreader.key.value.separator", ","); // Separate CSV into key : value
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(csv_BigramWordCount.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setInputFormatClass(KeyValueTextInputFormat.class); // To handle Key : Value pairs
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
