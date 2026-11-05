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
  Introduces a batch of resent messages, which are numbered by counting from the number it gives. A request may be answered in several batches.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpRetransmission extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private Integer nextSeqNo;
  private Integer messageCount;


}