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
  A client's request to create a session under an identifier it has never used, stating the flow type it will send.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpNegotiate extends FixpMessage {

  private String sessionId;
  private Integer requestTime;
  private String clientFlow;
  private String credentials;


}