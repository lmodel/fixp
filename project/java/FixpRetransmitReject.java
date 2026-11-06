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
  Refuses a RetransmitRequest, with a code saying why.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpRetransmitReject extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private String retransmitRejectCode;
  private String reasonText;


}