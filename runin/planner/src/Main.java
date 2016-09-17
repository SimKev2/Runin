import java.time.LocalDate;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        String eventDate;
        double eventDistance;

        Scanner in = new Scanner(System.in);

        System.out.println("Enter an Event Date(Y/M/D): ");
        eventDate = in.next();

        System.out.println("Enter the event Distance in miles: ");
        eventDistance = in.nextInt();


        System.out.println("Your " + eventDistance + " event is scheduled for " + eventDate + ".");

        LocalDate endDate = DateUtil.parseDateFromString(eventDate);
        LocalDate currentDate = LocalDate.now();

        long days = DateUtil.getDaysBetween(currentDate, endDate);

        System.out.println("Days: "  + days);

    }
}
