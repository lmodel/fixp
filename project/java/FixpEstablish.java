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
  A client's request to tie a negotiated session to the very transport this message arrives on. After a disconnection it is sent again to re-bind.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpEstablish extends FixpMessage {

  private String sessionId;
  private Integer requestTime;
  private Integer keepaliveInterval;
  private Integer nextSeqNo;
  private String credentials;


}