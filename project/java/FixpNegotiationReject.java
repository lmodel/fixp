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
  A server's refusal to create a session. The server sends nothing more and closes the transport.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpNegotiationReject extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private String negotiationRejectCode;
  private String reasonText;


}