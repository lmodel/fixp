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
  FIXP session message 'Establish'.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Establish extends FixpSessionMessage {

  private String sessionId;
  private String timestamp;
  private String keepaliveInterval;
  private String nextSeqNo;
  private String credentials;


}