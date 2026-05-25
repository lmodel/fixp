package None;

/* metamodel_version: 1.11.0 */
/* version: FIX.5.0SP2 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  Variable length data, also know as octect string
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeObjectComposite  {

  private Integer length;
  private Integer varData;


}