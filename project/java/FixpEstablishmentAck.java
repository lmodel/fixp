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
  A server's acceptance of the binding. From here, application messages may flow.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpEstablishmentAck extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private Integer keepaliveInterval;
  private Integer nextSeqNo;


}