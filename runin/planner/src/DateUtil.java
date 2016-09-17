import java.lang.reflect.Array;
import java.time.LocalDate;
import java.util.ArrayList;


/**
 * Created by davidgarner on 9/16/16.
 */
public class DateUtil {

    final int daysInMonth [] = {31,28,31,30,31,30,31,31,30,31,30,31};

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

    public static ArrayList<LocalDate> getListOfDates(LocalDate startDate, LocalDate endDate){
        ArrayList<LocalDate> dates = new ArrayList<LocalDate>();
        LocalDate mStartDate = startDate;

        while(mStartDate.isBefore(endDate)){
            mStartDate = mStartDate.plusDays(1);
            dates.add(mStartDate.plusDays(1));
        }
        return  dates;
    }
}
