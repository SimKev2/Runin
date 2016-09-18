/**
 * Created by davidgarner on 9/17/16.
 */
public class Event {
    String name;
    String date;
    String distance;

    public Event(String name, String date, String distance){
        this.name = name;
        this.date = date;
        this.distance = distance;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getDistance() {
        return distance;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }
}
