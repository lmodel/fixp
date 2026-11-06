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
  A server's refusal of the binding.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpEstablishmentReject extends FixpMessage {

  private String sessionId;
  private Integer requestTimestamp;
  private String establishmentRejectCode;
  private String reasonText;


}