import java.time.LocalDate;


/**
 * Created by davidgarner on 9/16/16.
 */
public class DateUtil {

    public static long getDaysBetween(LocalDate startDate, LocalDate endDate) {
        long days = java.time.temporal.ChronoUnit.DAYS.between(startDate, endDate);
        return days;
    }

    public static LocalDate parseDateFromString(String date){
        int month = Integer.parseInt(date.substring(0, 2));
        int day = Integer.parseInt(date.substring(3,5));
        int year = Integer.parseInt(date.substring(6,8));
        year += 2000;

        LocalDate newDate = LocalDate.of(year, month, day);
        return newDate;
    }
}
