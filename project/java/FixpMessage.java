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
  One FIXP message, as its fields would be read from the wire before or after encoding.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class FixpMessage  {

  private String messageKind;


}