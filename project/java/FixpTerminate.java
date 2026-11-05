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
  Releases the session from its transport without ending the session, which can be bound again later. The peer answers with a Terminate, and after its own Terminate a party sends nothing more.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpTerminate extends FixpMessage {

  private String sessionId;
  private String terminationCode;
  private String reasonText;


}