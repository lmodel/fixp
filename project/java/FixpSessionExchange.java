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
  Top-level container for a FIXP session exchange - holds an ordered list of session messages plus optional metadata.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpSessionExchange  {

  private List<FixpSessionMessage> messages;
  private String title;
  private String creator;
  private String publisher;
  private String rights;
  private String date;


}