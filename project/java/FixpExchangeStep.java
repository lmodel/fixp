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
  One step: a FIXP message, or a run of application messages whose content FIXP does not define, and the side that sent it.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpExchangeStep  {

  private String sentBy;
  private FixpMessage fixpMessage;
  private Integer applicationMessageCount;


}