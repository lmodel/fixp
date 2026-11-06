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
  An optional application message telling the party that sends an idempotent flow which of its operations took effect, where no business message already says so.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpApplied extends FixpMessage {

  private Integer fromSeqNo;
  private Integer messageCount;


}