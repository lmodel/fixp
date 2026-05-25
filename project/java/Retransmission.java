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
  FIXP session message 'Retransmission'.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Retransmission extends FixpSessionMessage {

  private String sessionId;
  private String requestTimestamp;
  private String nextSeqNo;
  private String count;


}