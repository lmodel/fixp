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
  On a transport that several sessions share, names the session the following messages belong to and, when the flow is sequenced, where its numbering continues.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpContext extends FixpMessage {

  private String sessionId;
  private Integer nextSeqNo;


}