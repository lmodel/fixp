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
  Asks the peer to resend some messages of its recoverable flow. A party has at most one such request open at a time.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpRetransmitRequest extends FixpMessage {

  private String sessionId;
  private Integer requestTime;
  private Integer fromSeqNo;
  private Integer messageCount;


}