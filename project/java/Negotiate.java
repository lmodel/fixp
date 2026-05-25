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
  FIXP session message 'Negotiate'.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Negotiate extends FixpSessionMessage {

  private String sessionId;
  private String timestamp;
  private String clientFlow;
  private String credentials;


}