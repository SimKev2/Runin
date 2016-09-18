import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {


    public static void main(String[] args) {
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
        ArrayList<Event> events =  p.buildEventList(DateUtil.getListOfDates(currentDate, endDate));

        JSONEventBuilder builder = new JSONEventBuilder(events, DateUtil.getDateString(currentDate), DateUtil.getDateString(endDate));

        String jsonString = builder.createJSON();
        System.out.println(jsonString);


        /*
        for(int i=0; i<events.size(); i++){
            System.out.println(" Name: " + events.get(i).getName() + " Date: " + events.get(i).getDate() + " Distance: " + events.get(i).getDistance());
        }
        */
    }
}
