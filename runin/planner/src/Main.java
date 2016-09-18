import java.io.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {


    public static void main(String[] args) throws IOException {
        String eventDate;
        double eventDistance;
        long numDays;

        Scanner in = new Scanner(System.in);

        System.out.println("Enter an Event Date(MM/DD/YY): ");
        eventDate = in.next();

        System.out.println("Enter the event Distance in miles: ");
        eventDistance = in.nextInt();


        System.out.println("Your " + eventDistance + " event is scheduled for " + eventDate + ".");

        LocalDate endDate = DateUtil.parseDateFromString(eventDate);
        LocalDate currentDate = LocalDate.now();

        numDays = DateUtil.getDaysBetween(currentDate, endDate);


        Plan p = new Plan();
        p.populateEvents(eventDistance, numDays );
        ArrayList<Event> events =  p.buildEventList(DateUtil.getListOfDates(currentDate, endDate),endDate);

        JSONEventBuilder builder = new JSONEventBuilder(events, DateUtil.getDateString(currentDate), DateUtil.getDateString(endDate));

        String jsonString = builder.createJSON();
        //System.out.println(jsonString);

        String directory = System.getProperty("user.home");

        PrintWriter writer = new PrintWriter(directory + "/Documents/Hackathon/Runin/runin/plan.json", "UTF-8");
        writer.println(jsonString);
        writer.close();

       String userDirectory = System.getProperty("user.dir");

        String[] cmd = {
                "/bin/bash",
                "-c",
                "source /Users/davidgarner/Documents/Hackathon/venv/bin/activate: python /Users/davidgarner/Documents/Hackathon/Runin/runin/processing.py"
        };




        /*
        for(int i=0; i<events.size(); i++){
            System.out.println(" Name: " + events.get(i).getName() + " Date: " + events.get(i).getDate() + " Distance: " + events.get(i).getDistance());
        }
        */
    }
}
