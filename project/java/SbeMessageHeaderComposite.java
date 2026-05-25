package None;

/* metamodel_version: 1.11.0 */
/* version: FIX.5.0SP2 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  Message identifiers and length of message root
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeMessageHeaderComposite  {

  private Integer blockLength;
  private Integer templateId;
  private Integer schemaId;
  private Integer schemaVersion;


}