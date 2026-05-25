# Auto generated from fixp.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-05-26T00:41:04
# Schema: fixp
#
# id: https://w3id.org/lmodel/fixp
# description: LinkML schema for the FIX Performance (FIXP) Session Protocol, auto-generated from the upstream specification artifacts (FixRepositoryForFIXP.xml, SBEschemaForFIXP.xml, OrchestraForFIXP.xml).
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date, Datetime, Float, Integer, String
from linkml_runtime.utils.metamodelcore import XSDDate, XSDDateTime

metamodel_version = "1.11.0"
version = "FIX.5.0SP2"

# Namespaces
COMMON_DOMAIN_MODEL = CurieNamespace('common_domain_model', 'https://w3id.org/lmodel/common-domain-model/elements/')
DC = CurieNamespace('dc', 'http://purl.org/dc/elements/1.1/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FIX_ORCHESTRA = CurieNamespace('fix_orchestra', 'https://w3id.org/lmodel/fix-orchestra/elements/')
FIX_SBE = CurieNamespace('fix_sbe', 'https://w3id.org/lmodel/fix-sbe/elements/')
FIXP = CurieNamespace('fixp', 'https://w3id.org/lmodel/fixp/')
FIXR = CurieNamespace('fixr', 'http://fixprotocol.io/2020/orchestra/repository/')
FLUXNOVA_BPM_PLATFORM = CurieNamespace('fluxnova_bpm_platform', 'https://w3id.org/lmodel/fluxnova-bpm-platform/elements/')
GIST_LINKML = CurieNamespace('gist_linkml', 'https://w3id.org/lmodel/gist/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SBE = CurieNamespace('sbe', 'http://fixprotocol.io/2016/sbe/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = FIXP


# Types
class FIXInt(Integer):
    """ FIX int base datatype. Sequence of digits without commas or decimals and optional sign character (ASCII characters "-" and "0" - "9" ). The sign character utilizes one byte (i.e. positive int is "99999" while negative int is "-99999"). Note that int values may contain leading zeros (e.g. "00023" = "23"). Example: 723 in field 21 would be mapped int as |21=723|. -723 in field 12 would be mapped int as |12=-723|. """
    type_class_uri = FIXP["FIXInt"]
    type_class_curie = "fixp:FIXInt"
    type_name = "FIXInt"
    type_model_uri = FIXP.FIXInt


class FIXLength(Integer):
    """ FIX Length datatype (extends int). int field representing the length in bytes. Value must be positive. """
    type_class_uri = FIXP["FIXLength"]
    type_class_curie = "fixp:FIXLength"
    type_name = "FIXLength"
    type_model_uri = FIXP.FIXLength


class FIXTagNum(Integer):
    """ FIX TagNum datatype (extends int). int field representing a field's tag number when using FIX "Tag=Value" syntax. Value must be positive and may not contain leading zeros. """
    type_class_uri = FIXP["FIXTagNum"]
    type_class_curie = "fixp:FIXTagNum"
    type_name = "FIXTagNum"
    type_model_uri = FIXP.FIXTagNum


class FIXSeqNum(Integer):
    """ FIX SeqNum datatype (extends int). int field representing a message sequence number. Value must be positive. """
    type_class_uri = FIXP["FIXSeqNum"]
    type_class_curie = "fixp:FIXSeqNum"
    type_name = "FIXSeqNum"
    type_model_uri = FIXP.FIXSeqNum


class FIXNumInGroup(String):
    """ FIX NumInGroup datatype (extends int). int field representing the number of entries in a repeating group. Value must be positive. """
    type_class_uri = FIXP["FIXNumInGroup"]
    type_class_curie = "fixp:FIXNumInGroup"
    type_name = "FIXNumInGroup"
    type_model_uri = FIXP.FIXNumInGroup


class FIXDayOfMonth(String):
    """ FIX DayOfMonth datatype (extends int). int field representing a day during a particular monthy (values 1 to 31). """
    type_class_uri = FIXP["FIXDayOfMonth"]
    type_class_curie = "fixp:FIXDayOfMonth"
    type_name = "FIXDayOfMonth"
    type_model_uri = FIXP.FIXDayOfMonth


class FIXFloat(Float):
    """ FIX float base datatype. Sequence of digits with optional decimal point and sign character (ASCII characters "-", "0" - "9" and "."); the absence of the decimal point within the string will be interpreted as the float representation of an integer value. All float fields must accommodate up to fifteen significant digits. The number of decimal places used should be a factor of business/market needs and mutual agreement between counterparties. Note that float values may contain leading zeros (e.g. "00023.23" = "23.23") and may contain or omit trailing zeros after the decimal point (e.g. "23.0" = "23.0000" = "23" = "23."). Note that fields which are derived from float may contain negative values unless explicitly specified otherwise. """
    type_class_uri = FIXP["FIXFloat"]
    type_class_curie = "fixp:FIXFloat"
    type_name = "FIXFloat"
    type_model_uri = FIXP.FIXFloat


class FIXQty(Float):
    """ FIX Qty datatype (extends float). float field capable of storing either a whole number (no decimal places) of "shares" (securities denominated in whole units) or a decimal value containing decimal places for non-share quantity asset classes (securities denominated in fractional units). """
    type_class_uri = FIXP["FIXQty"]
    type_class_curie = "fixp:FIXQty"
    type_name = "FIXQty"
    type_model_uri = FIXP.FIXQty


class FIXPrice(Float):
    """ FIX Price datatype (extends float). float field representing a price. Note the number of decimal places may vary. For certain asset classes prices may be negative values. For example, prices for options strategies can be negative under certain market conditions. Refer to Volume 7: FIX Usage by Product for asset classes that support negative price values. Example: Strk="47.50" """
    type_class_uri = FIXP["FIXPrice"]
    type_class_curie = "fixp:FIXPrice"
    type_name = "FIXPrice"
    type_model_uri = FIXP.FIXPrice


class FIXPriceOffset(Float):
    """ FIX PriceOffset datatype (extends float). float field representing a price offset, which can be mathematically added to a "Price". Note the number of decimal places may vary and some fields such as LastForwardPoints may be negative. """
    type_class_uri = FIXP["FIXPriceOffset"]
    type_class_curie = "fixp:FIXPriceOffset"
    type_name = "FIXPriceOffset"
    type_model_uri = FIXP.FIXPriceOffset


class FIXAmt(Float):
    """ FIX Amt datatype (extends float). float field typically representing a Price times a Qty Example: Amt="6847.00" """
    type_class_uri = FIXP["FIXAmt"]
    type_class_curie = "fixp:FIXAmt"
    type_name = "FIXAmt"
    type_model_uri = FIXP.FIXAmt


class FIXPercentage(Float):
    """ FIX Percentage datatype (extends float). float field representing a percentage (e.g. 0.05 represents 5% and 0.9525 represents 95.25%). Note the number of decimal places may vary. """
    type_class_uri = FIXP["FIXPercentage"]
    type_class_curie = "fixp:FIXPercentage"
    type_name = "FIXPercentage"
    type_model_uri = FIXP.FIXPercentage


class FIXChar(String):
    """ FIX char base datatype. Single character value, can include any alphanumeric character or punctuation except the delimiter. All char fields are case sensitive (i.e. m != M). """
    type_class_uri = FIXP["FIXChar"]
    type_class_curie = "fixp:FIXChar"
    type_name = "FIXChar"
    type_model_uri = FIXP.FIXChar


class FIXBoolean(String):
    """ FIX Boolean datatype (extends char). char field containing one of two values: 'Y' = True/Yes 'N' = False/No """
    type_class_uri = FIXP["FIXBoolean"]
    type_class_curie = "fixp:FIXBoolean"
    type_name = "FIXBoolean"
    type_model_uri = FIXP.FIXBoolean


class FIXString(String):
    """ FIX String base datatype. Alpha-numeric free format strings, can include any character or punctuation except the delimiter. All String fields are case sensitive (i.e. morstatt != Morstatt). """
    type_class_uri = FIXP["FIXString"]
    type_class_curie = "fixp:FIXString"
    type_name = "FIXString"
    type_model_uri = FIXP.FIXString


class FIXMultipleCharValue(String):
    """ FIX MultipleCharValue datatype (extends String). string field containing one or more space delimited single character values (e.g. |18=2 A F| ). """
    type_class_uri = FIXP["FIXMultipleCharValue"]
    type_class_curie = "fixp:FIXMultipleCharValue"
    type_name = "FIXMultipleCharValue"
    type_model_uri = FIXP.FIXMultipleCharValue


class FIXMultipleStringValue(String):
    """ FIX MultipleStringValue datatype (extends String). string field containing one or more space delimited multiple character values (e.g. |277=AV AN A| ). """
    type_class_uri = FIXP["FIXMultipleStringValue"]
    type_class_curie = "fixp:FIXMultipleStringValue"
    type_name = "FIXMultipleStringValue"
    type_model_uri = FIXP.FIXMultipleStringValue


class FIXCountry(String):
    """ FIX Country datatype (extends String). string field representing a country using ISO 3166 Country code (2 character) values (see Appendix 6-B). """
    type_class_uri = FIXP["FIXCountry"]
    type_class_curie = "fixp:FIXCountry"
    type_name = "FIXCountry"
    type_model_uri = FIXP.FIXCountry


class FIXCurrency(String):
    """ FIX Currency datatype (extends String). string field representing a currency type using ISO 4217 Currency code (3 character) values (see Appendix 6-A). Example: StrkCcy="USD" """
    type_class_uri = FIXP["FIXCurrency"]
    type_class_curie = "fixp:FIXCurrency"
    type_name = "FIXCurrency"
    type_model_uri = FIXP.FIXCurrency


class FIXExchange(String):
    """ FIX Exchange datatype (extends String). string field representing a market or exchange using ISO 10383 Market Identifier Code (MIC) values (see"Appendix 6-C). """
    type_class_uri = FIXP["FIXExchange"]
    type_class_curie = "fixp:FIXExchange"
    type_name = "FIXExchange"
    type_model_uri = FIXP.FIXExchange


class FIXMonthYear(String):
    """ FIX MonthYear datatype (extends String). string field representing month of a year. An optional day of the month can be appended or an optional week code. Valid formats: YYYYMM YYYYMMDD YYYYMMWW Valid values: YYYY = 0000-9999; MM = 01-12; DD = 01-31; WW = w1, w2, w3, w4, w5. Example: MonthYear="200303", MonthYear="20030320", MonthYear="200303w2" """
    type_class_uri = FIXP["FIXMonthYear"]
    type_class_curie = "fixp:FIXMonthYear"
    type_name = "FIXMonthYear"
    type_model_uri = FIXP.FIXMonthYear


class FIXUTCTimestamp(Datetime):
    """ FIX UTCTimestamp datatype (extends String). string field representing time/date combination represented in UTC (Universal Time Coordinated, also known as "GMT") in either YYYYMMDD-HH:MM:SS (whole seconds) or YYYYMMDD-HH:MM:SS.sss* format, colons, dash, and period required. Valid values: YYYY = 0000-9999, MM = 01-12, DD = 01-31, HH = 00-23, MM = 00-59, SS = 00-60 (60 only if UTC leap second), sss* fractions of seconds. The fractions of seconds may be empty when no fractions of seconds are conveyed (in such a case the period is not conveyed), it may include 3 digits to convey milliseconds, 6 digits to convey microseconds, 9 digits to convey nanoseconds, 12 digits to convey picoseconds; Other number of digits may be used with bilateral agreement. Leap Seconds: Note that UTC includes corrections for leap seconds, which are inserted to account for slowing of the rotation of the earth. Leap second insertion is declared by the International Earth Rotation Service (IERS) and has, since 1972, only occurred on the night of Dec. 31 or Jun 30. The IERS considers March 31 and September 30 as secondary dates for leap second insertion, but has never utilized these dates. During a leap second insertion, a UTCTimestamp field may read "19981231-23:59:59", "19981231-23:59:60", "19990101-00:00:00". (see http://tycho.usno.navy.mil/leapsec.html) Example: TransactTime(60)="20011217-09:30:47.123" millisecond TransactTime(60)="20011217-09:30:47.123456" microseconds TransactTime(60)="20011217-09:30:47.123456789" nanoseconds TransactTime(60)="20011217-09:30:47.123456789123" picoseconds """
    type_class_uri = FIXP["FIXUTCTimestamp"]
    type_class_curie = "fixp:FIXUTCTimestamp"
    type_name = "FIXUTCTimestamp"
    type_model_uri = FIXP.FIXUTCTimestamp


class FIXUTCTimeOnly(String):
    """ FIX UTCTimeOnly datatype (extends String). string field representing time-only represented in UTC (Universal Time Coordinated, also known as "GMT") in either HH:MM:SS (whole seconds) or HH:MM:SS.sss* (milliseconds) format, colons, and period required. This special-purpose field is paired with UTCDateOnly to form a proper UTCTimestamp for bandwidth-sensitive messages. Valid values: HH = 00-23, MM = 00-59, SS = 00-60 (60 only if UTC leap second), sss* fractions of seconds. The fractions of seconds may be empty when no fractions of seconds are conveyed (in such a case the period is not conveyed), it may include 3 digits to convey milliseconds, 6 digits to convey microseconds, 9 digits to convey nanoseconds, 12 digits to convey picoseconds; Other number of digits may be used with bilateral agreement. Example: MDEntryTime(273)="13:20:00.123"milliseconds MDEntryTime(273)="13:20:00.123456" microseconds MDEntryTime(273)="13:20:00.123456789" nanoseconds MDEntryTime(273)="13:20:00.123456789123" picoseconds """
    type_class_uri = FIXP["FIXUTCTimeOnly"]
    type_class_curie = "fixp:FIXUTCTimeOnly"
    type_name = "FIXUTCTimeOnly"
    type_model_uri = FIXP.FIXUTCTimeOnly


class FIXUTCDateOnly(Date):
    """ FIX UTCDateOnly datatype (extends String). string field representing Date represented in UTC (Universal Time Coordinated, also known as "GMT") in YYYYMMDD format. This special-purpose field is paired with UTCTimeOnly to form a proper UTCTimestamp for bandwidth-sensitive messages. Valid values: YYYY = 0000-9999, MM = 01-12, DD = 01-31. Example: MDEntryDate="20030910" """
    type_class_uri = FIXP["FIXUTCDateOnly"]
    type_class_curie = "fixp:FIXUTCDateOnly"
    type_name = "FIXUTCDateOnly"
    type_model_uri = FIXP.FIXUTCDateOnly


class FIXLocalMktDate(Date):
    """ FIX LocalMktDate datatype (extends String). string field representing a Date of Local Market (as opposed to UTC) in YYYYMMDD format. This is the "normal" date field used by the FIX Protocol. Valid values: YYYY = 0000-9999, MM = 01-12, DD = 01-31 Example: MaturityDate(541)="20150724" """
    type_class_uri = FIXP["FIXLocalMktDate"]
    type_class_curie = "fixp:FIXLocalMktDate"
    type_name = "FIXLocalMktDate"
    type_model_uri = FIXP.FIXLocalMktDate


class FIXTZTimeOnly(String):
    """ FIX TZTimeOnly datatype (extends String). string field representing the time represented based on ISO 8601. This is the time with a UTC offset to allow identification of local time and timezone of that time. Format is HH:MM[:SS][Z | [ + | - hh[:mm]]] where HH = 00-23 hours, MM = 00-59 minutes, SS = 00-59 seconds, hh = 01-12 offset hours, mm = 00-59 offset minutes. Example: "07:39Z" is 07:39 UTC "02:39-05" is five hours behind UTC, thus Eastern Time "15:39+08" is eight hours ahead of UTC, Hong Kong/Singapore time "13:09+05:30" is 5.5 hours ahead of UTC, India time """
    type_class_uri = FIXP["FIXTZTimeOnly"]
    type_class_curie = "fixp:FIXTZTimeOnly"
    type_name = "FIXTZTimeOnly"
    type_model_uri = FIXP.FIXTZTimeOnly


class FIXTZTimestamp(Datetime):
    """ FIX TZTimestamp datatype (extends String). string field representing a time/date combination representing local time with an offset to UTC to allow identification of local time and timezone offset of that time. The representation is based on ISO 8601. Format is YYYYMMDD-HH:MM:SS.sss*[Z | [ + | - hh[:mm]]] where YYYY = 0000 to 9999, MM = 01-12, DD = 01-31 HH = 00-23 hours, MM = 00-59 minutes, SS = 00-59 seconds, hh = 01-12 offset hours, mm = 00-59 offset minutes, sss* fractions of seconds. The fractions of seconds may be empty when no fractions of seconds are conveyed (in such a case the period is not conveyed), it may include 3 digits to convey milliseconds, 6 digits to convey microseconds, 9 digits to convey nanoseconds, 12 digits to convey picoseconds; Other number of digits may be used with bilateral agreement Example: "20060901-07:39Z" is 07:39 UTC on 1st of September 2006 "20060901-02:39-05" is five hours behind UTC, thus Eastern Time on 1st of September 2006 "20060901-15:39+08" is eight hours ahead of UTC, Hong Kong/Singapore time on 1st of September 2006 "20060901-13:09+05:30" is 5.5 hours ahead of UTC, India time on 1st of September 2006 Using decimal seconds: "20060901-13:09.123+05:30" milliseconds "20060901-13:09.123456+05:30" microseconds "20060901-13:09.123456789+05:30" nanoseconds "20060901-13:09.123456789123+05:30" picoseconds "20060901-13:09.123456789Z" nanoseconds UTC timezone """
    type_class_uri = FIXP["FIXTZTimestamp"]
    type_class_curie = "fixp:FIXTZTimestamp"
    type_name = "FIXTZTimestamp"
    type_model_uri = FIXP.FIXTZTimestamp


class FIXData(String):
    """ FIX data datatype (extends String). string field containing raw data with no format or content restrictions. Data fields are always immediately preceded by a length field. The length field should specify the number of bytes of the value of the data field (up to but not including the terminating SOH). Caution: the value of one of these fields may contain the delimiter (SOH) character. Note that the value specified for this field should be followed by the delimiter (SOH) character as all fields are terminated with an "SOH". """
    type_class_uri = FIXP["FIXData"]
    type_class_curie = "fixp:FIXData"
    type_name = "FIXData"
    type_model_uri = FIXP.FIXData


class FIXPattern(String):
    """ FIX Pattern base datatype. Used to build on and provide some restrictions on what is allowed as valid values in fields that uses a base FIX data type and a pattern data type. The universe of allowable valid values for the field would then be the union of the base set of valid values and what is defined by the pattern data type. The pattern data type used by the field will retain its base FIX data type (e.g. String, int, char). """
    type_class_uri = FIXP["FIXPattern"]
    type_class_curie = "fixp:FIXPattern"
    type_name = "FIXPattern"
    type_model_uri = FIXP.FIXPattern


class FIXTenor(String):
    """ FIX Tenor datatype (extends Pattern). used to allow the expression of FX standard tenors in addition to the base valid enumerations defined for the field that uses this pattern data type. This pattern data type is defined as follows: Dx = tenor expression for "days", e.g. "D5", where "x" is any integer > 0 Mx = tenor expression for "months", e.g. "M3", where "x" is any integer > 0 Wx = tenor expression for "weeks", e.g. "W13", where "x" is any integer > 0 Yx = tenor expression for "years", e.g. "Y1", where "x" is any integer > 0 """
    type_class_uri = FIXP["FIXTenor"]
    type_class_curie = "fixp:FIXTenor"
    type_name = "FIXTenor"
    type_model_uri = FIXP.FIXTenor


class FIXReserved100Plus(Integer):
    """ FIX Reserved100Plus datatype (extends Pattern). Values "100" and above are reserved for bilaterally agreed upon user defined enumerations. """
    type_class_uri = FIXP["FIXReserved100Plus"]
    type_class_curie = "fixp:FIXReserved100Plus"
    type_name = "FIXReserved100Plus"
    type_model_uri = FIXP.FIXReserved100Plus


class FIXReserved1000Plus(Integer):
    """ FIX Reserved1000Plus datatype (extends Pattern). Values "1000" and above are reserved for bilaterally agreed upon user defined enumerations. """
    type_class_uri = FIXP["FIXReserved1000Plus"]
    type_class_curie = "fixp:FIXReserved1000Plus"
    type_name = "FIXReserved1000Plus"
    type_model_uri = FIXP.FIXReserved1000Plus


class FIXReserved4000Plus(Integer):
    """ FIX Reserved4000Plus datatype (extends Pattern). Values "4000" and above are reserved for bilaterally agreed upon user defined enumerations. """
    type_class_uri = FIXP["FIXReserved4000Plus"]
    type_class_curie = "fixp:FIXReserved4000Plus"
    type_name = "FIXReserved4000Plus"
    type_model_uri = FIXP.FIXReserved4000Plus


class FIXXMLData(String):
    """ FIX XMLData datatype (extends String). Contains an XML document raw data with no format or content restrictions. XMLData fields are always immediately preceded by a length field. The length field should specify the number of bytes of the value of the data field (up to but not including the terminating SOH). """
    type_class_uri = FIXP["FIXXMLData"]
    type_class_curie = "fixp:FIXXMLData"
    type_name = "FIXXMLData"
    type_model_uri = FIXP.FIXXMLData


class FIXLanguage(String):
    """ FIX Language datatype (extends String). Identifier for a national language - uses ISO 639-1 standard Example: en (English), es (spanish), etc. """
    type_class_uri = FIXP["FIXLanguage"]
    type_class_curie = "fixp:FIXLanguage"
    type_name = "FIXLanguage"
    type_model_uri = FIXP.FIXLanguage


class FIXLocalMktTime(String):
    """ FIX LocalMktTime datatype (extends String). string field representing the time local to a particular market center. Used where offset to UTC varies throughout the year and the defining market center is identified in a corresponding field. Format is HH:MM:SS where HH = 00-23 hours, MM = 00-59 minutes, SS = 00-59 seconds. In general only the hour token is non-zero. Example: Example: 07:00:00 """
    type_class_uri = FIXP["FIXLocalMktTime"]
    type_class_curie = "fixp:FIXLocalMktTime"
    type_name = "FIXLocalMktTime"
    type_model_uri = FIXP.FIXLocalMktTime


class FIXXID(String):
    """ FIX XID datatype (extends String). The purpose of the XID datatype is to define a unique identifier that is global to a FIX message. An identifier defined using this datatype uniquely identifies its containing element, whatever its type and name is. The constraint added by this datatype is that the values of all the fields that have an ID datatype in a FIX message must be unique. """
    type_class_uri = FIXP["FIXXID"]
    type_class_curie = "fixp:FIXXID"
    type_name = "FIXXID"
    type_model_uri = FIXP.FIXXID


class FIXXIDREF(String):
    """ FIX XIDREF datatype (extends String). The XIDREF datatype defines a reference to an identifier defined by the XID datatype. """
    type_class_uri = FIXP["FIXXIDREF"]
    type_class_curie = "fixp:FIXXIDREF"
    type_name = "FIXXIDREF"
    type_model_uri = FIXP.FIXXIDREF


class SbeUUID(Integer):
    """ RFC 4122 version 4 compliant unique identifier SBE primitive 'UUID' (primitiveType=uint8). """
    type_class_uri = FIXP["SbeUUID"]
    type_class_curie = "fixp:SbeUUID"
    type_name = "SbeUUID"
    type_model_uri = FIXP.SbeUUID


class SbeNanotime(Integer):
    """ Time in nanoseconds SBE primitive 'nanotime' (primitiveType=uint64). """
    type_class_uri = FIXP["SbeNanotime"]
    type_class_curie = "fixp:SbeNanotime"
    type_name = "SbeNanotime"
    type_model_uri = FIXP.SbeNanotime


class SbeDeltaMillisecs(Integer):
    """ Time interval in milliseconds SBE primitive 'DeltaMillisecs' (primitiveType=uint32). """
    type_class_uri = FIXP["SbeDeltaMillisecs"]
    type_class_curie = "fixp:SbeDeltaMillisecs"
    type_name = "SbeDeltaMillisecs"
    type_model_uri = FIXP.SbeDeltaMillisecs


class SbeOrdinal(Integer):
    """ SBE primitive 'ordinal' (primitiveType=uint64). """
    type_class_uri = FIXP["SbeOrdinal"]
    type_class_curie = "fixp:SbeOrdinal"
    type_name = "SbeOrdinal"
    type_model_uri = FIXP.SbeOrdinal


class SbeCardinal(Integer):
    """ SBE primitive 'cardinal' (primitiveType=uint32). """
    type_class_uri = FIXP["SbeCardinal"]
    type_class_curie = "fixp:SbeCardinal"
    type_name = "SbeCardinal"
    type_model_uri = FIXP.SbeCardinal


# Class references



@dataclass(repr=False)
class FixpSessionExchange(YAMLRoot):
    """
    Top-level container for a FIXP session exchange - holds an ordered list of session messages plus optional metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpSessionExchange"]
    class_class_curie: ClassVar[str] = "fixp:FixpSessionExchange"
    class_name: ClassVar[str] = "FixpSessionExchange"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpSessionExchange

    messages: Optional[Union[Union[dict, "FixpSessionMessage"], list[Union[dict, "FixpSessionMessage"]]]] = empty_list()
    title: Optional[str] = None
    creator: Optional[str] = None
    publisher: Optional[str] = None
    rights: Optional[str] = None
    date: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.messages, list):
            self.messages = [self.messages] if self.messages is not None else []
        self.messages = [v if isinstance(v, FixpSessionMessage) else FixpSessionMessage(**as_dict(v)) for v in self.messages]

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.creator is not None and not isinstance(self.creator, str):
            self.creator = str(self.creator)

        if self.publisher is not None and not isinstance(self.publisher, str):
            self.publisher = str(self.publisher)

        if self.rights is not None and not isinstance(self.rights, str):
            self.rights = str(self.rights)

        if self.date is not None and not isinstance(self.date, str):
            self.date = str(self.date)

        super().__post_init__(**kwargs)


class FixpSessionMessage(YAMLRoot):
    """
    Abstract base class for every FIXP session message.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpSessionMessage"]
    class_class_curie: ClassVar[str] = "fixp:FixpSessionMessage"
    class_name: ClassVar[str] = "FixpSessionMessage"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpSessionMessage


@dataclass(repr=False)
class SbeObjectComposite(YAMLRoot):
    """
    Variable length data, also know as octect string
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["SbeObjectComposite"]
    class_class_curie: ClassVar[str] = "fixp:SbeObjectComposite"
    class_name: ClassVar[str] = "SbeObjectComposite"
    class_model_uri: ClassVar[URIRef] = FIXP.SbeObjectComposite

    length: Optional[int] = None
    var_data: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.var_data is not None and not isinstance(self.var_data, int):
            self.var_data = int(self.var_data)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeCharacterStringComposite(YAMLRoot):
    """
    Variable length text
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["SbeCharacterStringComposite"]
    class_class_curie: ClassVar[str] = "fixp:SbeCharacterStringComposite"
    class_name: ClassVar[str] = "SbeCharacterStringComposite"
    class_model_uri: ClassVar[URIRef] = FIXP.SbeCharacterStringComposite

    length: Optional[int] = None
    var_data: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.var_data is not None and not isinstance(self.var_data, str):
            self.var_data = str(self.var_data)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageHeaderComposite(YAMLRoot):
    """
    Message identifiers and length of message root
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["SbeMessageHeaderComposite"]
    class_class_curie: ClassVar[str] = "fixp:SbeMessageHeaderComposite"
    class_name: ClassVar[str] = "SbeMessageHeaderComposite"
    class_model_uri: ClassVar[URIRef] = FIXP.SbeMessageHeaderComposite

    block_length: Optional[int] = None
    template_id: Optional[int] = None
    schema_id: Optional[int] = None
    schema_version: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.block_length is not None and not isinstance(self.block_length, int):
            self.block_length = int(self.block_length)

        if self.template_id is not None and not isinstance(self.template_id, int):
            self.template_id = int(self.template_id)

        if self.schema_id is not None and not isinstance(self.schema_id, int):
            self.schema_id = int(self.schema_id)

        if self.schema_version is not None and not isinstance(self.schema_version, int):
            self.schema_version = int(self.schema_version)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Negotiate(FixpSessionMessage):
    """
    FIXP session message 'Negotiate'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Negotiate"]
    class_class_curie: ClassVar[str] = "fixp:Negotiate"
    class_name: ClassVar[str] = "Negotiate"
    class_model_uri: ClassVar[URIRef] = FIXP.Negotiate

    session_id: Union[str, FIXString] = None
    timestamp: Union[int, FIXInt] = None
    client_flow: Union[str, "ClientFlowFieldEnum"] = None
    credentials: Optional[Union[str, FIXData]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.timestamp):
            self.MissingRequiredField("timestamp")
        if not isinstance(self.timestamp, FIXInt):
            self.timestamp = FIXInt(self.timestamp)

        if self._is_empty(self.client_flow):
            self.MissingRequiredField("client_flow")
        if not isinstance(self.client_flow, ClientFlowFieldEnum):
            self.client_flow = ClientFlowFieldEnum(self.client_flow)

        if self.credentials is not None and not isinstance(self.credentials, FIXData):
            self.credentials = FIXData(self.credentials)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NegotiationResponse(FixpSessionMessage):
    """
    FIXP session message 'NegotiationResponse'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["NegotiationResponse"]
    class_class_curie: ClassVar[str] = "fixp:NegotiationResponse"
    class_name: ClassVar[str] = "NegotiationResponse"
    class_model_uri: ClassVar[URIRef] = FIXP.NegotiationResponse

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    server_flow: Union[str, "ClientFlowCodeSet"] = None
    credentials: Optional[Union[str, FIXData]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.server_flow):
            self.MissingRequiredField("server_flow")
        if not isinstance(self.server_flow, ClientFlowCodeSet):
            self.server_flow = ClientFlowCodeSet(self.server_flow)

        if self.credentials is not None and not isinstance(self.credentials, FIXData):
            self.credentials = FIXData(self.credentials)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NegotiationReject(FixpSessionMessage):
    """
    FIXP session message 'NegotiationReject'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["NegotiationReject"]
    class_class_curie: ClassVar[str] = "fixp:NegotiationReject"
    class_name: ClassVar[str] = "NegotiationReject"
    class_model_uri: ClassVar[URIRef] = FIXP.NegotiationReject

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    negotiation_reject_code: Union[str, "NegotiationRejectCodeFieldEnum"] = None
    reason: Optional[Union[str, FIXString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.negotiation_reject_code):
            self.MissingRequiredField("negotiation_reject_code")
        if not isinstance(self.negotiation_reject_code, NegotiationRejectCodeFieldEnum):
            self.negotiation_reject_code = NegotiationRejectCodeFieldEnum(self.negotiation_reject_code)

        if self.reason is not None and not isinstance(self.reason, FIXString):
            self.reason = FIXString(self.reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Topic(FixpSessionMessage):
    """
    FIXP session message 'Topic'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Topic"]
    class_class_curie: ClassVar[str] = "fixp:Topic"
    class_name: ClassVar[str] = "Topic"
    class_model_uri: ClassVar[URIRef] = FIXP.Topic

    session_id: Union[str, FIXString] = None
    flow: Union[str, "FlowFieldEnum"] = None
    keepalive_interval: Union[int, FIXInt] = None
    classification: Union[str, FIXData] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.flow):
            self.MissingRequiredField("flow")
        if not isinstance(self.flow, FlowFieldEnum):
            self.flow = FlowFieldEnum(self.flow)

        if self._is_empty(self.keepalive_interval):
            self.MissingRequiredField("keepalive_interval")
        if not isinstance(self.keepalive_interval, FIXInt):
            self.keepalive_interval = FIXInt(self.keepalive_interval)

        if self._is_empty(self.classification):
            self.MissingRequiredField("classification")
        if not isinstance(self.classification, FIXData):
            self.classification = FIXData(self.classification)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Establish(FixpSessionMessage):
    """
    FIXP session message 'Establish'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Establish"]
    class_class_curie: ClassVar[str] = "fixp:Establish"
    class_name: ClassVar[str] = "Establish"
    class_model_uri: ClassVar[URIRef] = FIXP.Establish

    session_id: Union[str, FIXString] = None
    timestamp: Union[int, FIXInt] = None
    keepalive_interval: Union[int, FIXInt] = None
    next_seq_no: Optional[Union[int, FIXInt]] = None
    credentials: Optional[Union[str, FIXData]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.timestamp):
            self.MissingRequiredField("timestamp")
        if not isinstance(self.timestamp, FIXInt):
            self.timestamp = FIXInt(self.timestamp)

        if self._is_empty(self.keepalive_interval):
            self.MissingRequiredField("keepalive_interval")
        if not isinstance(self.keepalive_interval, FIXInt):
            self.keepalive_interval = FIXInt(self.keepalive_interval)

        if self.next_seq_no is not None and not isinstance(self.next_seq_no, FIXInt):
            self.next_seq_no = FIXInt(self.next_seq_no)

        if self.credentials is not None and not isinstance(self.credentials, FIXData):
            self.credentials = FIXData(self.credentials)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EstablishmentAck(FixpSessionMessage):
    """
    FIXP session message 'EstablishmentAck'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["EstablishmentAck"]
    class_class_curie: ClassVar[str] = "fixp:EstablishmentAck"
    class_name: ClassVar[str] = "EstablishmentAck"
    class_model_uri: ClassVar[URIRef] = FIXP.EstablishmentAck

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    keepalive_interval: Union[int, FIXInt] = None
    next_seq_no: Optional[Union[int, FIXInt]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.keepalive_interval):
            self.MissingRequiredField("keepalive_interval")
        if not isinstance(self.keepalive_interval, FIXInt):
            self.keepalive_interval = FIXInt(self.keepalive_interval)

        if self.next_seq_no is not None and not isinstance(self.next_seq_no, FIXInt):
            self.next_seq_no = FIXInt(self.next_seq_no)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EstablishmentReject(FixpSessionMessage):
    """
    FIXP session message 'EstablishmentReject'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["EstablishmentReject"]
    class_class_curie: ClassVar[str] = "fixp:EstablishmentReject"
    class_name: ClassVar[str] = "EstablishmentReject"
    class_model_uri: ClassVar[URIRef] = FIXP.EstablishmentReject

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    establishment_reject_code: Union[str, "EstablishmentRejectCodeFieldEnum"] = None
    reason: Optional[Union[str, FIXString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.establishment_reject_code):
            self.MissingRequiredField("establishment_reject_code")
        if not isinstance(self.establishment_reject_code, EstablishmentRejectCodeFieldEnum):
            self.establishment_reject_code = EstablishmentRejectCodeFieldEnum(self.establishment_reject_code)

        if self.reason is not None and not isinstance(self.reason, FIXString):
            self.reason = FIXString(self.reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sequence(FixpSessionMessage):
    """
    FIXP session message 'Sequence'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Sequence"]
    class_class_curie: ClassVar[str] = "fixp:Sequence"
    class_name: ClassVar[str] = "Sequence"
    class_model_uri: ClassVar[URIRef] = FIXP.Sequence

    next_seq_no: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.next_seq_no):
            self.MissingRequiredField("next_seq_no")
        if not isinstance(self.next_seq_no, FIXInt):
            self.next_seq_no = FIXInt(self.next_seq_no)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Context(FixpSessionMessage):
    """
    FIXP session message 'Context'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Context"]
    class_class_curie: ClassVar[str] = "fixp:Context"
    class_name: ClassVar[str] = "Context"
    class_model_uri: ClassVar[URIRef] = FIXP.Context

    session_id: Union[str, FIXString] = None
    next_seq_no: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.next_seq_no):
            self.MissingRequiredField("next_seq_no")
        if not isinstance(self.next_seq_no, FIXInt):
            self.next_seq_no = FIXInt(self.next_seq_no)

        super().__post_init__(**kwargs)


class UnsequencedHeartbeat(FixpSessionMessage):
    """
    FIXP session message 'UnsequencedHeartbeat'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["UnsequencedHeartbeat"]
    class_class_curie: ClassVar[str] = "fixp:UnsequencedHeartbeat"
    class_name: ClassVar[str] = "UnsequencedHeartbeat"
    class_model_uri: ClassVar[URIRef] = FIXP.UnsequencedHeartbeat


@dataclass(repr=False)
class RetransmitRequest(FixpSessionMessage):
    """
    FIXP session message 'RetransmitRequest'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["RetransmitRequest"]
    class_class_curie: ClassVar[str] = "fixp:RetransmitRequest"
    class_name: ClassVar[str] = "RetransmitRequest"
    class_model_uri: ClassVar[URIRef] = FIXP.RetransmitRequest

    session_id: Union[str, FIXString] = None
    timestamp: Union[int, FIXInt] = None
    from_seq_no: Union[int, FIXInt] = None
    count: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.timestamp):
            self.MissingRequiredField("timestamp")
        if not isinstance(self.timestamp, FIXInt):
            self.timestamp = FIXInt(self.timestamp)

        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FIXInt):
            self.from_seq_no = FIXInt(self.from_seq_no)

        if self._is_empty(self.count):
            self.MissingRequiredField("count")
        if not isinstance(self.count, FIXInt):
            self.count = FIXInt(self.count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Retransmission(FixpSessionMessage):
    """
    FIXP session message 'Retransmission'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Retransmission"]
    class_class_curie: ClassVar[str] = "fixp:Retransmission"
    class_name: ClassVar[str] = "Retransmission"
    class_model_uri: ClassVar[URIRef] = FIXP.Retransmission

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    next_seq_no: Union[int, FIXInt] = None
    count: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.next_seq_no):
            self.MissingRequiredField("next_seq_no")
        if not isinstance(self.next_seq_no, FIXInt):
            self.next_seq_no = FIXInt(self.next_seq_no)

        if self._is_empty(self.count):
            self.MissingRequiredField("count")
        if not isinstance(self.count, FIXInt):
            self.count = FIXInt(self.count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RestransmitReject(FixpSessionMessage):
    """
    FIXP session message 'RestransmitReject'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["RestransmitReject"]
    class_class_curie: ClassVar[str] = "fixp:RestransmitReject"
    class_name: ClassVar[str] = "RestransmitReject"
    class_model_uri: ClassVar[URIRef] = FIXP.RestransmitReject

    session_id: Union[str, FIXString] = None
    request_timestamp: Union[int, FIXInt] = None
    retransmit_reject_code: Union[str, "RetransmitRejectCodeFieldEnum"] = None
    reason: Optional[Union[str, FIXString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FIXInt):
            self.request_timestamp = FIXInt(self.request_timestamp)

        if self._is_empty(self.retransmit_reject_code):
            self.MissingRequiredField("retransmit_reject_code")
        if not isinstance(self.retransmit_reject_code, RetransmitRejectCodeFieldEnum):
            self.retransmit_reject_code = RetransmitRejectCodeFieldEnum(self.retransmit_reject_code)

        if self.reason is not None and not isinstance(self.reason, FIXString):
            self.reason = FIXString(self.reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Terminate(FixpSessionMessage):
    """
    FIXP session message 'Terminate'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Terminate"]
    class_class_curie: ClassVar[str] = "fixp:Terminate"
    class_name: ClassVar[str] = "Terminate"
    class_model_uri: ClassVar[URIRef] = FIXP.Terminate

    session_id: Union[str, FIXString] = None
    termination_code: Union[str, "TerminationCodeFieldEnum"] = None
    reason: Optional[Union[str, FIXString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.termination_code):
            self.MissingRequiredField("termination_code")
        if not isinstance(self.termination_code, TerminationCodeFieldEnum):
            self.termination_code = TerminationCodeFieldEnum(self.termination_code)

        if self.reason is not None and not isinstance(self.reason, FIXString):
            self.reason = FIXString(self.reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FinishedSending(FixpSessionMessage):
    """
    FIXP session message 'FinishedSending'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FinishedSending"]
    class_class_curie: ClassVar[str] = "fixp:FinishedSending"
    class_name: ClassVar[str] = "FinishedSending"
    class_model_uri: ClassVar[URIRef] = FIXP.FinishedSending

    session_id: Union[str, FIXString] = None
    last_seq_no: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        if self._is_empty(self.last_seq_no):
            self.MissingRequiredField("last_seq_no")
        if not isinstance(self.last_seq_no, FIXInt):
            self.last_seq_no = FIXInt(self.last_seq_no)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FinishedReceiving(FixpSessionMessage):
    """
    FIXP session message 'FinishedReceiving'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FinishedReceiving"]
    class_class_curie: ClassVar[str] = "fixp:FinishedReceiving"
    class_name: ClassVar[str] = "FinishedReceiving"
    class_model_uri: ClassVar[URIRef] = FIXP.FinishedReceiving

    session_id: Union[str, FIXString] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FIXString):
            self.session_id = FIXString(self.session_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Applied(FixpSessionMessage):
    """
    FIXP session message 'Applied'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["Applied"]
    class_class_curie: ClassVar[str] = "fixp:Applied"
    class_name: ClassVar[str] = "Applied"
    class_model_uri: ClassVar[URIRef] = FIXP.Applied

    from_seq_no: Union[int, FIXInt] = None
    count: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FIXInt):
            self.from_seq_no = FIXInt(self.from_seq_no)

        if self._is_empty(self.count):
            self.MissingRequiredField("count")
        if not isinstance(self.count, FIXInt):
            self.count = FIXInt(self.count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NotApplied(FixpSessionMessage):
    """
    FIXP session message 'NotApplied'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["NotApplied"]
    class_class_curie: ClassVar[str] = "fixp:NotApplied"
    class_name: ClassVar[str] = "NotApplied"
    class_model_uri: ClassVar[URIRef] = FIXP.NotApplied

    from_seq_no: Union[int, FIXInt] = None
    count: Union[int, FIXInt] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FIXInt):
            self.from_seq_no = FIXInt(self.from_seq_no)

        if self._is_empty(self.count):
            self.MissingRequiredField("count")
        if not isinstance(self.count, FIXInt):
            self.count = FIXInt(self.count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MessageTemplate(FixpSessionMessage):
    """
    FIXP session message 'MessageTemplate'.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["MessageTemplate"]
    class_class_curie: ClassVar[str] = "fixp:MessageTemplate"
    class_name: ClassVar[str] = "MessageTemplate"
    class_model_uri: ClassVar[URIRef] = FIXP.MessageTemplate

    flow: Union[str, "FlowFieldEnum"] = None
    effective_time: Union[int, FIXInt] = None
    template: Union[str, FIXData] = None
    version: Optional[Union[str, FIXData]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.flow):
            self.MissingRequiredField("flow")
        if not isinstance(self.flow, FlowFieldEnum):
            self.flow = FlowFieldEnum(self.flow)

        if self._is_empty(self.effective_time):
            self.MissingRequiredField("effective_time")
        if not isinstance(self.effective_time, FIXInt):
            self.effective_time = FIXInt(self.effective_time)

        if self._is_empty(self.template):
            self.MissingRequiredField("template")
        if not isinstance(self.template, FIXData):
            self.template = FIXData(self.template)

        if self.version is not None and not isinstance(self.version, FIXData):
            self.version = FIXData(self.version)

        if self.template is not None and not isinstance(self.template, FIXData):
            self.template = FIXData(self.template)

        super().__post_init__(**kwargs)


# Enumerations
class ClientFlowCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'ClientFlowCodeSet' (id=3, type=int).
    """
    RECOVERABLE = PermissibleValue(
        text="RECOVERABLE",
        title="Recoverable")
    IDEMPOTENT = PermissibleValue(
        text="IDEMPOTENT",
        title="Idempotent")
    UNSEQUENCED = PermissibleValue(
        text="UNSEQUENCED",
        title="Unsequenced")
    NONE = PermissibleValue(
        text="NONE",
        title="None")

    _defn = EnumDefinition(
        name="ClientFlowCodeSet",
        description="FIX Orchestra codeSet 'ClientFlowCodeSet' (id=3, type=int).",
    )

class NegotiationRejectCodeCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'NegotiationRejectCodeCodeSet' (id=7, type=int).
    """
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials")
    FLOW_TYPE_NOT_SUPPORTED = PermissibleValue(
        text="FLOW_TYPE_NOT_SUPPORTED",
        title="FlowTypeNotSupported")
    DUPLICATE_ID = PermissibleValue(
        text="DUPLICATE_ID",
        title="DuplicateId")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="NegotiationRejectCodeCodeSet",
        description="FIX Orchestra codeSet 'NegotiationRejectCodeCodeSet' (id=7, type=int).",
    )

class EstablishmentRejectCodeCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'EstablishmentRejectCodeCodeSet' (id=12, type=int).
    """
    UNNEGOTIATED = PermissibleValue(
        text="UNNEGOTIATED",
        title="Unnegotiated")
    ALREADY_ESTABLISHED = PermissibleValue(
        text="ALREADY_ESTABLISHED",
        title="AlreadyEstablished")
    SESSION_BLOCKED = PermissibleValue(
        text="SESSION_BLOCKED",
        title="SessionBlocked")
    KEEPALIVE_INTERVAL = PermissibleValue(
        text="KEEPALIVE_INTERVAL",
        title="KeepaliveInterval")
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="EstablishmentRejectCodeCodeSet",
        description="FIX Orchestra codeSet 'EstablishmentRejectCodeCodeSet' (id=12, type=int).",
    )

class RetransmitRejectCodeCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'RetransmitRejectCodeCodeSet' (id=15, type=int).
    """
    OUT_OF_RANGE = PermissibleValue(
        text="OUT_OF_RANGE",
        title="OutOfRange")
    INVALID_SESSION = PermissibleValue(
        text="INVALID_SESSION",
        title="InvalidSession")
    REQUEST_LIMIT_EXCEEDED = PermissibleValue(
        text="REQUEST_LIMIT_EXCEEDED",
        title="RequestLimitExceeded")

    _defn = EnumDefinition(
        name="RetransmitRejectCodeCodeSet",
        description="FIX Orchestra codeSet 'RetransmitRejectCodeCodeSet' (id=15, type=int).",
    )

class TerminationCodeCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'TerminationCodeCodeSet' (id=16, type=int).
    """
    FINISHED = PermissibleValue(
        text="FINISHED",
        title="Finished")
    UNSPECIFIED_ERROR = PermissibleValue(
        text="UNSPECIFIED_ERROR",
        title="UnspecifiedError")
    RE_REQUEST_OUT_OF_BOUNDS = PermissibleValue(
        text="RE_REQUEST_OUT_OF_BOUNDS",
        title="ReRequestOutOfBounds")
    RE_REQUEST_IN_PROGRESS = PermissibleValue(
        text="RE_REQUEST_IN_PROGRESS",
        title="ReRequestInProgress")

    _defn = EnumDefinition(
        name="TerminationCodeCodeSet",
        description="FIX Orchestra codeSet 'TerminationCodeCodeSet' (id=16, type=int).",
    )

class FlowCodeSet(EnumDefinitionImpl):
    """
    FIX Orchestra codeSet 'FlowCodeSet' (id=18, type=int).
    """
    RECOVERABLE = PermissibleValue(
        text="RECOVERABLE",
        title="Recoverable")
    IDEMPOTENT = PermissibleValue(
        text="IDEMPOTENT",
        title="Idempotent")

    _defn = EnumDefinition(
        name="FlowCodeSet",
        description="FIX Orchestra codeSet 'FlowCodeSet' (id=18, type=int).",
    )

class SbeFlowType(EnumDefinitionImpl):
    """
    SBE enum 'FlowType' (encodingType=uint8).
    """
    RECOVERABLE = PermissibleValue(
        text="RECOVERABLE",
        title="Recoverable",
        description="Guarantees exactly-once message delivery")
    IDEMPOTENT = PermissibleValue(
        text="IDEMPOTENT",
        title="Idempotent",
        description="Guarantees at-most-once delivery")
    UNSEQUENCED = PermissibleValue(
        text="UNSEQUENCED",
        title="Unsequenced",
        description="Best effort delivery")
    NONE = PermissibleValue(
        text="NONE",
        title="None",
        description="No application messages should be sent in one direction of a session")

    _defn = EnumDefinition(
        name="SbeFlowType",
        description="SBE enum 'FlowType' (encodingType=uint8).",
    )

class SbeNegotiationRejectCode(EnumDefinitionImpl):
    """
    SBE enum 'NegotiationRejectCode' (encodingType=uint8).
    """
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials",
        description="""Failed authentication because identity is not recognized, or the user is not authorized to use a particular service""")
    FLOW_TYPE_NOT_SUPPORTED = PermissibleValue(
        text="FLOW_TYPE_NOT_SUPPORTED",
        title="FlowTypeNotSupported",
        description="Server does not support requested client flow type")
    DUPLICATE_ID = PermissibleValue(
        text="DUPLICATE_ID",
        title="DuplicateId",
        description="Session ID is non-unique")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="SbeNegotiationRejectCode",
        description="SBE enum 'NegotiationRejectCode' (encodingType=uint8).",
    )

class SbeEstablishmentRejectCode(EnumDefinitionImpl):
    """
    SBE enum 'EstablishmentRejectCode' (encodingType=uint8).
    """
    UNNEGOTIATED = PermissibleValue(
        text="UNNEGOTIATED",
        title="Unnegotiated",
        description="""Establish request was not preceded by a Negotiation or session was finalized, requiring renegotiation""")
    ALREADY_ESTABLISHED = PermissibleValue(
        text="ALREADY_ESTABLISHED",
        title="AlreadyEstablished",
        description="EstablishmentAck was already sent; Establish was redundant")
    SESSION_BLOCKED = PermissibleValue(
        text="SESSION_BLOCKED",
        title="SessionBlocked",
        description="User is not authorized")
    KEEPALIVE_INTERVAL = PermissibleValue(
        text="KEEPALIVE_INTERVAL",
        title="KeepaliveInterval",
        description="Value is out of accepted range")
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials",
        description="""Failed authentication because identity is not recognized, or the user is not authorized to use a particular service""")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="SbeEstablishmentRejectCode",
        description="SBE enum 'EstablishmentRejectCode' (encodingType=uint8).",
    )

class SbeRetransmitRejectCode(EnumDefinitionImpl):
    """
    SBE enum 'RetransmitRejectCode' (encodingType=uint8).
    """
    OUT_OF_RANGE = PermissibleValue(
        text="OUT_OF_RANGE",
        title="OutOfRange",
        description="NextSeqNo + Count is beyond the range of sequence numbers")
    INVALID_SESSION = PermissibleValue(
        text="INVALID_SESSION",
        title="InvalidSession",
        description="The specified SessionId is unknown or is not authorized for the requester to access")
    REQUEST_LIMIT_EXCEEDED = PermissibleValue(
        text="REQUEST_LIMIT_EXCEEDED",
        title="RequestLimitExceeded",
        description="The message Count exceeds a local rule for maximum retransmission size")

    _defn = EnumDefinition(
        name="SbeRetransmitRejectCode",
        description="SBE enum 'RetransmitRejectCode' (encodingType=uint8).",
    )

class SbeTerminationCode(EnumDefinitionImpl):
    """
    SBE enum 'TerminationCode' (encodingType=uint8).
    """
    FINISHED = PermissibleValue(
        text="FINISHED",
        title="Finished")
    UNSPECIFIED_ERROR = PermissibleValue(
        text="UNSPECIFIED_ERROR",
        title="UnspecifiedError")
    RE_REQUEST_OUT_OF_BOUNDS = PermissibleValue(
        text="RE_REQUEST_OUT_OF_BOUNDS",
        title="ReRequestOutOfBounds")
    RE_REQUEST_IN_PROGRESS = PermissibleValue(
        text="RE_REQUEST_IN_PROGRESS",
        title="ReRequestInProgress")

    _defn = EnumDefinition(
        name="SbeTerminationCode",
        description="SBE enum 'TerminationCode' (encodingType=uint8).",
    )

class ClientFlowFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'ClientFlow' (id=3).
    """
    RECOVERABLE = PermissibleValue(
        text="RECOVERABLE",
        title="Recoverable")
    IDEMPOTENT = PermissibleValue(
        text="IDEMPOTENT",
        title="Idempotent")
    UNSEQUENCED = PermissibleValue(
        text="UNSEQUENCED",
        title="Unsequenced")
    NONE = PermissibleValue(
        text="NONE",
        title="None")

    _defn = EnumDefinition(
        name="ClientFlowFieldEnum",
        description="Inline FIX field enumeration for field 'ClientFlow' (id=3).",
    )

class NegotiationRejectCodeFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'NegotiationRejectCode' (id=7).
    """
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials")
    FLOW_TYPE_NOT_SUPPORTED = PermissibleValue(
        text="FLOW_TYPE_NOT_SUPPORTED",
        title="FlowTypeNotSupported")
    DUPLICATE_ID = PermissibleValue(
        text="DUPLICATE_ID",
        title="DuplicateId")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="NegotiationRejectCodeFieldEnum",
        description="Inline FIX field enumeration for field 'NegotiationRejectCode' (id=7).",
    )

class EstablishmentRejectCodeFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'EstablishmentRejectCode' (id=12).
    """
    UNNEGOTIATED = PermissibleValue(
        text="UNNEGOTIATED",
        title="Unnegotiated")
    ALREADY_ESTABLISHED = PermissibleValue(
        text="ALREADY_ESTABLISHED",
        title="AlreadyEstablished")
    SESSION_BLOCKED = PermissibleValue(
        text="SESSION_BLOCKED",
        title="SessionBlocked")
    KEEPALIVE_INTERVAL = PermissibleValue(
        text="KEEPALIVE_INTERVAL",
        title="KeepaliveInterval")
    CREDENTIALS = PermissibleValue(
        text="CREDENTIALS",
        title="Credentials")
    UNSPECIFIED = PermissibleValue(
        text="UNSPECIFIED",
        title="Unspecified")

    _defn = EnumDefinition(
        name="EstablishmentRejectCodeFieldEnum",
        description="Inline FIX field enumeration for field 'EstablishmentRejectCode' (id=12).",
    )

class RetransmitRejectCodeFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'RetransmitRejectCode' (id=15).
    """
    OUT_OF_RANGE = PermissibleValue(
        text="OUT_OF_RANGE",
        title="OutOfRange")
    INVALID_SESSION = PermissibleValue(
        text="INVALID_SESSION",
        title="InvalidSession")
    REQUEST_LIMIT_EXCEEDED = PermissibleValue(
        text="REQUEST_LIMIT_EXCEEDED",
        title="RequestLimitExceeded")

    _defn = EnumDefinition(
        name="RetransmitRejectCodeFieldEnum",
        description="Inline FIX field enumeration for field 'RetransmitRejectCode' (id=15).",
    )

class TerminationCodeFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'TerminationCode' (id=16).
    """
    FINISHED = PermissibleValue(
        text="FINISHED",
        title="Finished")
    UNSPECIFIED_ERROR = PermissibleValue(
        text="UNSPECIFIED_ERROR",
        title="UnspecifiedError")
    RE_REQUEST_OUT_OF_BOUNDS = PermissibleValue(
        text="RE_REQUEST_OUT_OF_BOUNDS",
        title="ReRequestOutOfBounds")
    RE_REQUEST_IN_PROGRESS = PermissibleValue(
        text="RE_REQUEST_IN_PROGRESS",
        title="ReRequestInProgress")

    _defn = EnumDefinition(
        name="TerminationCodeFieldEnum",
        description="Inline FIX field enumeration for field 'TerminationCode' (id=16).",
    )

class FlowFieldEnum(EnumDefinitionImpl):
    """
    Inline FIX field enumeration for field 'Flow' (id=18).
    """
    RECOVERABLE = PermissibleValue(
        text="RECOVERABLE",
        title="Recoverable")
    IDEMPOTENT = PermissibleValue(
        text="IDEMPOTENT",
        title="Idempotent")

    _defn = EnumDefinition(
        name="FlowFieldEnum",
        description="Inline FIX field enumeration for field 'Flow' (id=18).",
    )

# Slots
class slots:
    pass

slots.session_id = Slot(uri=FIXP.session_id, name="session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.session_id, domain=None, range=Optional[Union[str, FIXString]])

slots.timestamp = Slot(uri=FIXP.timestamp, name="timestamp", curie=FIXP.curie('timestamp'),
                   model_uri=FIXP.timestamp, domain=None, range=Optional[Union[int, FIXInt]])

slots.client_flow = Slot(uri=FIXP.client_flow, name="client_flow", curie=FIXP.curie('client_flow'),
                   model_uri=FIXP.client_flow, domain=None, range=Optional[Union[str, "ClientFlowFieldEnum"]])

slots.credentials = Slot(uri=FIXP.credentials, name="credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.credentials, domain=None, range=Optional[Union[str, FIXData]])

slots.request_timestamp = Slot(uri=FIXP.request_timestamp, name="request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.request_timestamp, domain=None, range=Optional[Union[int, FIXInt]])

slots.server_flow = Slot(uri=FIXP.server_flow, name="server_flow", curie=FIXP.curie('server_flow'),
                   model_uri=FIXP.server_flow, domain=None, range=Optional[Union[str, "ClientFlowCodeSet"]])

slots.negotiation_reject_code = Slot(uri=FIXP.negotiation_reject_code, name="negotiation_reject_code", curie=FIXP.curie('negotiation_reject_code'),
                   model_uri=FIXP.negotiation_reject_code, domain=None, range=Optional[Union[str, "NegotiationRejectCodeFieldEnum"]])

slots.reason = Slot(uri=FIXP.reason, name="reason", curie=FIXP.curie('reason'),
                   model_uri=FIXP.reason, domain=None, range=Optional[Union[str, FIXString]])

slots.keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.keepalive_interval, domain=None, range=Optional[Union[int, FIXInt]])

slots.classification = Slot(uri=FIXP.classification, name="classification", curie=FIXP.curie('classification'),
                   model_uri=FIXP.classification, domain=None, range=Optional[Union[str, FIXData]])

slots.next_seq_no = Slot(uri=FIXP.next_seq_no, name="next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.next_seq_no, domain=None, range=Optional[Union[int, FIXInt]])

slots.establishment_reject_code = Slot(uri=FIXP.establishment_reject_code, name="establishment_reject_code", curie=FIXP.curie('establishment_reject_code'),
                   model_uri=FIXP.establishment_reject_code, domain=None, range=Optional[Union[str, "EstablishmentRejectCodeFieldEnum"]])

slots.from_seq_no = Slot(uri=FIXP.from_seq_no, name="from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.from_seq_no, domain=None, range=Optional[Union[int, FIXInt]])

slots.count = Slot(uri=FIXP.count, name="count", curie=FIXP.curie('count'),
                   model_uri=FIXP.count, domain=None, range=Optional[Union[int, FIXInt]])

slots.retransmit_reject_code = Slot(uri=FIXP.retransmit_reject_code, name="retransmit_reject_code", curie=FIXP.curie('retransmit_reject_code'),
                   model_uri=FIXP.retransmit_reject_code, domain=None, range=Optional[Union[str, "RetransmitRejectCodeFieldEnum"]])

slots.termination_code = Slot(uri=FIXP.termination_code, name="termination_code", curie=FIXP.curie('termination_code'),
                   model_uri=FIXP.termination_code, domain=None, range=Optional[Union[str, "TerminationCodeFieldEnum"]])

slots.last_seq_no = Slot(uri=FIXP.last_seq_no, name="last_seq_no", curie=FIXP.curie('last_seq_no'),
                   model_uri=FIXP.last_seq_no, domain=None, range=Optional[Union[int, FIXInt]])

slots.flow = Slot(uri=FIXP.flow, name="flow", curie=FIXP.curie('flow'),
                   model_uri=FIXP.flow, domain=None, range=Optional[Union[str, "FlowFieldEnum"]])

slots.effective_time = Slot(uri=FIXP.effective_time, name="effective_time", curie=FIXP.curie('effective_time'),
                   model_uri=FIXP.effective_time, domain=None, range=Optional[Union[int, FIXInt]])

slots.version = Slot(uri=FIXP.version, name="version", curie=FIXP.curie('version'),
                   model_uri=FIXP.version, domain=None, range=Optional[Union[str, FIXData]])

slots.template = Slot(uri=FIXP.template, name="template", curie=FIXP.curie('template'),
                   model_uri=FIXP.template, domain=None, range=Optional[Union[str, FIXData]])

slots.fixpSessionExchange__messages = Slot(uri=FIXP.messages, name="fixpSessionExchange__messages", curie=FIXP.curie('messages'),
                   model_uri=FIXP.fixpSessionExchange__messages, domain=None, range=Optional[Union[Union[dict, FixpSessionMessage], list[Union[dict, FixpSessionMessage]]]])

slots.fixpSessionExchange__title = Slot(uri=DCTERMS.title, name="fixpSessionExchange__title", curie=DCTERMS.curie('title'),
                   model_uri=FIXP.fixpSessionExchange__title, domain=None, range=Optional[str])

slots.fixpSessionExchange__creator = Slot(uri=DCTERMS.creator, name="fixpSessionExchange__creator", curie=DCTERMS.curie('creator'),
                   model_uri=FIXP.fixpSessionExchange__creator, domain=None, range=Optional[str])

slots.fixpSessionExchange__publisher = Slot(uri=DCTERMS.publisher, name="fixpSessionExchange__publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=FIXP.fixpSessionExchange__publisher, domain=None, range=Optional[str])

slots.fixpSessionExchange__rights = Slot(uri=DCTERMS.rights, name="fixpSessionExchange__rights", curie=DCTERMS.curie('rights'),
                   model_uri=FIXP.fixpSessionExchange__rights, domain=None, range=Optional[str])

slots.fixpSessionExchange__date = Slot(uri=DCTERMS.date, name="fixpSessionExchange__date", curie=DCTERMS.curie('date'),
                   model_uri=FIXP.fixpSessionExchange__date, domain=None, range=Optional[str])

slots.sbeObjectComposite__length = Slot(uri=FIXP.length, name="sbeObjectComposite__length", curie=FIXP.curie('length'),
                   model_uri=FIXP.sbeObjectComposite__length, domain=None, range=Optional[int])

slots.sbeObjectComposite__var_data = Slot(uri=FIXP.var_data, name="sbeObjectComposite__var_data", curie=FIXP.curie('var_data'),
                   model_uri=FIXP.sbeObjectComposite__var_data, domain=None, range=Optional[int])

slots.sbeCharacterStringComposite__length = Slot(uri=FIXP.length, name="sbeCharacterStringComposite__length", curie=FIXP.curie('length'),
                   model_uri=FIXP.sbeCharacterStringComposite__length, domain=None, range=Optional[int])

slots.sbeCharacterStringComposite__var_data = Slot(uri=FIXP.var_data, name="sbeCharacterStringComposite__var_data", curie=FIXP.curie('var_data'),
                   model_uri=FIXP.sbeCharacterStringComposite__var_data, domain=None, range=Optional[str])

slots.sbeMessageHeaderComposite__block_length = Slot(uri=FIXP.block_length, name="sbeMessageHeaderComposite__block_length", curie=FIXP.curie('block_length'),
                   model_uri=FIXP.sbeMessageHeaderComposite__block_length, domain=None, range=Optional[int])

slots.sbeMessageHeaderComposite__template_id = Slot(uri=FIXP.template_id, name="sbeMessageHeaderComposite__template_id", curie=FIXP.curie('template_id'),
                   model_uri=FIXP.sbeMessageHeaderComposite__template_id, domain=None, range=Optional[int])

slots.sbeMessageHeaderComposite__schema_id = Slot(uri=FIXP.schema_id, name="sbeMessageHeaderComposite__schema_id", curie=FIXP.curie('schema_id'),
                   model_uri=FIXP.sbeMessageHeaderComposite__schema_id, domain=None, range=Optional[int])

slots.sbeMessageHeaderComposite__schema_version = Slot(uri=FIXP.schema_version, name="sbeMessageHeaderComposite__schema_version", curie=FIXP.curie('schema_version'),
                   model_uri=FIXP.sbeMessageHeaderComposite__schema_version, domain=None, range=Optional[int])

slots.Negotiate_session_id = Slot(uri=FIXP.session_id, name="Negotiate_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Negotiate_session_id, domain=Negotiate, range=Union[str, FIXString])

slots.Negotiate_timestamp = Slot(uri=FIXP.timestamp, name="Negotiate_timestamp", curie=FIXP.curie('timestamp'),
                   model_uri=FIXP.Negotiate_timestamp, domain=Negotiate, range=Union[int, FIXInt])

slots.Negotiate_client_flow = Slot(uri=FIXP.client_flow, name="Negotiate_client_flow", curie=FIXP.curie('client_flow'),
                   model_uri=FIXP.Negotiate_client_flow, domain=Negotiate, range=Union[str, "ClientFlowFieldEnum"])

slots.Negotiate_credentials = Slot(uri=FIXP.credentials, name="Negotiate_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.Negotiate_credentials, domain=Negotiate, range=Optional[Union[str, FIXData]])

slots.NegotiationResponse_session_id = Slot(uri=FIXP.session_id, name="NegotiationResponse_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.NegotiationResponse_session_id, domain=NegotiationResponse, range=Union[str, FIXString])

slots.NegotiationResponse_request_timestamp = Slot(uri=FIXP.request_timestamp, name="NegotiationResponse_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.NegotiationResponse_request_timestamp, domain=NegotiationResponse, range=Union[int, FIXInt])

slots.NegotiationResponse_server_flow = Slot(uri=FIXP.server_flow, name="NegotiationResponse_server_flow", curie=FIXP.curie('server_flow'),
                   model_uri=FIXP.NegotiationResponse_server_flow, domain=NegotiationResponse, range=Union[str, "ClientFlowCodeSet"])

slots.NegotiationResponse_credentials = Slot(uri=FIXP.credentials, name="NegotiationResponse_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.NegotiationResponse_credentials, domain=NegotiationResponse, range=Optional[Union[str, FIXData]])

slots.NegotiationReject_session_id = Slot(uri=FIXP.session_id, name="NegotiationReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.NegotiationReject_session_id, domain=NegotiationReject, range=Union[str, FIXString])

slots.NegotiationReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="NegotiationReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.NegotiationReject_request_timestamp, domain=NegotiationReject, range=Union[int, FIXInt])

slots.NegotiationReject_negotiation_reject_code = Slot(uri=FIXP.negotiation_reject_code, name="NegotiationReject_negotiation_reject_code", curie=FIXP.curie('negotiation_reject_code'),
                   model_uri=FIXP.NegotiationReject_negotiation_reject_code, domain=NegotiationReject, range=Union[str, "NegotiationRejectCodeFieldEnum"])

slots.NegotiationReject_reason = Slot(uri=FIXP.reason, name="NegotiationReject_reason", curie=FIXP.curie('reason'),
                   model_uri=FIXP.NegotiationReject_reason, domain=NegotiationReject, range=Optional[Union[str, FIXString]])

slots.Topic_session_id = Slot(uri=FIXP.session_id, name="Topic_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Topic_session_id, domain=Topic, range=Union[str, FIXString])

slots.Topic_flow = Slot(uri=FIXP.flow, name="Topic_flow", curie=FIXP.curie('flow'),
                   model_uri=FIXP.Topic_flow, domain=Topic, range=Union[str, "FlowFieldEnum"])

slots.Topic_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="Topic_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.Topic_keepalive_interval, domain=Topic, range=Union[int, FIXInt])

slots.Topic_classification = Slot(uri=FIXP.classification, name="Topic_classification", curie=FIXP.curie('classification'),
                   model_uri=FIXP.Topic_classification, domain=Topic, range=Union[str, FIXData])

slots.Establish_session_id = Slot(uri=FIXP.session_id, name="Establish_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Establish_session_id, domain=Establish, range=Union[str, FIXString])

slots.Establish_timestamp = Slot(uri=FIXP.timestamp, name="Establish_timestamp", curie=FIXP.curie('timestamp'),
                   model_uri=FIXP.Establish_timestamp, domain=Establish, range=Union[int, FIXInt])

slots.Establish_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="Establish_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.Establish_keepalive_interval, domain=Establish, range=Union[int, FIXInt])

slots.Establish_credentials = Slot(uri=FIXP.credentials, name="Establish_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.Establish_credentials, domain=Establish, range=Optional[Union[str, FIXData]])

slots.EstablishmentAck_session_id = Slot(uri=FIXP.session_id, name="EstablishmentAck_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.EstablishmentAck_session_id, domain=EstablishmentAck, range=Union[str, FIXString])

slots.EstablishmentAck_request_timestamp = Slot(uri=FIXP.request_timestamp, name="EstablishmentAck_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.EstablishmentAck_request_timestamp, domain=EstablishmentAck, range=Union[int, FIXInt])

slots.EstablishmentAck_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="EstablishmentAck_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.EstablishmentAck_keepalive_interval, domain=EstablishmentAck, range=Union[int, FIXInt])

slots.EstablishmentReject_session_id = Slot(uri=FIXP.session_id, name="EstablishmentReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.EstablishmentReject_session_id, domain=EstablishmentReject, range=Union[str, FIXString])

slots.EstablishmentReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="EstablishmentReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.EstablishmentReject_request_timestamp, domain=EstablishmentReject, range=Union[int, FIXInt])

slots.EstablishmentReject_establishment_reject_code = Slot(uri=FIXP.establishment_reject_code, name="EstablishmentReject_establishment_reject_code", curie=FIXP.curie('establishment_reject_code'),
                   model_uri=FIXP.EstablishmentReject_establishment_reject_code, domain=EstablishmentReject, range=Union[str, "EstablishmentRejectCodeFieldEnum"])

slots.EstablishmentReject_reason = Slot(uri=FIXP.reason, name="EstablishmentReject_reason", curie=FIXP.curie('reason'),
                   model_uri=FIXP.EstablishmentReject_reason, domain=EstablishmentReject, range=Optional[Union[str, FIXString]])

slots.Sequence_next_seq_no = Slot(uri=FIXP.next_seq_no, name="Sequence_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.Sequence_next_seq_no, domain=Sequence, range=Union[int, FIXInt])

slots.Context_session_id = Slot(uri=FIXP.session_id, name="Context_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Context_session_id, domain=Context, range=Union[str, FIXString])

slots.Context_next_seq_no = Slot(uri=FIXP.next_seq_no, name="Context_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.Context_next_seq_no, domain=Context, range=Union[int, FIXInt])

slots.RetransmitRequest_session_id = Slot(uri=FIXP.session_id, name="RetransmitRequest_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.RetransmitRequest_session_id, domain=RetransmitRequest, range=Union[str, FIXString])

slots.RetransmitRequest_timestamp = Slot(uri=FIXP.timestamp, name="RetransmitRequest_timestamp", curie=FIXP.curie('timestamp'),
                   model_uri=FIXP.RetransmitRequest_timestamp, domain=RetransmitRequest, range=Union[int, FIXInt])

slots.RetransmitRequest_from_seq_no = Slot(uri=FIXP.from_seq_no, name="RetransmitRequest_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.RetransmitRequest_from_seq_no, domain=RetransmitRequest, range=Union[int, FIXInt])

slots.RetransmitRequest_count = Slot(uri=FIXP.count, name="RetransmitRequest_count", curie=FIXP.curie('count'),
                   model_uri=FIXP.RetransmitRequest_count, domain=RetransmitRequest, range=Union[int, FIXInt])

slots.Retransmission_session_id = Slot(uri=FIXP.session_id, name="Retransmission_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Retransmission_session_id, domain=Retransmission, range=Union[str, FIXString])

slots.Retransmission_request_timestamp = Slot(uri=FIXP.request_timestamp, name="Retransmission_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.Retransmission_request_timestamp, domain=Retransmission, range=Union[int, FIXInt])

slots.Retransmission_next_seq_no = Slot(uri=FIXP.next_seq_no, name="Retransmission_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.Retransmission_next_seq_no, domain=Retransmission, range=Union[int, FIXInt])

slots.Retransmission_count = Slot(uri=FIXP.count, name="Retransmission_count", curie=FIXP.curie('count'),
                   model_uri=FIXP.Retransmission_count, domain=Retransmission, range=Union[int, FIXInt])

slots.RestransmitReject_session_id = Slot(uri=FIXP.session_id, name="RestransmitReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.RestransmitReject_session_id, domain=RestransmitReject, range=Union[str, FIXString])

slots.RestransmitReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="RestransmitReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.RestransmitReject_request_timestamp, domain=RestransmitReject, range=Union[int, FIXInt])

slots.RestransmitReject_retransmit_reject_code = Slot(uri=FIXP.retransmit_reject_code, name="RestransmitReject_retransmit_reject_code", curie=FIXP.curie('retransmit_reject_code'),
                   model_uri=FIXP.RestransmitReject_retransmit_reject_code, domain=RestransmitReject, range=Union[str, "RetransmitRejectCodeFieldEnum"])

slots.RestransmitReject_reason = Slot(uri=FIXP.reason, name="RestransmitReject_reason", curie=FIXP.curie('reason'),
                   model_uri=FIXP.RestransmitReject_reason, domain=RestransmitReject, range=Optional[Union[str, FIXString]])

slots.Terminate_session_id = Slot(uri=FIXP.session_id, name="Terminate_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.Terminate_session_id, domain=Terminate, range=Union[str, FIXString])

slots.Terminate_termination_code = Slot(uri=FIXP.termination_code, name="Terminate_termination_code", curie=FIXP.curie('termination_code'),
                   model_uri=FIXP.Terminate_termination_code, domain=Terminate, range=Union[str, "TerminationCodeFieldEnum"])

slots.Terminate_reason = Slot(uri=FIXP.reason, name="Terminate_reason", curie=FIXP.curie('reason'),
                   model_uri=FIXP.Terminate_reason, domain=Terminate, range=Optional[Union[str, FIXString]])

slots.FinishedSending_session_id = Slot(uri=FIXP.session_id, name="FinishedSending_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FinishedSending_session_id, domain=FinishedSending, range=Union[str, FIXString])

slots.FinishedSending_last_seq_no = Slot(uri=FIXP.last_seq_no, name="FinishedSending_last_seq_no", curie=FIXP.curie('last_seq_no'),
                   model_uri=FIXP.FinishedSending_last_seq_no, domain=FinishedSending, range=Union[int, FIXInt])

slots.FinishedReceiving_session_id = Slot(uri=FIXP.session_id, name="FinishedReceiving_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FinishedReceiving_session_id, domain=FinishedReceiving, range=Union[str, FIXString])

slots.Applied_from_seq_no = Slot(uri=FIXP.from_seq_no, name="Applied_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.Applied_from_seq_no, domain=Applied, range=Union[int, FIXInt])

slots.Applied_count = Slot(uri=FIXP.count, name="Applied_count", curie=FIXP.curie('count'),
                   model_uri=FIXP.Applied_count, domain=Applied, range=Union[int, FIXInt])

slots.NotApplied_from_seq_no = Slot(uri=FIXP.from_seq_no, name="NotApplied_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.NotApplied_from_seq_no, domain=NotApplied, range=Union[int, FIXInt])

slots.NotApplied_count = Slot(uri=FIXP.count, name="NotApplied_count", curie=FIXP.curie('count'),
                   model_uri=FIXP.NotApplied_count, domain=NotApplied, range=Union[int, FIXInt])

slots.MessageTemplate_flow = Slot(uri=FIXP.flow, name="MessageTemplate_flow", curie=FIXP.curie('flow'),
                   model_uri=FIXP.MessageTemplate_flow, domain=MessageTemplate, range=Union[str, "FlowFieldEnum"])

slots.MessageTemplate_effective_time = Slot(uri=FIXP.effective_time, name="MessageTemplate_effective_time", curie=FIXP.curie('effective_time'),
                   model_uri=FIXP.MessageTemplate_effective_time, domain=MessageTemplate, range=Union[int, FIXInt])

slots.MessageTemplate_template = Slot(uri=FIXP.template, name="MessageTemplate_template", curie=FIXP.curie('template'),
                   model_uri=FIXP.MessageTemplate_template, domain=MessageTemplate, range=Union[str, FIXData])

slots.MessageTemplate_version = Slot(uri=FIXP.version, name="MessageTemplate_version", curie=FIXP.curie('version'),
                   model_uri=FIXP.MessageTemplate_version, domain=MessageTemplate, range=Optional[Union[str, FIXData]])
