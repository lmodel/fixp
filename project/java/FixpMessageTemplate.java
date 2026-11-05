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
  Hands the peer a template or schema it needs to read messages in an encoding that templates drive. There is no fixed moment for sending it.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpMessageTemplate extends FixpMessage {

  private Integer sofhEncodingType;
  private Integer effectiveTime;
  private String templateVersion;
  private String template;


}