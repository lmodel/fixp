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
  One side's choices at each layer of the stack: application, presentation, session, security and transport.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class FixpStackProfile  {

  private Boolean applicationRecovery;
  private String applicationFixVersion;
  private String servicePack;
  private List<String> extensionPacks;
  private String messageEncoding;
  private String encodingVersion;
  private List<String> messageSchemas;
  private String framing;
  private List<String> supportedFlowTypes;
  private Integer shortestKeepaliveInterval;
  private Integer longestKeepaliveInterval;
  private Integer retransmissionLimit;
  private String tlsVersion;
  private List<String> authenticationMethods;
  private String credentialsFormat;
  private List<String> cipherSuites;
  private List<String> transports;
  private List<String> networkProtocols;


}