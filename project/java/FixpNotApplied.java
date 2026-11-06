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
  An application message telling the party that sends an idempotent flow about a gap: a run of operations that did not take effect. That party's application decides what to do.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpNotApplied extends FixpMessage {

  private Integer fromSeqNo;
  private Integer messageCount;


}