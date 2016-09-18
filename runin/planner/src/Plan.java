import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

/**
 * Created by davidgarner on 9/17/16.
 */
public class Plan {
    public static void main(String[] args) {
        Plan p = new Plan();
        p.populateEvents(5,30);

    }

    String user;
    String targetDistance;
    ArrayList<Double> distanceList = new ArrayList<>();

    double L = 0;
    double k = 0;
    int x = 0;

    public Plan(){

    }

    public ArrayList<Double> populateEvents(double endDistance, long numDays){
        L = endDistance + 3;
        k = 0.095;
        x = 8;

        for(int i = 0; i < numDays; i++) {
            double value = L / (1 + Math.exp(-1 * k * (i - x)));
            distanceList.add(0.5*Math.round(value/0.5));
        }

        return  distanceList;
    }

    public ArrayList<Event> buildEventList(ArrayList<LocalDate> dates, LocalDate endDate){
        ArrayList<Event> events = new ArrayList<>();

        for(int i=0; i < dates.size() - 1; i += 2){
            if(dates.get(i).isBefore(endDate)){
                String name = "Run " + distanceList.get(i) + " miles today.";
                String date = DateUtil.getDateString(dates.get(i));
                events.add(new Event(name, date, distanceList.get(i).toString()));
            }

        }

        //System.out.println(events.toString());

        return events;
    }
}
