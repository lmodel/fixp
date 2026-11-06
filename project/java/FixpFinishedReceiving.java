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
  Answers FinishedSending once the last message of the peer's flow has been processed. After it the session is finalized and its identifier is spent.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpFinishedReceiving extends FixpMessage {

  private String sessionId;


}