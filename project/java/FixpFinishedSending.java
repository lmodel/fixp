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
  Says that the sender's flow has carried its last application message, which begins finalization. It is repeated as the heartbeat until the answer comes.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpFinishedSending extends FixpMessage {

  private String sessionId;
  private Integer lastSeqNo;


}