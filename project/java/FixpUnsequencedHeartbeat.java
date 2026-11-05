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
  Shows the peer that the session and transport are alive when the sender's flow is unsequenced or empty. It has no fields.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpUnsequencedHeartbeat extends FixpMessage {



}