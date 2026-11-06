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
  Starts the numbering of a sequenced flow, so that the application messages after it are numbered by counting up from the value it carries. Sent when idle, it is also the heartbeat.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpSequence extends FixpMessage {

  private Integer nextSeqNo;


}