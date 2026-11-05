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
  What two counterparties agree on for one FIXP service, layer by layer, for the client and for the server.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpRulesOfEngagement  {

  private URI id;
  private String description;
  private FixpStackProfile clientStack;
  private FixpStackProfile serverStack;


}