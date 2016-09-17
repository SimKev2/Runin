/**
 * Created by davidgarner on 9/17/16.
 */
public class JSONEventBuilder {

    public static void main(String[] args) {
        JSONEventBuilder builder = new JSONEventBuilder();
        builder.addFieldToJSONString("name", "david");
        builder.addFieldToJSONString("description", "this is a description");
        System.out.println(builder.getJSONString());
    }

    String jsonString = "";

    public JSONEventBuilder(){
        jsonString = "";
    }

    public void addFieldToJSONString(String key, String value){
        if(jsonString.equals(""))
            jsonString = jsonString + key + ":" + value;
        else
            jsonString = jsonString + "," + key + ":" + value;
    }

    public String getJSONString(){
        jsonString = "{" + jsonString + "}";
        return jsonString;
    }
}
