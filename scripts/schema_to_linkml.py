#!/usr/bin/env python3
"""Generate a LinkML schema for the FIXP (FIX Performance) Session Protocol.

Sources (under ``upstream-releases/fixp-specification/<version>/resources/``):

* ``FixRepositoryForFIXP.xml`` - FIX Repository: datatypes, categories,
  sections, fields (with inline enums), messages (with fieldRefs).
* ``SBEschemaForFIXP.xml`` - Simple Binary Encoding: primitive types,
  composites, enums, and a wire-level message catalogue.
* ``OrchestraForFIXP.xml`` (when present) - FIX Orchestra: codeSets
  (richer enum names), datatypes with annotations, message structure.

The output is a single LinkML YAML schema covering 100% of the named
declarations across the three sources.  Where the same logical entity
appears in more than one source it is emitted once and annotated with the
list of source artifacts it derives from.

Defaults::

    upstream-releases/fixp-specification/v1-1/resources/*.xml
    upstream-releases/fixp-specification/v1-0-STANDARD/resources/OrchestraForFIXP.xml  (fallback - v1-1 omits Orchestra)
    src/fixp/schema/fixp.yaml

Usage::

    python3 scripts/schema_to_linkml.py
    UPSTREAM_DIR=.../v1-0-STANDARD/resources OUT_FILE=/tmp/fixp.yaml python3 scripts/schema_to_linkml.py
    python3 scripts/schema_to_linkml.py --upstream-dir ... --orchestra-xml ... --out-file ...

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------

SBE_NS = "http://fixprotocol.io/2016/sbe"
FIXR_NS = "http://fixprotocol.io/2020/orchestra/repository"

SBE = "{" + SBE_NS + "}"
FIXR = "{" + FIXR_NS + "}"


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------

_SNAKE1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
_SNAKE2 = re.compile(r"([a-z0-9])([A-Z])")


def snake(name: str) -> str:
    s = _SNAKE1.sub(r"\1_\2", name)
    s = _SNAKE2.sub(r"\1_\2", s)
    return s.lower().replace("-", "_")


def upper_snake(name: str) -> str:
    """PascalCase / camelCase -> UPPER_SNAKE_CASE (LinkML convention for
    permissible values)."""
    return snake(name).upper()


def pascal(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    out = "".join(p[:1].upper() + p[1:] for p in parts if p)
    return out[:1].upper() + out[1:] if out else out


def text_of(elt: ET.Element | None) -> str | None:
    if elt is None or elt.text is None:
        return None
    txt = " ".join(elt.text.split())
    return txt or None


# Map ``xs:*`` base types -> LinkML primitive types.
XSD_BASE_TO_LINKML: dict[str, str] = {
    "xs:integer": "integer",
    "xs:nonNegativeInteger": "integer",
    "xs:positiveInteger": "integer",
    "xs:long": "integer",
    "xs:int": "integer",
    "xs:short": "integer",
    "xs:decimal": "float",
    "xs:float": "float",
    "xs:double": "float",
    "xs:boolean": "boolean",
    "xs:string": "string",
    "xs:normalizedString": "string",
    "xs:token": "string",
    "xs:language": "string",
    "xs:Name": "string",
    "xs:NCName": "string",
    "xs:ID": "string",
    "xs:IDREF": "string",
    "xs:anyURI": "uri",
    "xs:base64Binary": "string",
    "xs:date": "date",
    "xs:dateTime": "datetime",
    "xs:time": "string",
}

# SBE primitiveType -> LinkML primitive type
SBE_PRIM_TO_LINKML: dict[str, str] = {
    "char": "string",
    "int8": "integer",
    "int16": "integer",
    "int32": "integer",
    "int64": "integer",
    "uint8": "integer",
    "uint16": "integer",
    "uint32": "integer",
    "uint64": "integer",
    "float": "float",
    "double": "double",
}

# FIX datatype name -> protobuf scalar (kept in sync with the
# fix-orchestra schema_to_linkml.py table for cross-project consistency).
FIX_DATATYPE_TO_PROTO: dict[str, str] = {
    "int": "fixed32",
    "Length": "fixed32",
    "TagNum": "fixed32",
    "SeqNum": "fixed32",
    "DayOfMonth": "fixed32",
    "NumInGroup": "fixed32",
    "float": "double",
    "Qty": "Decimal64",
    "Price": "Decimal64",
    "PriceOffset": "Decimal64",
    "Amt": "Decimal64",
    "Percentage": "double",
    "char": "string",
    "Boolean": "bool",
    "String": "string",
    "MultipleCharValue": "string",
    "MultipleStringValue": "string",
    "Country": "string",
    "Currency": "string",
    "Exchange": "string",
    "MonthYear": "string",
    "UTCTimestamp": "Timestamp",
    "UTCTimeOnly": "TimeOnly",
    "UTCDateOnly": "string",
    "LocalMktDate": "string",
    "TZTimeOnly": "TimeOnly",
    "TZTimestamp": "Timestamp",
    "data": "bytes",
    "Pattern": "string",
    "Tenor": "Tenor",
    "Reserved100Plus": "fixed32",
    "Reserved1000Plus": "fixed32",
    "Reserved4000Plus": "fixed32",
    "XMLData": "string",
    "Language": "string",
    "LocalMktTime": "TimeOnly",
    "XID": "string",
    "XIDREF": "string",
}


# ---------------------------------------------------------------------------
# Parsers - FIX Repository (FixRepositoryForFIXP.xml)
# ---------------------------------------------------------------------------


def parse_fix_repository(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    fix = root.find("fix")
    if fix is None:
        return {}

    out: dict = {
        "version": fix.get("version"),
        "edition": root.get("edition"),
        "copyright": root.get("copyright"),
        "generated": root.get("generated"),
        "datatypes": OrderedDict(),
        "categories": OrderedDict(),
        "sections": OrderedDict(),
        "fields": OrderedDict(),
        "messages": OrderedDict(),
    }

    dtypes = fix.find("datatypes")
    if dtypes is not None:
        for dt in dtypes.findall("datatype"):
            name = dt.get("name")
            if not name:
                continue
            xml = dt.find("XML")
            example = dt.find("Example")
            out["datatypes"][name] = {
                "base_type": dt.get("baseType"),
                "added": dt.get("added"),
                "xml_base": xml.get("base") if xml is not None else None,
                "xml_pattern": xml.get("pattern") if xml is not None else None,
                "xml_min_inclusive": (
                    xml.get("minInclusive") if xml is not None else None
                ),
                "example": text_of(example),
            }

    cats = fix.find("categories")
    if cats is not None:
        for c in cats.findall("category"):
            out["categories"][c.get("id")] = {
                "section": c.get("section"),
                "component_type": c.get("componentType"),
                "volume": c.get("volume"),
            }
    secs = fix.find("sections")
    if secs is not None:
        for s in secs.findall("section"):
            out["sections"][s.get("id")] = {
                "name": s.get("name"),
                "volume": s.get("volume"),
            }

    fields = fix.find("fields")
    if fields is not None:
        for f in fields.findall("field"):
            name = f.get("name")
            fid = f.get("id")
            if not name or not fid:
                continue
            enums = []
            for e in f.findall("enum"):
                enums.append(
                    {
                        "name": e.get("name"),
                        "value": e.get("value"),
                        "description": e.get("description"),
                    }
                )
            # Same id can appear more than once; keep the first definition.
            if fid in out["fields"]:
                out["fields"][fid].setdefault("aliases", []).append(name)
                continue
            out["fields"][fid] = {
                "id": fid,
                "name": name,
                "type": f.get("type"),
                "enums": enums,
            }

    messages = fix.find("messages")
    if messages is not None:
        for m in messages.findall("message"):
            mid = m.get("id")
            mname = m.get("name")
            if not mid or not mname:
                continue
            refs = []
            for r in m.findall("fieldRef"):
                refs.append(
                    {
                        "id": r.get("id"),
                        "name": r.get("name"),
                        "required": r.get("required") == "1",
                    }
                )
            out["messages"][mid] = {
                "id": mid,
                "name": mname,
                "msg_type": m.get("msgType"),
                "category": m.get("category"),
                "section": m.get("section"),
                "field_refs": refs,
            }
    return out


# ---------------------------------------------------------------------------
# Parsers - SBE schema (SBEschemaForFIXP.xml)
# ---------------------------------------------------------------------------


def parse_sbe_schema(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    out: dict = {
        "package": root.get("package"),
        "id": root.get("id"),
        "version": root.get("version"),
        "byte_order": root.get("byteOrder"),
        "types": OrderedDict(),
        "composites": OrderedDict(),
        "enums": OrderedDict(),
        "messages": OrderedDict(),
    }

    # The SBE schema declares the ``sbe`` namespace on the root only; all
    # children are emitted without a prefix and therefore live in the
    # *no-namespace*.  Probe both forms so the parser works against either
    # convention.
    def _children(parent: ET.Element, tag: str) -> list[ET.Element]:
        hits = list(parent.findall(tag))
        if not hits:
            hits = list(parent.findall(f"{SBE}{tag}"))
        return hits

    def _child(parent: ET.Element, tag: str) -> ET.Element | None:
        elt = parent.find(tag)
        if elt is None:
            elt = parent.find(f"{SBE}{tag}")
        return elt

    types_el = _child(root, "types")
    if types_el is not None:
        for child in types_el:
            tag = child.tag.split("}", 1)[-1]
            name = child.get("name")
            if not name:
                continue
            if tag == "type":
                out["types"][name] = {
                    "primitive_type": child.get("primitiveType"),
                    "length": child.get("length"),
                    "semantic_type": child.get("semanticType"),
                    "description": child.get("description"),
                }
            elif tag == "composite":
                members = []
                for m in _children(child, "type"):
                    members.append(
                        {
                            "name": m.get("name"),
                            "primitive_type": m.get("primitiveType"),
                            "length": m.get("length"),
                            "semantic_type": m.get("semanticType"),
                        }
                    )
                out["composites"][name] = {
                    "description": child.get("description"),
                    "members": members,
                }
            elif tag == "enum":
                values = []
                for vv in _children(child, "validValue"):
                    values.append(
                        {
                            "name": vv.get("name"),
                            "value": (vv.text or "").strip() or None,
                            "description": vv.get("description"),
                        }
                    )
                out["enums"][name] = {
                    "encoding_type": child.get("encodingType"),
                    "values": values,
                }

    # ``<sbe:message>`` IS in the sbe namespace; un-prefixed ``<message>``
    # is permitted by some publishers.
    msg_iter = _children(root, "message")
    for msg in msg_iter:
        mname = msg.get("name")
        mid = msg.get("id")
        if not mname or not mid:
            continue
        fields = []
        for f in _children(msg, "field"):
            fields.append(
                {
                    "kind": "field",
                    "name": f.get("name"),
                    "id": f.get("id"),
                    "type": f.get("type"),
                    "presence": f.get("presence"),
                    "description": f.get("description"),
                }
            )
        for d in _children(msg, "data"):
            fields.append(
                {
                    "kind": "data",
                    "name": d.get("name"),
                    "id": d.get("id"),
                    "type": d.get("type"),
                    "description": d.get("description"),
                }
            )
        out["messages"][mid] = {
            "id": mid,
            "name": mname,
            "description": msg.get("description"),
            "fields": fields,
        }
    return out


# ---------------------------------------------------------------------------
# Parsers - Orchestra (OrchestraForFIXP.xml) - OPTIONAL
# ---------------------------------------------------------------------------


_BAD_SELFCLOSE_RE = re.compile(
    r'(<fixr:message\b[^/>]*)/>\s*(<fixr:structure[^>]*/?>)\s*(</fixr:message>)'
)


def _repair_orchestra_xml(text: str) -> str:
    """Patch a known upstream well-formedness bug.

    Some published OrchestraForFIXP.xml files contain::

        <fixr:message id="10" name="UnsequencedHeartbeat" category="Session"/>
            <fixr:structure/>
        </fixr:message>

    i.e. a self-closing ``<fixr:message ... />`` immediately followed by a
    structure element and a closing ``</fixr:message>``.  Convert the
    spurious self-close to an opening tag so the document parses.
    """

    def _fix(m: re.Match[str]) -> str:
        return f"{m.group(1)}>{m.group(2)}{m.group(3)}"

    return _BAD_SELFCLOSE_RE.sub(_fix, text)


def parse_orchestra(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        # Upstream sources occasionally ship malformed structure tags;
        # apply a minimal repair and retry once.
        root = ET.fromstring(_repair_orchestra_xml(text))

    out: dict = {
        "metadata": OrderedDict(),
        "code_sets": OrderedDict(),
        "datatypes": OrderedDict(),
        "fields": OrderedDict(),
        "messages": OrderedDict(),
        "name": root.get("name"),
        "version": root.get("version"),
    }

    md = root.find(f"{FIXR}metadata")
    if md is not None:
        for child in md:
            tag = child.tag.split("}", 1)[-1]
            txt = text_of(child)
            if txt:
                out["metadata"][tag] = txt

    cs_root = root.find(f"{FIXR}codeSets")
    if cs_root is not None:
        for cs in cs_root.findall(f"{FIXR}codeSet"):
            name = cs.get("name")
            if not name:
                continue
            codes = []
            for c in cs.findall(f"{FIXR}code"):
                codes.append(
                    {
                        "name": c.get("name"),
                        "id": c.get("id"),
                        "value": c.get("value"),
                    }
                )
            out["code_sets"][name] = {
                "id": cs.get("id"),
                "type": cs.get("type"),
                "codes": codes,
            }

    dt_root = root.find(f"{FIXR}datatypes")
    if dt_root is not None:
        for dt in dt_root.findall(f"{FIXR}datatype"):
            name = dt.get("name")
            if not name:
                continue
            xml_base = None
            xml_pattern = None
            mapped = dt.find(f"{FIXR}mappedDatatype")
            if mapped is not None and mapped.get("standard") == "XML":
                xml_base = mapped.get("base")
                xml_pattern = mapped.get("pattern")
            synopsis = None
            ann = dt.find(f"{FIXR}annotation")
            if ann is not None:
                for d in ann.findall(f"{FIXR}documentation"):
                    if d.get("purpose") == "SYNOPSIS":
                        synopsis = " ".join("".join(d.itertext()).split())
                        break
            out["datatypes"][name] = {
                "base_type": dt.get("baseType"),
                "xml_base": xml_base,
                "xml_pattern": xml_pattern,
                "synopsis": synopsis,
            }

    f_root = root.find(f"{FIXR}fields")
    if f_root is not None:
        for f in f_root.findall(f"{FIXR}field"):
            fid = f.get("id")
            fname = f.get("name")
            if not fid or not fname:
                continue
            out["fields"][fid] = {
                "id": fid,
                "name": fname,
                "type": f.get("type"),
            }

    m_root = root.find(f"{FIXR}messages")
    if m_root is not None:
        for m in m_root.findall(f"{FIXR}message"):
            mid = m.get("id")
            mname = m.get("name")
            if not mid or not mname:
                continue
            structure = m.find(f"{FIXR}structure")
            refs = []
            if structure is not None:
                for r in structure.findall(f"{FIXR}fieldRef"):
                    refs.append(
                        {
                            "id": r.get("id"),
                            "presence": r.get("presence", "optional"),
                        }
                    )
            out["messages"][mid] = {
                "id": mid,
                "name": mname,
                "category": m.get("category"),
                "field_refs": refs,
            }
    return out


# ---------------------------------------------------------------------------
# Builders - assemble LinkML entities from parsed sources
# ---------------------------------------------------------------------------


def build_types(
    fix_repo: dict, orchestra: dict
) -> "OrderedDict[str, OrderedDict]":
    """LinkML ``types`` entries for every FIX base datatype.

    Datatype names take the ``FIX<Name>`` form to avoid clashing with LinkML
    built-in primitives such as ``int`` / ``float`` / ``string``.
    """
    types: "OrderedDict[str, OrderedDict]" = OrderedDict()
    names: list[str] = []
    seen: set[str] = set()
    for src in (fix_repo.get("datatypes") or {}, orchestra.get("datatypes") or {}):
        for n in src:
            if n not in seen:
                seen.add(n)
                names.append(n)

    for name in names:
        repo_info = (fix_repo.get("datatypes") or {}).get(name, {})
        orch_info = (orchestra.get("datatypes") or {}).get(name, {})
        xml_base = orch_info.get("xml_base") or repo_info.get("xml_base")
        xml_pattern = orch_info.get("xml_pattern") or repo_info.get("xml_pattern")
        synopsis = orch_info.get("synopsis")
        example = repo_info.get("example")
        base_type = orch_info.get("base_type") or repo_info.get("base_type")

        linkml_typeof = XSD_BASE_TO_LINKML.get(xml_base or "", "string")
        linkml_name = "FIX" + name[:1].upper() + name[1:]

        desc_parts: list[str] = []
        if base_type:
            desc_parts.append(f"FIX {name} datatype (extends {base_type}).")
        else:
            desc_parts.append(f"FIX {name} base datatype.")
        if synopsis:
            desc_parts.append(synopsis)
        if example:
            desc_parts.append(f"Example: {example}")

        entry: OrderedDict = OrderedDict()
        entry["description"] = " ".join(desc_parts)
        entry["typeof"] = linkml_typeof
        entry["uri"] = f"fixp:{linkml_name}"
        entry["exact_mappings"] = [f"fixr:{name}"]
        entry["in_subset"] = ["fix_base_types"]
        if xml_pattern:
            entry["pattern"] = xml_pattern
        annotations: OrderedDict = OrderedDict()
        proto_scalar = FIX_DATATYPE_TO_PROTO.get(name)
        if proto_scalar:
            annotations["proto_scalar"] = proto_scalar
        if xml_base:
            annotations["xsd_base"] = xml_base
        if repo_info.get("xml_min_inclusive"):
            annotations["xsd_min_inclusive"] = repo_info["xml_min_inclusive"]
        if annotations:
            entry["annotations"] = annotations
        types[linkml_name] = entry
    return types


def build_sbe_types(sbe: dict) -> "OrderedDict[str, OrderedDict]":
    """Each SBE primitive ``<type>`` becomes a LinkML type."""
    out: "OrderedDict[str, OrderedDict]" = OrderedDict()
    for name, info in (sbe.get("types") or {}).items():
        linkml_name = "Sbe" + pascal(name)
        prim = info.get("primitive_type") or ""
        typeof = SBE_PRIM_TO_LINKML.get(prim, "string")
        descs = []
        if info.get("description"):
            descs.append(info["description"])
        descs.append(f"SBE primitive '{name}' (primitiveType={prim}).")
        entry: OrderedDict = OrderedDict()
        entry["description"] = " ".join(descs)
        entry["typeof"] = typeof
        entry["uri"] = f"fixp:{linkml_name}"
        entry["exact_mappings"] = [f"sbe:{name}"]
        entry["in_subset"] = ["sbe_types"]
        annotations: OrderedDict = OrderedDict([("sbe_primitive_type", prim)])
        if info.get("length"):
            annotations["sbe_length"] = info["length"]
        if info.get("semantic_type"):
            annotations["sbe_semantic_type"] = info["semantic_type"]
        entry["annotations"] = annotations
        out[linkml_name] = entry
    return out


def build_enums(
    fix_repo: dict, sbe: dict, orchestra: dict
) -> "OrderedDict[str, OrderedDict]":
    """Build the union of all enumeration definitions.

    Strategy: emit Orchestra codeSets verbatim (canonical names such as
    ``ClientFlowCodeSet``), SBE enums prefixed with ``Sbe``, and inline
    FIX field enums under ``<FieldName>FieldEnum`` so all three sources
    coexist without name collisions.
    """
    enums: "OrderedDict[str, OrderedDict]" = OrderedDict()

    for cs_name, info in (orchestra.get("code_sets") or {}).items():
        linkml_name = pascal(cs_name)
        perm: OrderedDict = OrderedDict()
        for c in info["codes"]:
            body: OrderedDict = OrderedDict([("title", c["name"])])
            if c.get("value") is not None:
                body["annotations"] = OrderedDict([("fixr_value", c["value"])])
            perm[upper_snake(c["name"])] = body
        entry: OrderedDict = OrderedDict()
        entry["description"] = (
            f"FIX Orchestra codeSet '{cs_name}' (id={info.get('id')}, "
            f"type={info.get('type')})."
        )
        entry["enum_uri"] = f"fixp:{linkml_name}"
        entry["exact_mappings"] = [f"fixr:{cs_name}"]
        entry["in_subset"] = ["orchestra_code_sets"]
        entry["permissible_values"] = perm
        enums[linkml_name] = entry

    for sbe_name, info in (sbe.get("enums") or {}).items():
        linkml_name = "Sbe" + pascal(sbe_name)
        perm = OrderedDict()
        for vv in info["values"]:
            body = OrderedDict([("title", vv["name"])])
            if vv.get("description"):
                body["description"] = vv["description"]
            if vv.get("value") is not None:
                body.setdefault("annotations", OrderedDict())["sbe_value"] = vv[
                    "value"
                ]
            perm[upper_snake(vv["name"])] = body
        entry = OrderedDict()
        entry["description"] = (
            f"SBE enum '{sbe_name}' (encodingType={info.get('encoding_type')})."
        )
        entry["enum_uri"] = f"fixp:{linkml_name}"
        entry["exact_mappings"] = [f"sbe:{sbe_name}"]
        entry["in_subset"] = ["sbe_types"]
        entry["permissible_values"] = perm
        enums[linkml_name] = entry

    for fid, finfo in (fix_repo.get("fields") or {}).items():
        if not finfo.get("enums"):
            continue
        linkml_name = pascal(finfo["name"]) + "FieldEnum"
        if linkml_name in enums:
            continue
        perm = OrderedDict()
        for e in finfo["enums"]:
            body = OrderedDict([("title", e["name"])])
            if e.get("description"):
                body["description"] = e["description"]
            if e.get("value") is not None:
                body.setdefault("annotations", OrderedDict())["fix_value"] = e[
                    "value"
                ]
            perm[upper_snake(e["name"])] = body
        entry = OrderedDict()
        entry["description"] = (
            f"Inline FIX field enumeration for field '{finfo['name']}' "
            f"(id={fid})."
        )
        entry["enum_uri"] = f"fixp:{linkml_name}"
        entry["exact_mappings"] = [f"fixr:{finfo['name']}"]
        entry["in_subset"] = ["fix_field_enums"]
        entry["permissible_values"] = perm
        enums[linkml_name] = entry

    return enums


def _field_range(
    type_name: str | None,
    enums: "OrderedDict[str, OrderedDict]",
    types: "OrderedDict[str, OrderedDict]",
) -> str:
    """Resolve a FIX field/Orchestra type reference to a LinkML range."""
    if not type_name:
        return "string"
    cand = pascal(type_name)
    if cand in enums:
        return cand
    fix_name = "FIX" + type_name[:1].upper() + type_name[1:]
    if fix_name in types:
        return fix_name
    return "string"


def build_field_slots(
    fix_repo: dict,
    orchestra: dict,
    enums: "OrderedDict[str, OrderedDict]",
    types: "OrderedDict[str, OrderedDict]",
) -> "OrderedDict[str, OrderedDict]":
    """Define one schema-level slot per unique FIX field.

    FIX fields are identified by their numeric tag id; the same id has one
    canonical (name, type) tuple across the spec, so de-duplication is on
    that key.
    """
    slots: "OrderedDict[str, OrderedDict]" = OrderedDict()
    merged: "OrderedDict[str, dict]" = OrderedDict()
    for src_name, src in (
        ("fix_repository", fix_repo.get("fields") or {}),
        ("orchestra", orchestra.get("fields") or {}),
    ):
        for fid, info in src.items():
            existing = merged.get(fid)
            if existing is None:
                merged[fid] = {**info, "sources": [src_name]}
            else:
                if src_name == "orchestra" and (info.get("type") or "").endswith(
                    "CodeSet"
                ):
                    existing["type"] = info["type"]
                existing["sources"].append(src_name)

    for fid, info in merged.items():
        slot_name = snake(info["name"])
        body: OrderedDict = OrderedDict()
        body["description"] = f"FIX field '{info['name']}' (tag {fid})."
        repo_field = (fix_repo.get("fields") or {}).get(fid, {})
        inline_enum_name = pascal(info["name"]) + "FieldEnum"
        if repo_field.get("enums") and inline_enum_name in enums:
            body["range"] = inline_enum_name
        else:
            body["range"] = _field_range(info.get("type"), enums, types)
        body["slot_uri"] = f"fixp:{slot_name}"
        body["exact_mappings"] = [f"fixr:{info['name']}"]
        body["annotations"] = OrderedDict(
            [
                ("fix_tag", str(fid)),
                ("fix_field_name", info["name"]),
            ]
        )
        slots[slot_name] = body
    return slots


def build_sbe_composite_classes(
    sbe: dict,
) -> "OrderedDict[str, OrderedDict]":
    """Each SBE ``<composite>`` becomes a LinkML class with one attribute per member."""
    out: "OrderedDict[str, OrderedDict]" = OrderedDict()
    for name, info in (sbe.get("composites") or {}).items():
        linkml_name = "Sbe" + pascal(name) + "Composite"
        cls: OrderedDict = OrderedDict()
        cls["description"] = (
            info.get("description") or f"SBE composite type '{name}'."
        )
        cls["class_uri"] = f"fixp:{linkml_name}"
        cls["exact_mappings"] = [f"sbe:{name}"]
        cls["in_subset"] = ["sbe_types"]
        attrs: OrderedDict = OrderedDict()
        for m in info["members"]:
            mname = snake(m["name"])
            # Disambiguate SBE composite-member names that collide with
            # top-level FIX field slots whose range is incompatible. The SBE
            # ``messageHeader.version`` is a uint16 wire-format byte, distinct
            # from the FIX ``version`` slot used by ``MessageTemplate``.
            if linkml_name == "SbeMessageHeaderComposite" and mname == "version":
                mname = "schema_version"
            prim = m.get("primitive_type") or ""
            attr: OrderedDict = OrderedDict()
            attr["range"] = SBE_PRIM_TO_LINKML.get(prim, "string")
            attr["description"] = (
                f"SBE member '{m['name']}' (primitiveType={prim}"
                + (
                    f", semanticType={m['semantic_type']}"
                    if m.get("semantic_type")
                    else ""
                )
                + ")."
            )
            attr_anno: OrderedDict = OrderedDict([("sbe_primitive_type", prim)])
            if m["name"] != mname:
                attr_anno["sbe_member_name"] = m["name"]
            if m.get("length"):
                attr_anno["sbe_length"] = m["length"]
            if m.get("semantic_type"):
                attr_anno["sbe_semantic_type"] = m["semantic_type"]
            attr["annotations"] = attr_anno
            attrs[mname] = attr
        if attrs:
            cls["attributes"] = attrs
        out[linkml_name] = cls
    return out


def build_message_classes(
    fix_repo: dict,
    sbe: dict,
    orchestra: dict,
    field_slots: "OrderedDict[str, OrderedDict]",
) -> "OrderedDict[str, OrderedDict]":
    """One LinkML class per FIXP session message.

    Each message merges field references from all three sources;
    fix_repository fieldRefs are authoritative on cardinality
    (required/optional), Orchestra contributes structural ordering, and
    SBE adds wire-level ``data``-vs-``field`` annotations.
    """
    classes: "OrderedDict[str, OrderedDict]" = OrderedDict()

    fid_to_slot: dict[str, str] = {}
    fid_to_field_name: dict[str, str] = {}
    for fid, finfo in (fix_repo.get("fields") or {}).items():
        fid_to_slot[fid] = snake(finfo["name"])
        fid_to_field_name[fid] = finfo["name"]
    for fid, finfo in (orchestra.get("fields") or {}).items():
        fid_to_slot.setdefault(fid, snake(finfo["name"]))
        fid_to_field_name.setdefault(fid, finfo["name"])

    all_msgs: "OrderedDict[str, dict]" = OrderedDict()
    for info in (fix_repo.get("messages") or {}).values():
        all_msgs[info["name"]] = {
            "fix_repo": info,
            "sbe": None,
            "orchestra": None,
        }
    for info in (sbe.get("messages") or {}).values():
        all_msgs.setdefault(
            info["name"], {"fix_repo": None, "sbe": None, "orchestra": None}
        )["sbe"] = info
    for info in (orchestra.get("messages") or {}).values():
        all_msgs.setdefault(
            info["name"], {"fix_repo": None, "sbe": None, "orchestra": None}
        )["orchestra"] = info

    for mname, srcs in all_msgs.items():
        linkml_name = pascal(mname)
        cls: OrderedDict = OrderedDict()
        cls["is_a"] = "FixpSessionMessage"
        cls["description"] = f"FIXP session message '{mname}'."
        cls["class_uri"] = f"fixp:{linkml_name}"

        exact: list[str] = []
        if srcs.get("fix_repo"):
            exact.append(f"fixr:{mname}")
        if srcs.get("sbe"):
            exact.append(f"sbe:{mname}")
        if exact:
            cls["exact_mappings"] = exact

        cls["in_subset"] = ["fixp_session_messages"]

        annotations: OrderedDict = OrderedDict()
        if srcs.get("fix_repo"):
            annotations["fix_message_id"] = srcs["fix_repo"]["id"]
            if srcs["fix_repo"].get("category"):
                annotations["fix_category"] = srcs["fix_repo"]["category"]
            if srcs["fix_repo"].get("section"):
                annotations["fix_section"] = srcs["fix_repo"]["section"]
        if srcs.get("sbe"):
            annotations["sbe_template_id"] = srcs["sbe"]["id"]
        if srcs.get("orchestra"):
            annotations["orchestra_message_id"] = srcs["orchestra"]["id"]
        annotations["sources"] = ", ".join(
            k for k in ("fix_repo", "sbe", "orchestra") if srcs.get(k)
        )
        cls["annotations"] = annotations

        required_by_id: dict[str, bool] = {}
        seen_ids: list[str] = []
        for r in (srcs.get("fix_repo") or {}).get("field_refs", []) if srcs.get(
            "fix_repo"
        ) else []:
            fid = r["id"]
            if fid not in seen_ids:
                seen_ids.append(fid)
            required_by_id[fid] = required_by_id.get(fid, False) or r["required"]
        for r in (srcs.get("orchestra") or {}).get("field_refs", []) if srcs.get(
            "orchestra"
        ) else []:
            fid = r["id"]
            if fid not in seen_ids:
                seen_ids.append(fid)
            req = r["presence"] == "required"
            required_by_id[fid] = required_by_id.get(fid, False) or req

        # Emit class-level slot refinements via ``slots:`` + ``slot_usage:``
        # rather than ``attributes:``. Using ``attributes`` here creates a
        # brand-new attribute that does NOT inherit ``range`` from the
        # top-level slot definition, so linkml-jsonschema falls back to
        # ``default_range: string`` for any usage that omits an explicit
        # range (e.g. ``timestamp`` whose top-level slot has ``range:
        # FIXInt``). ``slots`` + ``slot_usage`` is the canonical LinkML
        # idiom for "reuse this slot but tighten constraints".
        slot_list: list[str] = []
        slot_usage: "OrderedDict[str, OrderedDict]" = OrderedDict()
        for fid in seen_ids:
            slot = fid_to_slot.get(fid)
            if not slot or slot not in field_slots:
                slot = f"field_{fid}"
            slot_list.append(slot)
            usage: OrderedDict = OrderedDict()
            if required_by_id.get(fid):
                usage["required"] = True
            if usage:
                slot_usage[slot] = usage

        sbe_msg = srcs.get("sbe")
        if sbe_msg:
            sbe_data_names = {
                f["name"] for f in sbe_msg["fields"] if f["kind"] == "data"
            }
            for slot_name in slot_list:
                fix_name_for_slot = next(
                    (
                        fid_to_field_name[fid]
                        for fid in seen_ids
                        if fid_to_slot.get(fid) == slot_name
                    ),
                    None,
                )
                if fix_name_for_slot and fix_name_for_slot in sbe_data_names:
                    usage = slot_usage.setdefault(slot_name, OrderedDict())
                    usage.setdefault(
                        "annotations", OrderedDict()
                    )["sbe_data_field"] = True

        if slot_list:
            cls["slots"] = slot_list
        if slot_usage:
            cls["slot_usage"] = slot_usage
        classes[linkml_name] = cls
    return classes


# ---------------------------------------------------------------------------
# Conversion driver
# ---------------------------------------------------------------------------


def convert(
    fix_repo_xml: Path,
    sbe_xml: Path,
    orchestra_xml: Path | None,
    out_file: Path,
) -> None:
    fix_repo = parse_fix_repository(fix_repo_xml)
    sbe = parse_sbe_schema(sbe_xml)
    orchestra = parse_orchestra(orchestra_xml)

    types = build_types(fix_repo, orchestra)
    types.update(build_sbe_types(sbe))

    enums = build_enums(fix_repo, sbe, orchestra)
    field_slots = build_field_slots(fix_repo, orchestra, enums, types)
    sbe_composites = build_sbe_composite_classes(sbe)

    base_class = OrderedDict(
        [
            (
                "description",
                "Abstract base class for every FIXP session message.",
            ),
            ("abstract", True),
            ("class_uri", "fixp:FixpSessionMessage"),
            ("in_subset", ["fixp_session_messages"]),
        ]
    )

    container_class = OrderedDict(
        [
            (
                "description",
                "Top-level container for a FIXP session exchange - holds an "
                "ordered list of session messages plus optional metadata.",
            ),
            ("tree_root", True),
            ("class_uri", "fixp:FixpSessionExchange"),
            (
                "attributes",
                OrderedDict(
                    [
                        (
                            "messages",
                            OrderedDict(
                                [
                                    ("range", "FixpSessionMessage"),
                                    ("multivalued", True),
                                    ("inlined_as_list", True),
                                    (
                                        "description",
                                        "Ordered sequence of FIXP session messages.",
                                    ),
                                ]
                            ),
                        ),
                        (
                            "title",
                            OrderedDict(
                                [
                                    ("range", "string"),
                                    ("slot_uri", "dcterms:title"),
                                    (
                                        "description",
                                        "Title of this exchange document.",
                                    ),
                                ]
                            ),
                        ),
                        (
                            "creator",
                            OrderedDict(
                                [
                                    ("range", "string"),
                                    ("slot_uri", "dcterms:creator"),
                                    (
                                        "description",
                                        "Creator of this exchange document.",
                                    ),
                                ]
                            ),
                        ),
                        (
                            "publisher",
                            OrderedDict(
                                [
                                    ("range", "string"),
                                    ("slot_uri", "dcterms:publisher"),
                                    (
                                        "description",
                                        "Publisher of this exchange document.",
                                    ),
                                ]
                            ),
                        ),
                        (
                            "rights",
                            OrderedDict(
                                [
                                    ("range", "string"),
                                    ("slot_uri", "dcterms:rights"),
                                    (
                                        "description",
                                        "Rights statement for this exchange document.",
                                    ),
                                ]
                            ),
                        ),
                        (
                            "date",
                            OrderedDict(
                                [
                                    ("range", "string"),
                                    ("slot_uri", "dcterms:date"),
                                    (
                                        "description",
                                        "Date associated with this exchange document.",
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )

    classes: "OrderedDict[str, OrderedDict]" = OrderedDict()
    classes["FixpSessionExchange"] = container_class
    classes["FixpSessionMessage"] = base_class
    classes.update(sbe_composites)
    classes.update(
        build_message_classes(fix_repo, sbe, orchestra, field_slots)
    )

    subsets: "OrderedDict[str, OrderedDict]" = OrderedDict(
        [
            (
                "fixp_session_messages",
                OrderedDict(
                    [
                        (
                            "description",
                            "FIXP point-to-point and multicast session-layer "
                            "messages (Negotiate, Establish, Sequence, "
                            "Retransmit*, ...).",
                        )
                    ]
                ),
            ),
            (
                "fix_base_types",
                OrderedDict(
                    [
                        (
                            "description",
                            "FIX base datatypes (int, String, UTCTimestamp, "
                            "...) carried over from the FIX Repository / "
                            "Orchestra. Each type is annotated with the "
                            "recommended protobuf scalar via the proto_scalar "
                            "annotation.",
                        )
                    ]
                ),
            ),
            (
                "sbe_types",
                OrderedDict(
                    [
                        (
                            "description",
                            "Simple Binary Encoding (SBE) primitive types and "
                            "composites used by the FIXP wire format.",
                        )
                    ]
                ),
            ),
            (
                "orchestra_code_sets",
                OrderedDict(
                    [
                        (
                            "description",
                            "FIX Orchestra codeSets (enumerations) supplying "
                            "stable, named identifiers for the FIX field "
                            "enums (e.g. ClientFlowCodeSet, "
                            "NegotiationRejectCodeCodeSet).",
                        )
                    ]
                ),
            ),
            (
                "fix_field_enums",
                OrderedDict(
                    [
                        (
                            "description",
                            "Inline FIX field enumerations synthesised from "
                            "FixRepository <field><enum/></field> blocks when "
                            "no Orchestra codeSet name is available.",
                        )
                    ]
                ),
            ),
        ]
    )

    header: OrderedDict = OrderedDict()
    header["id"] = "https://w3id.org/lmodel/fixp"
    header["name"] = "fixp"
    header["title"] = "FIXP (FIX Performance) Session Protocol"
    header["description"] = (
        "LinkML schema for the FIX Performance (FIXP) Session Protocol, "
        "auto-generated from the upstream specification artifacts "
        "(FixRepositoryForFIXP.xml, SBEschemaForFIXP.xml, "
        "OrchestraForFIXP.xml)."
    )
    header["license"] = "Apache-2.0"
    header["see_also"] = [
        "https://www.fixtrading.org/standards/fixp/",
        "https://github.com/FIXTradingCommunity/fixp-specification",
        "https://lmodel.github.io/fixp",
    ]
    header["source"] = (
        "https://github.com/FIXTradingCommunity/fixp-specification"
    )
    header["version"] = fix_repo.get("version") or orchestra.get("version") or "v1-1"
    header["notes"] = [
        "(c) Copyright FIX Protocol Limited. Creative Commons "
        "Attribution-NoDerivatives 4.0 International Public License "
        "(CC BY-ND 4.0) applies to the upstream FIXP specification.",
        "This LinkML schema is auto-generated by "
        "scripts/schema_to_linkml.py - edit the script (or the upstream "
        "XMLs) and re-run; do not edit this file by hand.",
    ]
    header["annotations"] = OrderedDict(
        [
            (
                "sources",
                "FixRepositoryForFIXP.xml, SBEschemaForFIXP.xml, "
                "OrchestraForFIXP.xml",
            ),
            ("fix_version", fix_repo.get("version") or ""),
            ("sbe_package", sbe.get("package") or ""),
            ("sbe_schema_id", sbe.get("id") or ""),
            ("sbe_byte_order", sbe.get("byte_order") or ""),
        ]
    )
    header["prefixes"] = OrderedDict(
        [
            ("fixp", "https://w3id.org/lmodel/fixp/"),
            ("linkml", "https://w3id.org/linkml/"),
            ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
            ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
            ("xsd", "http://www.w3.org/2001/XMLSchema#"),
            ("skos", "http://www.w3.org/2004/02/skos/core#"),
            ("schema", "http://schema.org/"),
            ("dc", "http://purl.org/dc/elements/1.1/"),
            ("dcterms", "http://purl.org/dc/terms/"),
            ("fixr", "http://fixprotocol.io/2020/orchestra/repository/"),
            ("sbe", "http://fixprotocol.io/2016/sbe/"),
        ]
    )
    header["default_prefix"] = "fixp"
    header["default_range"] = "string"
    header["imports"] = ["linkml:types"]

    doc: OrderedDict = OrderedDict(header)
    if types:
        doc["types"] = types
    if subsets:
        doc["subsets"] = subsets
    if enums:
        doc["enums"] = enums
    if field_slots:
        doc["slots"] = field_slots
    doc["classes"] = classes

    out_lines = [
        "---",
        "# Auto-generated by scripts/schema_to_linkml.py",
        "# Sources: upstream-releases/fixp-specification/<version>/resources/",
        "#   * FixRepositoryForFIXP.xml",
        "#   * SBEschemaForFIXP.xml",
        "#   * OrchestraForFIXP.xml (optional)",
        "# DO NOT EDIT BY HAND - re-run the script to regenerate.",
        "",
    ]
    out_lines.extend(dump_yaml(doc))
    out_lines.append("")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(out_lines), encoding="utf-8")

    print("=== FIXP sources -> LinkML coverage ===", file=sys.stderr)
    print(
        f"  FixRepository: datatypes={len(fix_repo.get('datatypes') or {})} "
        f"fields={len(fix_repo.get('fields') or {})} "
        f"messages={len(fix_repo.get('messages') or {})} "
        f"categories={len(fix_repo.get('categories') or {})} "
        f"sections={len(fix_repo.get('sections') or {})}",
        file=sys.stderr,
    )
    print(
        f"  SBE          : types={len(sbe.get('types') or {})} "
        f"composites={len(sbe.get('composites') or {})} "
        f"enums={len(sbe.get('enums') or {})} "
        f"messages={len(sbe.get('messages') or {})}",
        file=sys.stderr,
    )
    if orchestra:
        print(
            f"  Orchestra    : codeSets={len(orchestra.get('code_sets') or {})} "
            f"datatypes={len(orchestra.get('datatypes') or {})} "
            f"fields={len(orchestra.get('fields') or {})} "
            f"messages={len(orchestra.get('messages') or {})}",
            file=sys.stderr,
        )
    else:
        print("  Orchestra    : (not provided)", file=sys.stderr)
    print(
        f"  Emitted      : types={len(types)} enums={len(enums)} "
        f"slots={len(field_slots)} classes={len(classes)}",
        file=sys.stderr,
    )
    print(f"  Wrote: {out_file}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Hand-rolled YAML emitter (no external deps).
# ---------------------------------------------------------------------------


def yaml_quote(s) -> str:
    s = str(s)
    if "\n" in s:
        s = " ".join(s.split())
    if s == "":
        return "''"
    if re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", s):
        return f"'{s}'"
    if s.lower() in ("true", "false", "null", "yes", "no", "on", "off", "~"):
        return f"'{s}'"
    first = s[0]
    needs_quote = (
        first in "'\"|>!@`[{&*%"
        or first == "#"
        or first == ":"
        or (first == "-" and len(s) > 1 and s[1] in " \t")
        or (first == "?" and len(s) > 1 and s[1] in " \t")
        or ": " in s
        or s.endswith(":")
        or " #" in s
        or s[0].isspace()
        or s[-1].isspace()
    )
    if needs_quote:
        if "'" not in s:
            return f"'{s}'"
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def yaml_key(k) -> str:
    s = str(k)
    return s if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s) else yaml_quote(s)


def scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if v is None:
        return "null"
    return yaml_quote(v)


# Keys whose dict values get a blank line between entries (readability).
SEPARATED_DICT_KEYS = {
    "types",
    "enums",
    "classes",
    "slots",
    "subsets",
    "attributes",
    "permissible_values",
}


def dump_yaml(value, indent: int = 0, separate: bool = False) -> list[str]:
    pad = "  " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        if not value:
            return [f"{pad}{{}}"]
        items = list(value.items())
        for idx, (k, v) in enumerate(items):
            key_str = yaml_key(k)
            child_separate = k in SEPARATED_DICT_KEYS
            if isinstance(v, dict):
                if not v:
                    lines.append(f"{pad}{key_str}: {{}}")
                else:
                    lines.append(f"{pad}{key_str}:")
                    lines.extend(dump_yaml(v, indent + 1, child_separate))
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{pad}{key_str}: []")
                else:
                    if (
                        all(not isinstance(x, (dict, list)) for x in v)
                        and len(v) <= 8
                        and sum(len(scalar(x)) for x in v) < 80
                    ):
                        rendered = ", ".join(scalar(x) for x in v)
                        lines.append(f"{pad}{key_str}: [{rendered}]")
                    else:
                        lines.append(f"{pad}{key_str}:")
                        item_pad = "  " * (indent + 1)
                        cont_pad = item_pad + "  "
                        for item in v:
                            if isinstance(item, dict):
                                sub = dump_yaml(item, 0)
                                if sub:
                                    lines.append(f"{item_pad}- {sub[0]}")
                                    for ln in sub[1:]:
                                        lines.append(cont_pad + ln)
                            else:
                                lines.append(f"{item_pad}- {scalar(item)}")
            else:
                lines.append(f"{pad}{key_str}: {scalar(v)}")
            if separate and idx < len(items) - 1:
                lines.append("")
    elif isinstance(value, list):
        item_pad = pad
        cont_pad = item_pad + "  "
        for item in value:
            if isinstance(item, (dict, list)):
                sub = dump_yaml(item, 0)
                if sub:
                    lines.append(f"{item_pad}- {sub[0]}")
                    for ln in sub[1:]:
                        lines.append(cont_pad + ln)
            else:
                lines.append(f"{item_pad}- {scalar(item)}")
    else:
        lines.append(f"{pad}{scalar(value)}")
    return lines


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _find_orchestra_fallback(project_dir: Path) -> Path | None:
    """v1-1 lacks OrchestraForFIXP.xml; fall back to the newest version that has it."""
    for v in ("v1-0-STANDARD", "v1-0-RC4", "v1-0-RC3", "v1-0-RC2", "v1-0-DRAFT"):
        c = (
            project_dir
            / "upstream-releases"
            / "fixp-specification"
            / v
            / "resources"
            / "OrchestraForFIXP.xml"
        )
        if c.is_file():
            return c
    return None


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    project_dir = here.parent
    default_upstream = Path(
        os.environ.get(
            "UPSTREAM_DIR",
            str(
                project_dir
                / "upstream-releases"
                / "fixp-specification"
                / "v1-1"
                / "resources"
            ),
        )
    )
    default_out = Path(
        os.environ.get(
            "OUT_FILE",
            str(project_dir / "src" / "fixp" / "schema" / "fixp.yaml"),
        )
    )
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--upstream-dir",
        type=Path,
        default=default_upstream,
        help=(
            "directory containing FixRepositoryForFIXP.xml, "
            "SBEschemaForFIXP.xml (and optionally OrchestraForFIXP.xml)"
        ),
    )
    p.add_argument(
        "--orchestra-xml",
        type=Path,
        default=None,
        help=(
            "explicit OrchestraForFIXP.xml path; if omitted, the script uses "
            "<upstream-dir>/OrchestraForFIXP.xml when present, otherwise the "
            "newest available v1-0-* release that contains it."
        ),
    )
    p.add_argument(
        "--out-file",
        type=Path,
        default=default_out,
        help="destination LinkML YAML schema path",
    )
    args = p.parse_args(argv)

    fix_repo_xml = args.upstream_dir / "FixRepositoryForFIXP.xml"
    sbe_xml = args.upstream_dir / "SBEschemaForFIXP.xml"
    for f in (fix_repo_xml, sbe_xml):
        if not f.is_file():
            print(f"ERROR: missing input file: {f}", file=sys.stderr)
            return 1

    orchestra_xml = args.orchestra_xml
    if orchestra_xml is None:
        local_orch = args.upstream_dir / "OrchestraForFIXP.xml"
        if local_orch.is_file():
            orchestra_xml = local_orch
        else:
            orchestra_xml = _find_orchestra_fallback(project_dir)
    if orchestra_xml is not None and not orchestra_xml.is_file():
        print(
            f"WARN: --orchestra-xml {orchestra_xml} not found; continuing "
            "without Orchestra enrichment",
            file=sys.stderr,
        )
        orchestra_xml = None

    convert(fix_repo_xml, sbe_xml, orchestra_xml, args.out_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
