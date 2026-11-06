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
  A multicast publisher's notice that starts a flow and ties the session's short-lived identifier to a lasting subject. It is repeated so that late listeners can join.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpTopic extends FixpMessage {

  private String sessionId;
  private String flow;
  private Integer keepaliveInterval;
  private String topicClassification;


}