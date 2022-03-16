package src;

import twitter4j.TwitterException;
import twitter4j.DirectMessage;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.PrintWriter;

   public class TwitterDriver {
      private static PrintStream consolePrint;
   
      public static void main (String []args) throws TwitterException, IOException, InterruptedException {
         // Create twtBot object to work with API
         Twitterer twtBot = new Twitterer(consolePrint);

         while(true){
            // reads all DMs in twitter account and saves them in variable directMessageList
            List<DirectMessage> directMessageList = twtBot.readDms();

            // saves the id of the most recent dm
            DirectMessage recentDm = directMessageList.get(0);
            long recentDmId = recentDm.getId();
            
            // if a new DM is found, display the dm + run the command given by the user
            if (recentDmId != checkLastDmId()){
               System.out.println("New DM Found! Here's what it said:");
               System.out.println(recentDm.getText());

               // 
               readStockCommand(recentDm.getText());

               storeLastDmId(recentDmId);

               // i
            }
            else System.out.println("No new DM was found.");

            // sleep for n seconds
            sleep(30);
         }
      }

      /**
       * stores the ID of the most recent DM in storedDms.txt
       * @param dmId the ID of the DM to be stored
       * @throws IOException
       */
      public static void storeLastDmId(long dmId) throws IOException {
         PrintWriter pw = new PrintWriter("src/storedDms.txt");
         pw.println(dmId);
         pw.close();
      }

      /**
       * @return id of the most recent DM
       * @throws IOException
       */
      public static long checkLastDmId() throws IOException {
         Scanner fileScan = new Scanner(new File("src/storedDms.txt"));
         long id = fileScan.nextLong();
         fileScan.close();
         return id;
      }
      
      /**
       * Reads the stock command given to the bot through DMs. 
       * @param recentDmText the message the user sent to the bot
       */
      public static void readStockCommand(String recentDmText){
         String[] command = recentDmText.split(" ");
         // after command is split, try to assign values to action, numShares, and ticker. If there is an index out of bounds
         // error, then the user likely formatted the request to the bot wrong
         try{
            String action = command[0];
            int numShares = Integer.parseInt(command[1]);
            String ticker = command[2];
            System.out.printf("Action: %s Shares: %d Ticker: %s", action, numShares, ticker);
         } 
         catch(Exception ArrayIndexOutOfBoundsException){
            System.out.println("Out of bounds error -- make sure your DM to the bot is formatted correctly!");
         }
      }

      /**
       * pauses the program for <sec> seconds
       * @param sec number of seconds to pause for
       * @throws InterruptedException
       */
      public static void sleep(double sec) throws InterruptedException {
         Thread.sleep((long)(sec * 1000));
      }

   }    
   