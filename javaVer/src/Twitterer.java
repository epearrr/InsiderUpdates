package javaVer.src;

import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterFactory;
import twitter4j.TwitterException;
import twitter4j.DirectMessage;

import java.io.IOException;
import java.io.PrintStream;

import java.util.ArrayList;
import java.util.List;

public class Twitterer
   {
      private Twitter twitter;
      private PrintStream consolePrint;
      private List<Status> statuses;

     
      public Twitterer(PrintStream console)
      {
         // Makes an instance of Twitter - this is re-useable and thread safe.
         // Connects to Twitter and performs authorizations.
         twitter = TwitterFactory.getSingleton(); 
         consolePrint = console;
         statuses = new ArrayList<Status>();
      }
   
     /** 
      * This method tweets a given message.
      * @param String  a message you wish to Tweet out
      */
      public void tweetOut(String message) throws TwitterException, IOException
      {
         Status status = twitter.updateStatus(message);
      }   

      /** 
       * @return every DM as a list of DirectMessage objects
      */
      public List<DirectMessage> readDms() throws TwitterException{
         return twitter.getDirectMessages();
      }
   }  
