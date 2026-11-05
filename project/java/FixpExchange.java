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
  The messages of one session in the order they were sent, as a test case, a worked example or a captured log.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpExchange  {

  private URI id;
  private String description;
  private String sessionKind;
  private Boolean multiplexed;
  private List<FixpExchangeStep> exchangeSteps;


}