package example;

/* metamodel_version: 1.12.0 */
/* version: 1.0 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  A server's acceptance of a new session, stating the flow type it will send back.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpNegotiationResponse extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private String serverFlow;
  private String credentials;


}