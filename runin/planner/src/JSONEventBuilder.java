import java.time.LocalDate;
import java.util.ArrayList;

/**
 * Created by davidgarner on 9/17/16.
 */
public class JSONEventBuilder {

    public static void main(String[] args) {
        /*
        JSONEventBuilder builder = new JSONEventBuilder("David", "3/15/16", "5");
        builder.addFieldToJSONString("name", "david");
        builder.addFieldToJSONString("description", "this is a description");
        System.out.println(builder.getJSONString());
        */
    }

    String jsonString = "";
    String eventString = "";
    String startDate = "";
    String endDate = "";

    ArrayList<Event> events = new ArrayList<>();

    public JSONEventBuilder(ArrayList<Event> events, String startDate, String endDate){
        this.events = events;
        this.startDate = startDate;
        this.endDate = endDate;
    }

    private void addFieldToJSONString(String key, String value){
        if(key.equals("name"))
            eventString = eventString + '\"' + key + '\"' + ":" + '\"' + value + '\"';
        else if(key.equals("distance"))
            eventString =  eventString + ","+ '\"' + key + '\"' + ":" + value;
        else
            eventString =  eventString + ","+ '\"' + key + '\"' + ":" + '\"' + value +  '\"';

    }

    public String createJSON(){
        for(int i=0; i<events.size(); i++){
            eventString = eventString + "{";
            addFieldToJSONString("name", events.get(i).getName());
            addFieldToJSONString("date", events.get(i).getDate());
            addFieldToJSONString("distance", events.get(i).getDistance());
            eventString = eventString + "},";
        }
        eventString = eventString.substring(0, eventString.lastIndexOf(','));


        jsonString = "\"events\": [" + eventString + "]";
        jsonString = "\"startDate\":" + '\"' + startDate  + '\"' +  ", \"endDate\":"  + '\"' + endDate  + '\"' + "," + jsonString;

        return "{" + jsonString + "}";
    }

    public String getJSONString(){
        jsonString = "{" + jsonString + "}";
        return jsonString;
    }
}
